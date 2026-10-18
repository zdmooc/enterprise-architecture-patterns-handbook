# Architecture de référence — Paiements instantanés SEPA sur OpenShift

**Édition consolidée V1.0 — 18 octobre 2026 — Auteur : Zidane Djamal**

**Statut :** architecture cible proposée, document de référence unifié à instruire en Design Authority. **Il ne décrit pas un SI interne vérifié de CAPS, de BPCE, de Wero, de STET ou de FIS.** Les noms de services, les plateformes, les métriques et les options techniques constituent des propositions. Aucune conception n'est « prête production » tant que les contrats avec le core, les infrastructures de place, les objectifs de service et la preuve de cohérence financière ne sont pas validés.

> **Document canonique unique.** Cette étude fusionne, réconcilie et remplace les deux études de travail consacrées au paiement instantané sur OpenShift (versions de 20 et 11 pages). **Les PDF d'origine ne sont ni copiés ni archivés dans ce dépôt.** Les règles publiques vérifiées en octobre 2026 sont référencées en section 26. Les contraintes internes restent ouvertes (section 25).

## Table des matières
1. Synthèse et recommandations
2. Périmètre, acteurs et responsabilités
3. Cadre réglementaire et sémantique SCT Inst
4. Principes non négociables et invariants
5. Architecture solution et cartographie logique
6. Capacités métier, découpage applicatif et choix de granularité
7. Modèle de données, identifiants et ownership
8. Machine à états et ordre des transitions
9. Parcours SCT Inst sortant (nominal)
10. Parcours SCT Inst entrant (nominal)
11. Contrats d'API, sécurité d'autorisation et idempotence
12. Intégration core / IBM MQ / Kafka / ACL / Outbox
13. Saga, transactions locales et point d'irréversibilité
14. Fraude, sanctions, VoP, contrôle de provision et liquidité
15. Routage multi-rails et messages ISO 20022
16. Architecture technique OpenShift
17. Cohérence et résilience multisite, fencing, PRA
18. Performance, capacité et budget temporel
19. Sécurité, conformité, audit et conservation
20. Observabilité, investigations et réconciliation
21. Livraison, migration progressive et retour arrière
22. Catalogue de scénarios de panne et tests d'acceptation
23. Matrice des patterns et décisions d'architecture (ADR)
24. Coûts, FinOps/GreenOps, exigences d'exploitation
25. Questions bloquantes et critères de validation
26. Sources publiques, terminologie et limites

---

## 1. Synthèse et recommandations

Concevoir un système 24/7 de traitement des **SEPA Instant Credit Transfers (SCT Inst)** : émission, réception, contrôles, gestion des fonds dans le core bancaire, échanges interbancaires, règlement, notifications, investigations et rapprochement. Le cœur du problème n'est pas d'« installer deux clusters OpenShift » : **c'est d'obtenir un état financier correct, vérifiable et récupérable après n'importe quelle panne, sans double mouvement sur compte**.

### Architecture cible recommandée
- **Canaux et partenaires** → API Management/Gateway → capacités Java sur OpenShift.
- **Avant autorisation du payeur** : Verification of Payee (VoP) et restitution du résultat, selon les règles applicables.
- **Création d'un ordre durable** : idempotence atomique, horodatage métier, deadline et Outbox.
- **Processus critique** : orchestration durable compacte ; accès à l'autorité de compte et aux contrôles obligatoires avec délais bornés.
- **Core bancaire existant** : **seule autorité** pour réservation, débit/crédit, visibilité financière et preuves de transaction. La plateforme n'entretient pas de « solde disponible alternatif » servant à débiter sur simple synchronisation asynchrone.
- **Connecteur rail** : choix admissible d'un seul parcours d'exécution, création et suivi des échanges ISO 20022, conservation des références.
- **Messaging** : IBM MQ **si** requis par les connecteurs/standards existants ; Kafka **si** les besoins de diffusion/rejeu/volumétrie le justifient. Ne pas imposer systématiquement les deux.
- **Outbox + consommateurs idempotents + réconciliation** : tolérer les redélivrances sans réexécuter une transaction financière.
- **Infrastructure** : OpenShift HA avec plusieurs zones de défaillance ; deuxième cluster/site pour continuité si le BIA l'exige. L'actif-actif applicatif n'implique **pas** une écriture simultanée financière sur la même partition.
- **Actif-actif contrôlé** : propriétaire d'écriture unique par domaine/partition, bail et fencing, bascule conditionnée par la visibilité des données reconnues durables, preuve de la situation des paiements en vol. **RPO 0 pour une perte de site** n'est **pas acquis** si la réplication inter-sites est asynchrone.

### Décisions non négociables
1. Une instruction client possède une identité et ne peut produire qu'un **seul effet financier autoritatif**.
2. Une confirmation MQ/Kafka, un HTTP 200/202 et une acceptation par le rail **ne valent pas règlement**.
3. Un timeout est un **résultat technique inconclusif**, jamais une preuve de rejet.
4. Une compensation Saga peut libérer une réservation ; **elle ne « rollback » pas un règlement final et irrévocable**.
5. La panne d'un site ne donne pas le droit au site survivant de réémettre aveuglément les paiements en vol.
6. Les exigences de délai SCT Inst priment sur un design de retry asynchrone pouvant prolonger le traitement sans borne.

### Décision proposée à la Design Authority
**Architecture hybride prudente, orientée invariants, avec source financière unique et intégration progressives.** Le choix « développer un nouveau moteur » contre « conserver/moderniser le progiciel existant » reste **ouvert** jusqu'à confirmation des capacités et du support éditeur. Une éventuelle solution FIS OPF/BIP doit être traitée comme produit à évaluer, pas comme architecture supposée ni comme composant à réécrire.

---

## 2. Périmètre, acteurs et responsabilités

### Périmètre fonctionnel
- SCT Inst sortant **et** entrant ; initiation depuis canal bancaire, partenaire PISP autorisé, entreprise ou scénario Wero **si un contrat réel le requiert**.
- VoP (IBAN/nom) **avant l'autorisation** du payeur et restitution du résultat.
- Authentification forte et consentement/autorisation selon les parcours et textes applicables.
- Règles de limite/plafond, anti-fraude, règles de sanctions, conformité et eligibility.
- Provision, réservation, débit/crédit et libération **par le core/tenue de compte autoritatif**.
- Émission, réception, corrélation et suivi des messages de place (CSM/settlement).
- Liquidité, retours, rappels, demandes de statut, investig. et réconciliation.
- Notification, reporting, comptabilité aval et support opérationnel.

### Hors périmètre comme système de référence
Tenue de compte principale, grand livre central, KYC maître, moteur de sanctions de référence, fraude de référence, domaine SIEM d'entreprise. Ils sont **intégrés** via contrats ; leur transformation n'est pas postulée.

### Acteurs
| Acteur | Responsabilité principale |
|---|---|
| Payeur/canal | Saisie, présentation VoP, autorisation, affichage de l'issue |
| PSP du payeur | Acceptation, contrôles, exécution, information, restauration si requise |
| PSP du bénéficiaire | Réception, validation/crédit et confirmation conformément au schéma |
| Core bancaire | Autorité sur comptes, réservations, écritures, références et preuves |
| CSM / infrastructure de règlement | Transport/compensation/règlement selon modalités du rail |
| Trésorerie | Suivi et rechargement des positions de liquidité |
| Plateforme d'intégration | Contrats, connexions, idempotence des échanges, sécurité |
| Support et investigations | Rapprochement et traitement des états incertains |

**Règle d'ownership :** l'API « Payment » gère l'intention client, l'orchestrateur le cycle de vie et le core la réalité du mouvement financier. Les vues Kafka, caches, dashboards et projections ne sont **jamais** des autorités concurrentes pour la preuve du règlement.

---

## 3. Cadre réglementaire et sémantique SCT Inst

### Textes de référence vérifiés à la date du document
- **EPC 2025 SCT Inst Rulebook version 1.2**, en vigueur le **30 septembre 2026** ; v1.2 modifie principalement les règles sur les formats d'adresse, pas la logique opérationnelle de v1.1. [EPC](https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-instant-credit-transfer-sct-inst/sepa-instant-credit-transfer).
- Règlement **UE 2024/886** (modification du règlement SEPA), notamment obligations sur SCT Inst, VoP et sanctions ciblées. [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32024R0886).
- **VoP** : effectuer la vérification à partir des données saisies **avant** de proposer au payeur l'autorisation du virement (avec exceptions et variantes prévues par les textes). [EPC FAQ VoP](https://www.europeanpaymentscouncil.eu/faq/verification-payee-scheme/rulebook/are-psp-allowed-send-vop-requests-when-intention-pay).
- **Sanctions ciblées UE** : le règlement prévoit des vérifications des utilisateurs après changement des mesures et au moins **une fois par jour** ; ne pas confondre avec les autres contrôles anti-fraude/AML, qui suivent leurs propres obligations. [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32024R0886).
- **TIPS** : règlement en monnaie de banque centrale **final et irrévocable**, fonctionnement 24/7/365 ; ne se substitue pas à la tenue de compte client. [BCE](https://www.ecb.europa.eu/paym/target/tips/html/index.es.html).
- **DORA (UE 2022/2554)** : cadre de résilience numérique ; analyse du périmètre exact des entités/prestataires et obligations de tiers requise. [EBA](https://www.eba.europa.eu/activities/direct-supervision-and-oversight/digital-operational-resilience-act).

### Découpage temporel — ne pas mélanger 9 et 10 secondes
Le chronomètre du schéma commence au **time of receipt** réglementaire de l'ordre, associé en général à l'autorisation par le payeur, et non au timestamp de réception d'un microservice. L'attribut EPC **AT-T056** est milliseconde, sans ambiguïté. Les jalons de déroulement inter-PSP sont **5 / 7 / 9 secondes** dans le rulebook 2025 ; les **10 secondes** constituent notamment l'échéance finale de gestion de l'absence de confirmation côté PSP du payeur, avec obligation de **restaurer immédiatement le compte** et d'informer le payeur selon les conditions prévues. Une éventuelle confirmation tardive exige un traitement métier spécifique, pas une suppression de l'historique. [EPC](https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-instant-credit-transfer-sct-inst/sepa-instant-credit-transfer).

**Règle de conception :** persister \`timeOfReceiptUtc\`, \`schemeDeadlineUtc\`, le temps restant et la référence du schéma ; propager la deadline aux adaptateurs. La réconciliation n'est pas bornée à 10 secondes, **mais la poursuite de l'exécution d'un ordre expiré est interdite sans décision métier conforme**.

### Distinctions indispensables
- VoP ne vaut **pas** autorisation de débit ; résultat VoP (match/close/no-match/unavailable) doit être présenté et conservé selon obligations.
- Détection fraude temps réel et obligation quotidienne de vérification des sanctions ciblées ne sont **pas** la même fonction.
- « Message pris en charge », « commande acceptée », « crédit au bénéficiaire » et « règlement final » ont des preuves distinctes.
- Les plafonds clients et les délais non réglementaires cités dans les exemples publics **ne sont pas** des paramètres universels du schéma.

---

## 4. Principes non négociables et invariants

| ID | Invariant démontrable | Preuve attendue |
|---|---|---|
| INV-01 | Une intention client répétée ne produit pas deux ordres métiers | Contrainte UNIQUE + tests de concurrence multi-pods |
| INV-02 | Une même référence d'opération au core ne produit pas deux mouvements financiers | Contrat d'idempotence du core + tests de redélivrance |
| INV-03 | Les états financiers sont durables, horodatés et auditables | Journal de transitions + preuves source autoritative |
| INV-04 | Un timeout / ACK manquant n'entraîne aucune émission indépendante | Requête de statut et procédure de rapprochement |
| INV-05 | La confirmation « réglé » provient d'une source faisant autorité | Preuve corrélée CSM/core avant état SETTLED |
| INV-06 | Un événement ne provoque pas de double effet chez un consommateur | Inbox / déduplication + écriture locale atomique |
| INV-07 | Un message après deadline ne redéclenche pas aveuglément un virement | Deadline propagée et décision enregistrée |
| INV-08 | Un règlement final ne peut être annulé par une simple compensation Saga | Restrictions machine à états + procédure de rappel/retour |
| INV-09 | Deux sites ne peuvent simultanément débiter une même partition | Fencing / époque de propriétaire / test split-brain |
| INV-10 | Après perte de site, toutes les opérations reconnues durables sont réconciliables | Preuves de commits, journal, core, rail et PRA |
| INV-11 | Un cache ou une vue analytique n'est jamais propriétaire d'un solde autoritatif | Architecture des flux et tests d'écart |
| INV-12 | Des données et secrets bancaires ne sont pas exposés dans les traces | Contrôles de masquage et d'accès |

**La notion « zéro doublon financier » est une exigence cible** : elle ne devient garantie démontrée qu'après validation du contrat du core et injections de pannes. Une simple contrainte d'unicité sur Payment API ne suffit pas.

---

## 5. Architecture solution et cartographie logique

~~~mermaid
flowchart TB
  U["Canal Web / Mobile / Partenaire"]
  VOP["Vérification du bénéficiaire VoP"]
  IAM["IdP / SCA / Autorisation du payeur"]
  GW["API Gateway / API Management"]
  API["Payment API / Order Management"]
  ORC["Orchestration durable + deadlines"]
  RISK["Validation / Risques / Fraude"]
  ACCT["Account Adapter / ACL"]
  CORE["Core bancaire : comptes et écritures (autorité)"]
  ROUTE["Routing + Scheme Adapter"]
  CSM["CSM / TIPS / autres rails sous contrats"]
  DB[("DB transactionnelle ACID : ordres, journal, Inbox, Outbox")]
  OUT["Relais Outbox / messaging bridge"]
  MQ["IBM MQ si l'existant l'exige"]
  KAFKA["Kafka si diffusion/rejeu justifiés"]
  NOTIF["Notifications / Canaux"]
  ANA["Reporting, audit, supervision"]
  REC["Réconciliation / Investigations"]

  U --> VOP --> U
  U --> IAM --> GW
  GW --> API
  API <--> DB
  API --> ORC
  ORC --> RISK
  ORC --> ACCT --> CORE
  ORC --> ROUTE --> CSM
  ORC <--> DB
  DB --> OUT
  OUT --> MQ
  OUT --> KAFKA
  MQ <-.-> ACCT
  KAFKA --> NOTIF
  KAFKA --> ANA
  CORE --> REC
  CSM --> REC
  DB --> REC
  REC --> ORC
~~~

**Lecture du schéma :** les flèches représentent des dépendances logiques ; il ne faut pas en déduire que l'ordre doit transiter **simultanément** par REST + MQ + Kafka. Un **contrat unique choisi par liaison** prévaut. La Gateway ne déclenche pas la transaction financière. La VoP précède l'autorisation. Les événements non critiques sont dérivés **après validation durable**.

### Vue C4 — containers logiques

| Zone | Container/fonction | Stateful ? | Source autoritative ? |
|---|---|---|---|
| Exposition | API Gateway + WAF selon topologie | Non / configuration externe | Non |
| Domaine paiement | API / orchestration / contrôle | Stateless runtime ; état persistant externe | Autorité sur *intention*, pas mouvement |
| Domaines intégration | Account ACL / Scheme Adapter | Sessions externes maîtrisées | Non |
| Données paiement | DB ACID + outbox/inbox + journal | Oui | État opérationnel du moteur |
| Intégration historique | MQ (si requis) | Oui | Transport, non effet financier |
| Bus événementiel | Kafka (si requis) | Oui | Historique dérivé, non grand livre |
| Dépendances | Core + PSP/CSM/TIPS | Existants et externes | Oui pour leurs domaines |
| Contrôle | Reconciliation + investigations | Oui | Gestion des preuves/écarts |

La présence de MQ et Kafka n'est **pas** une exigence d'office : documenter le coût, le support éditeur, la reprise et le bénéfice réel de chaque broker.

---

## 6. Capacités métier et découpage applicatif

**Ne pas confondre capacités logiques et nombre de microservices.** Conserver sur le chemin critique un nombre mesuré de sauts, avec frontières de responsabilité explicites.

| Capacité logique | Fonction | Déploiement initial candidat |
|---|---|---|
| API & Order Management | AuthN/AuthZ applicative, validations, idempotency-key, ordre durable | 1 service Java |
| Payment Orchestrator | Machine à états, budget de temps, Saga, reprise | 1 service Java ou moteur existant |
| Validation/Risk adapter | Référentiels, limites, fraude, conformité | Module/adaptateur dans services critiques |
| Account ACL | Réservation/débit/crédit et statut via core | 1 adapter selon contrat |
| Routing/Scheme adapter | Rail choisi, ISO 20022, statut/corrélation | 1–N connecteurs selon rail |
| Inbound handling | Déduplication, crédit, confirmation, reprise | 1 traitement spécifique |
| Liquidity coordination | Positions, seuils, réapprovisionnement sous contrôle trésorerie | Séparé et supervisé |
| Reconciliation & investigation | Preuve financière, écarts, corrections autorisées | Service/worker distinct |
| R-transactions | Recall, return, status et investigations | Workflow séparé |
| Notification / Reporting | Canal client et exploitation analytique | Consommateurs indépendants |
| VoP | Consultation et présentation **avant autorisation** | Capacité canal/PSP indépendante |

Une option existante FIS OPF ou autre moteur de paiement peut **déjà fournir** l'orchestration, ISO 20022, états, persistance et règles. Ne pas développer un moteur concurrent avant un **fit-gap éditeur** et une matrice de support OpenShift/configuration.

**SLO de conception :** optimiser nombre de transitions persistées, appels série/parallèles et latence p99 sous charge. Éviter l'« orchestration via 12 microservices » imposée sans preuve.

---

## 7. Modèle de données, identifiants et ownership

### Identités distinctes (ne jamais fusionner par commodité)
| Identifiant | Portée | Usage |
|---|---|---|
| clientRequestId / idempotencyKey | Client + canal + intention | Répétition de demande HTTP/partenaire |
| internalPaymentId | Moteur paiement | Clé stable du paiement |
| endToEndId | ISO 20022 / parcours commercial | Corrélation, pas nécessairement unique globalement |
| externalTxId / schemeReference | Rail / PSP | Identité des messages ou transaction interbancaire |
| accountOperationId | Core | Preuve d'une réservation, débit ou crédit unique |
| attemptId / transportMessageId | Tentative technique | Retries, erreurs, audit, distincts de l'intention |
| eventId / eventSequence | Evénement / agrégat | Déduplication et ordre des transitions |
| ownerEpoch / fencingToken | Domaine de données | Contrôle propriétaire d'écriture après bascule |
| traceId / correlationId | Observabilité | Diagnostics sans valeur de preuve financière autonome |

**Interdiction :** prendre l'IBAN comme seule clé d'unicité de paiement. Il peut aider au partitionnement ou au routage interne, mais doit être protégé et ne dit pas qu'une **intention de paiement précise** est unique.

### Schéma logique (proposition)
~~~text
PaymentOrder(internalPaymentId PK, entityId, clientId, channelId,
             idempotencyKey, requestFingerprint, debtorRef, creditorRef,
             amountMinor, currency, timeOfReceiptUtc, schemeDeadlineUtc,
             state, stateVersion, ownerPartition, ownerEpoch, createdAt)
UNIQUE(entityId, channelId, clientId, idempotencyKey)

PaymentTransaction(transactionId PK, paymentId FK, scheme, railId,
                   schemeReference, settlementReference, outcome, outcomeEvidenceRef)

AccountOperation(accountOperationId PK, paymentId FK, operationType,
                 coreReference, status, evidenceRef)
UNIQUE(coreReference, operationType)

PaymentAttempt(attemptId PK, paymentId, target, startedAt, finishedAt,
               result, errorCategory, correlationId)

PaymentEvent(eventId PK, paymentId, eventSequence, oldState, newState,
             timestampUtc, causationId, evidenceRef)
UNIQUE(paymentId, eventSequence)

Inbox(consumerId, messageId, processedAt, businessReference)
UNIQUE(consumerId, messageId)

Outbox(eventId PK, aggregateId, eventType, schemaVersion,
       payloadRef, occurredAt, publishState, attempts)

ReconciliationItem(itemId PK, paymentId, source, discrepancyType,
                   evidenceRefs, workflowState, owner, lastUpdate)

InvestigationCase(caseId PK, paymentId, status, reason,
                  approver, evidenceRefs, actionLog)
~~~

**Atomicité locale :** changement d'état + PaymentEvent + Outbox en **une transaction DB**. Versionnement optimistic locking/CAS ; contrôle des transitions autorisées. Le journal d'événements de l'application n'est **pas un substitut** aux journaux de règlement/compte.

### Rétention, confidentialité et audit
Périodes de conservation à décider avec juridique, conformité et politique de données (ne pas attribuer arbitrairement « 13 mois » à tous les objets). L'Outbox peut être nettoyée seulement après publication confirmée et possibilité raisonnable de reprise ; les clés d'idempotence doivent survivre à la fenêtre de replay technique/métier. Pseudonymiser les références dans Kafka et observabilité ; chiffrer colonnes sensibles lorsque requis.

---

## 8. Machine à états et cohérence

Trois axes **indépendants**, jamais un état unique ambigu.

### Paiement : état d'exécution
~~~mermaid
stateDiagram-v2
  [*] --> RECEIVED
  RECEIVED --> VALIDATING
  VALIDATING --> REJECTED_PRE_SUBMISSION
  VALIDATING --> AUTHORIZED_FOR_EXECUTION
  AUTHORIZED_FOR_EXECUTION --> SUBMITTED
  SUBMITTED --> CONFIRMED_SETTLED
  SUBMITTED --> CONFIRMED_REJECTED
  SUBMITTED --> CONFIRMATION_MISSING
  CONFIRMATION_MISSING --> INVESTIGATION_REQUIRED
  INVESTIGATION_REQUIRED --> CONFIRMED_SETTLED: preuve tardive
  INVESTIGATION_REQUIRED --> CONFIRMED_REJECTED: preuve de rejet
~~~
Les transitions après échéance sont **spécifiques au schéma** et doivent être explicitement approuvées. Le statut d'ordre et le règlement doivent être distingués dans les noms (une commande peut être « ACCEPTED_FOR_PROCESSING » sans être « SETTLED »). Une confirmation tardive ne peut être supprimée pour préserver artificiellement un état terminal local.

### Compte (autorité = core)
~~~text
NONE -> RESERVATION_PENDING -> RESERVED -> (RESERVATION_RELEASED | DEBIT_BOOKED)
NONE -> CREDIT_PENDING -> CREDIT_BOOKED    [parcours entrant]
UNKNOWN_ACCOUNT_OPERATION -> INVESTIGATION_REQUIRED
~~~
La restauration du compte prescrite à la dixième seconde **ne vaut pas** « le rail n'a rien exécuté » ; le rapprochement et, si nécessaire, la régularisation contrôlée restent ouverts.

### Investigation
\`NOT_REQUIRED → OPEN → EVIDENCE_REQUESTED → RESOLVED / MANUAL_REVIEW\`.

### Interdits
- \`CONFIRMED_SETTLED → RECEIVED\` sur événement tardif.
- \`SUBMITTED → REJECTED\` seulement parce qu'un appel a timeout.
- \`CONFIRMATION_MISSING → réémission indépendante\` sans consultation autoritative et examen de deadline.
- \`RESERVATION_RELEASED\` sans preuve de libération dans le core.

---

## 9. Parcours SCT Inst sortant

### Phase A — avant l'autorisation, hors chrono d'exécution lorsque réglementairement applicable
1. Saisir bénéficiaire (IBAN/nom), montant et contexte.
2. Exécuter **VoP** et communiquer la réponse au payeur.
3. Appliquer les règles de présentation/avertissement, exceptions et contrôle du consentement.
4. Authentifier/autoriser l'ordre (SCA selon parcours) et capturer le **time of receipt** réglementaire (AT-T056, précision milliseconde).

### Phase B — exécution critique, bornée
1. Gateway valide accès, quotas et contrat API ; le service vérifie **l'autorisation objet et métier**.
2. Établir l'intention idempotente, la référence interne et la deadline ; commit durable.
3. Contrôler les limites et les règles de conformité applicables ; interroger les dépendances avec timeout strict.
4. Solliciter le core pour réserver/autoriser les fonds par **référence stable** ; recevoir preuve de réservation.
5. Déterminer rail admissible (joignabilité, modèle de participation, liquidité, capacité, règles) ; enregistrer route choisie.
6. Persister intention d'émission + Outbox ; Scheme Adapter envoie selon protocole du rail **sans créer de nouvelle intention**.
7. Corréler preuves interbancaires et core ; finaliser état côté PSP et opérations sur compte selon les règles et contrats convenus.
8. Publication Outbox d'événements **post-commit**, notification et reporting séparés.
9. Si confirmation absente à échéance, suivre exactement les obligations EPC de **restauration/information** et démarrer réconciliation.

~~~mermaid
sequenceDiagram
  autonumber
  actor P as Payeur
  participant V as VoP
  participant C as Canal + SCA
  participant A as Payment API + DB
  participant O as Orchestrateur
  participant K as Core bancaire
  participant R as Rail/CSM
  participant E as Outbox / événements
  P->>V: Bénéficiaire IBAN + nom
  V-->>P: Résultat VoP affiché
  P->>C: Autorisation du paiement
  C->>A: POST + Idempotency-Key + temps de réception
  A->>A: Transaction intention + Outbox
  A->>O: Référence persistée
  O->>K: Reserve(paymentId, coreOperationId)
  K-->>O: PREUVE reservation
  O->>R: Ordre ISO 20022 (deadline, ref)
  alt Confirmation positive vérifiée
    R-->>O: Statut autoritatif
    O->>K: Finaliser selon contrat core
    K-->>O: Écritures confirmées
    O->>A: SETTLED + preuve durable
  else Refus confirmé avant règlement
    R-->>O: Rejet avéré
    O->>K: Libérer réservation (même ref)
    O->>A: REJECTED après preuve
  else Pas de confirmation au délai EPC
    O->>K: Procédure de restauration applicable
    O->>A: CONFIRMATION_MISSING + investigation
  end
  A->>E: Evénement confirmé dans Outbox
  E-->>C: Notification suivant statut/contrat
~~~
**Remarque :** représentation fonctionnelle ; les obligations exactes du PSP et du CSM pilotent l'ordre final des écritures et confirmations. Les étapes pouvant être déplacées avant T0 doivent être identifiées et approuvées.

---

## 10. Parcours SCT Inst entrant

1. Le Scheme Adapter reçoit un message ISO 20022 authentifié selon le rail et identifie l'**entité, message, transaction et références**.
2. Contrôle schéma/version, heure, répétition (Inbox durable) et éligibilité du bénéficiaire.
3. Interroge le **core** par référence de crédit stable ; ne peut pas fabriquer un solde autoritatif local.
4. Applique les contrôles conformes au rôle PSP bénéficiaire et au protocole rail, notamment les délais de décision.
5. Envoie la réponse interbancaire attendue ; ne la confond pas avec un ACK de transport.
6. Finalise crédit, état et journal par preuve core/settlement ; publie événements après commit et notifie.
7. Si crédit enregistré puis réponse de confirmation perdue, **redélivrer n'entraîne jamais un deuxième crédit**.

~~~mermaid
sequenceDiagram
  participant R as Infrastructure de paiement
  participant A as Inbound Adapter
  participant D as Inbox/État durable
  participant C as Core bancaire
  R->>A: pacs.008 / instruction
  A->>D: Dédupliquer référence rail/transaction
  alt Nouveau et valide
    A->>C: Crédit / engagement via référence stable
    C-->>A: Preuve ou résultat inconnu
    A->>D: Enregistrer résultat durable
    A-->>R: Confirmation suivant protocole
  else Déjà traité
    D-->>A: Retrouver résultat durable
    A-->>R: Même résultat, aucune nouvelle écriture
  end
~~~
Tests obligatoires : crédit accompli/ACK perdu, compte bloqué ou fermé, pod tué après commit, reprise de session, confirmation tardive, message illisible, même référence avec contenu divergent, core en panne.

---

## 11. Contrats d'API, identité et idempotence

### API illustrative — *pas* un contrat CAPS
~~~http
POST /api/v1/instant-payments
Authorization: Bearer <token>
Idempotency-Key: req-unique-001
X-Correlation-ID: trace-001
Content-Type: application/json

{"debtorAccountRef":"acct-a","creditorIban":"EXAMPLE",
 "amountMinor":50000,"currency":"EUR","scheme":"SCT_INST"}
~~~
Le payload est illustratif (l'IBAN \`EXAMPLE\` n'est **pas** valide). En production : schémas stricts, bénéficiaire complet, preuves VoP/SCA et classification de données.

Réponse d'acquisition candidate :
~~~http
HTTP/1.1 202 Accepted
Location: /api/v1/instant-payments/VIR-001
Content-Type: application/json

{"paymentId":"VIR-001","processingStatus":"PROCESSING"}
~~~
**Précaution réglementaire :** \`202\` prouve uniquement l'acquisition selon le contrat API. Il ne dispense pas le PSP du retour d'issue SCT Inst dans les délais applicables ; définir le canal et les mécanismes de notification conformément au schéma.

### Algorithme d'unicité
1. Scope = (entité, client, canal, type d'opération, idempotencyKey), empreinte canonique des données financières.
2. Transaction DB ACID ; contrainte \`UNIQUE(scope)\`; insert ordre **et** Outbox atomiques.
3. Clé existante + même empreinte → **même paymentId**, statut et liens de suivi.
4. Clé existante + empreinte différente → **conflit** ; aucune modification silencieuse.
5. Deux requêtes simultanées sur deux Pods → verrouillage/contrainte DB arbitre un seul propriétaire.
6. La clé HTTP n'est **pas** suffisante : le core déduplique la **référence financière stable**.
7. Après timeout, consulter les états reconnus par core/rail ; ne pas générer de nouvel ordre sur un retry.

### Résultats API
- \`401\` identité invalide ; \`403\` autorisation insuffisante ; \`409\` conflit d'idempotency-key (suivant contrat) ; \`422\` rejet de règles d'entrée ; \`429\` quotas ; \`503/504\` indisponibilité/timeouts.
- Ne pas déduire \`PAYMENT_REJECTED\` d'un simple HTTP \`503\` ou \`504\`.
- \`GET /api/v1/instant-payments/{paymentId}\` protégé par **authorization object-level** et anti-enumeration.
- \`traceId\` et \`correlationId\` ne remplacent pas preuve financière.

### Sécurité des APIs
OIDC identifie un utilisateur dans le contexte convenu ; OAuth 2.0 régit les délégations/autorisations ; JWT est un format de token possible. Vérifier signature, iss/aud/exp/nbf/scopes et rotation de clés ; TLS/mTLS pour partenaires/interopérabilité selon contrat. L'autorisation d'accéder à une API **ne vaut pas** autorisation du virement.

---

## 12. Intégration core / MQ / Kafka / ACL / Outbox

### Commandes et événements
| Objet | Exemple | Sémantique |
|---|---|---|
| Commande | \`ExecutePayment(paymentId, deadlineUtc)\` | Demande d'action, potentiellement répétée au transport |
| Evénement | \`PaymentSettled(paymentId, evidenceRef)\` | Fait attesté, après commit et preuve autoritative |
| Accusé technique | \`MQ PUT OK\` | Broker a accepté, **pas** core/rail exécuté |
| Réponse métier | \`PaymentRejected / SettlementConfirmed\` | Résultat interprété selon source et protocole |
| Correction | \`InvestigationResolved\` | Fin d'un workflow de preuve, non création rétroactive de règlement |

### Outbox : atomicité locale uniquement
~~~mermaid
sequenceDiagram
  participant S as Service de paiement
  participant D as DB ACID
  participant P as Publisher
  participant B as IBM MQ ou Kafka
  participant C as Consumer
  S->>D: BEGIN
  S->>D: UPDATE payment + INSERT Outbox
  S->>D: COMMIT
  P->>D: Lire Outbox non publiée
  P->>B: Publier même eventId/paymentId
  B-->>P: ACK de transport
  Note over P,B: Crash ici => republication possible
  B->>C: Redélivrance éventuelle
  C->>C: Inbox/dédoublonnage + effet local atomique
~~~
L'Outbox ne garantit pas à elle seule une livraison **exactly-once** ; son relais peut republier. Kafka garantit l'ordre **dans une partition**, pas entre toutes les partitions ; utiliser une clé stable selon le besoin d'ordre, protéger PII et envisager les changements de partitionnement. Ne pas faire d'un topic Kafka le seul support de preuve d'un paiement.

### IBM MQ : quand le choisir
Contrats imposant une queue avec legacy, messages persistants, \`syncpoint\`, request/reply asynchrone, reprise contrôlée, backout queue applicative et dead-letter queue de transport. **Un message ancien doit être relu avec sa deadline et son état, jamais exécuté comme neuf.** Les redélivrances sont normales lors de crash avant ACK.

### Kafka : quand le choisir
Diffusion multi-abonnés, analyses en continu, projections, rejeu selon rétention ; topiques par faits confirmés (\`payments.status.v1\`) ; clé \`paymentId\` lorsque la préservation d'ordre par paiement est requise, ACLs, TLS/SASL selon installation, \`acks=all\`, réplication et stratégie de reprise. Les offsets n'ont aucun pouvoir sur le core financier.

### Anti-Corruption Layer
Traduction API/JSON ↔ COBOL/CICS/MQ ou format propriétaire, y compris **sémantique** des statuts :
\`Legacy A01\` (*hypothétique*) → \`ACCEPTED_FOR_PROCESSING\`, **jamais** \`SETTLED\`.
\`Timeout\` → \`UNKNOWN / TO_RECONCILE\` et consultation par identifiant stable.
Contract tests, versionnement, erreurs, montants en unité minimale, champ source, chiffrement, audit.

### Décision d'intégration
**Privilégier l'intégration existante compatible**. Ajouter IBM MQ **et** Kafka uniquement si les exigences transport de commandes **et** diffusion/rejeu justifient deux socles distincts. Tenir un registre de flux décrivant source, cible, protocole, identité, schéma, timeout, SLA et comportement en panne.

---

## 13. Saga, transactions et irréversibilité

### Transactions locales
- Transaction DB paiement/outbox atomique.
- Opération de réservation/débit **dans le core bancaire**, avec son propre contrat d'atomicité et idempotence.
- Publication/redélivrance entre les deux assurées par une stratégie explicitement choisie.
- Pas de **XA distribué présumé** entre DB, broker, core et rail. XA n'est pas « techniquement impossible sur Kubernetes », mais impose coûts, support de toutes les ressources et contraintes de cohérence difficiles ; sa décision exige une preuve et n'est pas le défaut.

### Saga avec orchestration
~~~mermaid
flowchart TD
  A["Ordre et autorisation"] --> B["Contrôles requis"]
  B -->|KO| R["Rejet avant soumission"]
  B -->|OK| C["Réserver fonds par core"]
  C -->|KO| R
  C -->|OK| D["Soumettre au rail"]
  D -->|Rejet certain avant règlement| L["Libération autorisée selon core"]
  D -->|Confirmation réglée| S["Finaliser résultat"]
  D -->|Issue inconnue| I["Restaurer selon règles + Investigation"]
  I --> Q["Consulter, rapprocher, régulariser sous contrôle"]
~~~
**Compensation réversible** : libérer une réservation prouvée, sans double libération. **Point pivot** : le règlement irrévocable au niveau du rail concerné, et les autres engagements suivant contrats ; l'architecte doit préciser ce pivot par scénario. Une *return/recall* constitue une **nouvelle procédure réglementée**, non un rollback.

### Scénarios
| Incident | Conduite |
|---|---|
| Fraude négative après réservation | Libération idempotente + état REJECTED après preuve |
| Réservation réussie mais réponse core perdue | Relire par référence, sans re-réserver aveuglément |
| Soumission rail puis timeout | UNKNOWN, statut, délai et rapprochement, aucune nouvelle émission indépendante |
| Confirmation SETTLED puis notification KO | Rejouer notification uniquement |
| Compensation KO | Etat compensating/needs-action durable, alerte et reprise contrôlée |
| Saga leader en panne | Reprise depuis état durable avec ownership/epoch, aucun double effet |

Le *retry* n'est jamais un mécanisme pour « forcer » une transaction financière dont l'issue n'est pas connue.

---

## 14. VoP, fraude, sanctions, provision, liquidité

### VoP
Vérification IBAN/nom depuis le canal **avant** l'autorisation ; afficher \`match\`, \`close match\`, \`no match\` ou \`verification not possible\` suivant les contrats VoP courants et règles applicables. Tracer preuve et information donnée au payeur, sous protection RGPD. Les règles en cas de divergence doivent être validées par le métier/conformité.

### Sanctions, fraude, AML
Distinguer la vérification **au moins quotidienne** des utilisateurs visés par sanctions ciblées UE et les autres contrôles de fraude/AML éventuellement en temps réel. Ne pas imposer un check transactionnel de listes UE ciblées qui contredirait l'approche prévue par le règlement, ni supprimer des contrôles prescrits par d'autres régimes. Le « fallback si moteur fraude indisponible » est une **décision de risque/conformité**, et non une astuce technique.

### Gestion de provision
Une réservation locale au moteur ne donne pas le droit d'afficher ou de débiter un solde alternatif. **Toute transition de fonds doit être attestée par l'autorité du core**. Si le core n'offre pas de reservation/cancel/status idempotents dans les temps, le design doit être révisé ; un cache ne corrige pas cette lacune.

### Liquidité
Suivre positions, seuils et disponibilité par rail/entité ; en TIPS, les comptes dédiés et responsabilités de trésorerie doivent être décrits par accord de participation réel. Alimentation et transfert de liquidité ne doivent pas être déclenchés sur une métrique de cache isolée sans autorisation et procédures de contrôle.

---

## 15. Routage multi-rails et ISO 20022

### Options
STET / TIPS / RT1 sont des **pistes d'intégration conditionnées** par les contrats PSP/CSM, la participation, joignabilité et connectivité. Leur présence chez CAPS/BPCE **n'est pas affirmée**. Le schéma SCT Inst et les profils du rail régissent la construction des messages.

### Messages à étudier
| ISO 20022 (famille) | Usage courant / précaution |
|---|---|
| \`pacs.008\` | Instruction de transfert interbancaire, profil exact selon rail |
| \`pacs.002\` | Statut / confirmation interbancaire dans les scénarios applicables |
| \`pacs.004\` | Retour de fonds selon procédure, **pas rollback** |
| \`camt.056\` | Demande de rappel/annulation suivant schéma/profil |
| \`camt.029\` | Réponse d'investigation/rappel suivant profil |
| \`pain.001\` | Initiation client/entreprise dans certains parcours, pas universel |
Les versions XML, obligations de signature, champs, codes statut et acheminement doivent être établis sur les **Implementation Guidelines de la version exacte** et les règles CSM/banque.

### Bascule de rail : principe de prudence
**Ne jamais** relancer un paiement vers TIPS parce que STET n'a pas répondu. Préconditions minimales :
1. Preuve que la commande **n'a pas été exécutée** (ou protocole de bascule garantissant unicité de bout en bout).
2. Même identité métier et corrélation traçable du changement de tentative.
3. Rails et bénéficiaire joignables ; capacité/liquidité; accords CSM compatibles.
4. Temps restant avant deadline suffisant.
5. Autorisation métier/conformité de l'option et journal de décision.
Sinon : **investigation** et réponse conforme au statut disponible.

Un Circuit Breaker peut protéger un connecteur malade. Il ne crée pas de droit de reroutage financier.

---

## 16. Architecture technique OpenShift

### Topologie retenue par hypothèse
- Deux clusters OpenShift indépendants **si** BIA/exigences régionales justifient la reprise de site ; plusieurs zones physiques par cluster **si le datacenter/cloud les fournit réellement**.
- Déploiements répliqués pour **fonctions sans état**, anti-affinité/topology spread, capacity planning et niveaux de priorité ; ne pas compter sur les pods pour porter l'état de Saga.
- Systèmes de données et brokers dans cluster ou managés **à arbitrer** selon RTO/RPO, support, stockage, licences, exploitation et isolation des mises à niveau.
- Gestion multi-cluster (ACM ou équivalent) et GitOps pour politiques et configuration ; **n'assurent pas** la cohérence des données métier.
- GSLB / load balancing conforme à la politique d'écriture ; affinité d'interface ou de session **ne constitue pas un verrou d'autorité financière**.

### Sondes et HPA
| Élément | Décision |
|---|---|
| \`startupProbe\` | Distinguer démarrage lent et process réellement défaillant |
| \`readinessProbe\` | Retirer du trafic un Pod incapable d'assurer son contrat local |
| \`livenessProbe\` | Redémarrer process irrécupérable, **pas** sur un core externe indisponible |
| PDB | Limiter évictions volontaires ; pas remède à une panne brutale |
| HPA/KEDA | CPU, concurrence, lag ; bornes selon débit supporté par core/rail |
| Ressources | Requests/limits chiffrés après profiling Java, CPU, GC, TLS, connexions, mémoire |
| NetworkPolicy | Default deny + flux sortants strictement autorisés |
| TLS | Gateway → Route → Service, reencrypt / passthrough suivant exigences |
| Secrets | Vault / External Secrets / PKI ; rotation testé, aucun secret en Git |

~~~mermaid
flowchart TB
  G["GSLB / DNS / API Edge"]
  subgraph SA["Site A — OpenShift Cluster A"]
    A1["Zone A1 — services"]
    A2["Zone A2 — services"]
    A3["Zone A3 — services"]
    DA["DB/broker HA locaux"]
  end
  subgraph SB["Site B — OpenShift Cluster B"]
    B1["Zone B1 — services"]
    B2["Zone B2 — services"]
    B3["Zone B3 — services"]
    DB["DB/broker HA locaux"]
  end
  ARB["Quorum / arbitrage / fencing indépendant"]
  G --> SA
  G --> SB
  DA <-.->|"Réplication à définir : jamais présumer RPO 0"| DB
  ARB -.-> SA
  ARB -.-> SB
~~~

**Aucune promesse** de « 3 zones par site » sans démonstration des domaines de panne indépendants et analyse du quorum. La capacité survivante doit supporter le trafic pendant une panne de zone et, si exigé, de site.

### HA des données
- PostgreSQL HA (opérateur qualifié) **ou** Oracle/SQL distribué selon standards, performance et support. Démontrer quorum, latence d'ACK, RPO/RTO et procédure split-brain.
- MQ HA selon produit/édition et topologie ; stockage fiable et consommateurs idempotents.
- Kafka HA si justifié : réplication et \`min.insync.replicas\`, traitement des interruptions et quotas ; MirrorMaker/asynchrone **ne reproduit pas un commit financier synchrone**.
- Copies/backup indépendants, récupération de corruption logique, restauration testée et clé de chiffrement accessible pendant PRA.

---

## 17. Cohérence et résilience multisite, fencing, PRA

### Pourquoi l'actif-actif naïf est incorrect
Deux clusters accessibles par GSLB, avec bases répliquées en asynchrone, peuvent **chacun accepter la même intention** et subir une panne réseau. Un hash d'IBAN à la Gateway n'est **pas** un mécanisme de sérialisation sûre. Un fencing tardif empêche d'aggraver le split-brain, mais ne rétablit pas des écritures déjà acquittées et absentes du site secours.

### Modèle d'autorité proposé
- Définir **partition métier** (par entité/compte selon invariants et contraintes core) avec **un propriétaire d'écriture actif** à l'instant T.
- Stocker et faire respecter **ownerEpoch / fencing token** par la ressource qui applique les écritures, pas seulement par le proxy HTTP.
- La répartition initiale peut être active sur les deux sites pour **des partitions différentes** ; une même partition n'a **qu'un écrivain**.
- En perte/partition réseau : mettre en quarantaine l'ancien propriétaire, prouver la fin du bail et la promotion de la version correcte avant reprise de l'écriture.
- Un nouvel écrivain doit disposer **de toutes les transactions reconnues durables** ou suspendre l'admission et reconstituer/réconcilier avant d'exécuter. Ne jamais promettre RPO 0 avec un flux async seul.
- Les commandes en vol au core/CSM sont consultées via leurs références, y compris celles potentiellement absentes de la réplication du moteur.

### Alternatives de données
| Option | Bénéfices | Risques / condition |
|---|---|---|
| Site unique écrivain + site secours | Modèle simple, ownership clair | Bascule lente selon volumes et réseau ; RPO à prouver |
| Partitions active-active avec writer exclusif par partition | Utilisation des deux sites | Ownership, routing durable, fencing fort et failover par partition |
| DB distribuée à consensus/quorum étendu | Peut fournir garantie forte de commit selon modèle | Coût en latence, distance, quorum, support et partitionnement |
| Réplication asynchrone inter-site seule | Performance et coût | **RPO > 0 possible** ; ne suffit pas à zéro perte d'ordres acquittés |

**Choix recommandé pour phase 1 :** HA locale prouvée, site secondaire en capacité disponible, bascule **contrôlée** par procédure de données et core ; activer le multi-site à double ownership partitionné seulement après exercice de split-brain concluant.

### Playbook de bascule
1. Identifier panne et portée réelle : pod, nœud, zone, cluster, site, stockage, core, réseau/rail.
2. Geler les nouvelles admissions financièrement risquées sur partitions impactées, tout en exposant statuts/informations compatibles.
3. Retirer accès en écriture de l'ancien propriétaire ; **fencing prouvé**, renouvellement de l'époque d'autorité.
4. Évaluer perte de visibilité de réplication ; comparer positions de logs, transactions reconnues et données source.
5. Vérifier toutes les instructions en vol : core, messages reçus, CSM, idempotency-keys, Outbox.
6. Promouvoir la ressource cohérente après contrôle ; réinitialiser connexions/credentials si nécessaire.
7. Reprendre consommation et production avec **mêmes références**, deadline vérifiée ; pas d'exécution rétroactive non autorisée.
8. Ouvrir progressivement acquisition et routage ; surveiller écarts, résultat financier et SLA.
9. Exécuter rapprochement et investigations, consigner preuves et approbations.
10. Préparer un **failback distinct**, sans lancer deux écrivains lors du retour du site.

### RPO / RTO explicités
- **Zone** : viser RPO 0 seulement si ack de commit durable exige quorum intra-site survivant, démontré en test.
- **Site** : RPO non nul possible en réplication async ; le RPO de données *et* le RPO des **ordres reconnus au client** doivent être analysés séparément.
- **RTO** : valeur issue du BIA, du volume en vol, des contrôles manuels et de la reprise des sessions rails ; aucun nombre universel « 15 min » ne suffit.
- **Corruption logique** : ni réplication sync ni active-active ne remplacent sauvegardes, PITR, validation/restauration et journal de preuves indépendant.

---

## 18. Performance, capacité et budget temporel

### Enveloppe réglementaire
\`T0 = timeOfReceipt/AT-T056\` ; chaque appel reçoit \`deadlineUtc\` et le budget résiduel. Les budgets ci-dessous ne sont **pas des valeurs de production** et doivent être évalués en p99 sous charge et panne.

| Fonction interne | Budget illustratif *candidat* | Commentaire |
|---|---:|---|
| Gateway + Order Management + commit intention | 50–150 ms | Revoir en charge multi-zone |
| Contrôles réellement requis après T0 | 100–500 ms | Certains peuvent se produire avant T0 selon règles |
| Provision/core | 100–300 ms | **Mesure core indispensable**, sinon architecture à revoir |
| Orchestration + persistance + adaptateur | 50–200 ms | Inclure contention/quorum réseau |
| Rail + PSP destinataire | Temps restant | Contrat CSM et sous-délais EPC 5/7/9 |
| Finalisation + information | Budget spécifique | Obligation à 10 s et confirmations tardives |

La somme de moyennes n'est pas un p99 bout en bout : mesurer **distributions corrélées, rafales, contention, GC, I/O, TLS, WAN, invalidation cache, retry et failover**. Ne pas laisser un timeout de 2 s + 3 retries dépasser la deadline.

### Hypothèses de volumétrie à valider
Scénario purement illustratif : \`TPS moyen = 300\`, \`TPS crête = 1 500\`, marge à étudier selon BIA. **Ce ne sont pas des données CAPS ou BPCE**. Little : \`concurrence ≈ débit × durée\` ; à 1 500 TPS et 2 s, environ 3 000 transactions simultanées **en moyenne pendant cette durée**, avant marge et queues. Mesurer débit maximum par core et rail, IOPS/commit, queues depth, consumer lag, CPU/GC/pools, max connections et capacité mono-site.

### SLOs proposés comme exigences à négocier
| Indicateur | Principe |
|---|---|
| Succès dans délais EPC | Mesurer depuis T0 réel, distinguer parcours et exceptions |
| Duplicate financial effects | **0**, prouvé par tests + core |
| Ordres reconnus définitivement perdus | **0 cible**, justifier modèle durable et RPO |
| Paiements UNKNOWN | Taux et ancienneté mesurés ; objectif à fixer |
| Temps de reprise zone/site | BIA + exercices, pas une assertion |
| API p95/p99 | Seuils par endpoint et budget bout en bout |
| Rapprochement | Âge maximal des écarts critiques et règles d'escalade |

**Alerte :** un SLO 99,9 % « délai respecté » ne suspend **aucune** obligation légale individuelle ; il mesure les performances. En cas de non-conformité, traitement réglementaire requis pour chaque ordre.

---

## 19. Sécurité, conformité, audit et conservation

### Architecture de confiance
- Zone canaux/partenaires → WAF/API Gateway → OpenShift ingress → services → data → adaptateurs core et CSM.
- mTLS selon contrats, rotation de certificats, service accounts par application, NetworkPolicy default deny, egress contrôlé, segmentation CNI/pare-feu.
- OAuth2/OIDC et SCA canal ; authorization object-level et politique d'autorisation métier séparées. Pas de « confiance » implicite parce qu'un appel est intracluster.
- HSM/KMS lorsque exigé pour les clés de signatures/messages de place ; secrets hors Git et images, rotation testée.
- Supply-chain : SBOM, analyse de vulnérabilités, signatures Cosign/équivalent selon standards, contrôles d'admission, provenance, rollback sûr.
- OCP restricted/SCC adéquate, non-root, rootfs read-only si compatible, seccomp/capabilities minimales.
- Données : minimisation et classification (IBAN, bénéficiaire, identités, tokens, payload ISO), masquage des traces, chiffrement at-rest/in-transit et archives protégées.
- Separation of duties : opérateurs, investigations financières et administrateurs base ; double contrôle sur corrections financières.
- DORA : BIA, registre des prestataires ICT critiques/importants le cas échéant, plan incidents, tests de continuité, licences/support et plan de sortie.
- RGPD : finalités, conservation, accès et purge documentés ; éviter de répliquer inutilement les données personnelles dans tous les topics.

### Tableau de contrôle de flux
Pour **chaque** flux documenter \`source / destination / protocole / identité / droits / chiffrement / données / timeout / retry / transformation / journaux / incident / propriétaire\`. Utiliser cette matrice comme critère de revue de sécurité avant exposé réseau.

---

## 20. Observabilité, investigations et réconciliation

### Quatre vues
1. **Infrastructure** : cluster, pods, quorum DB, queue managers, partitions Kafka, latence des disques, certificats.
2. **Application** : erreurs, timeouts, Circuit Breakers, pools, saturation, Outbox age, queues depth, consumer lag.
3. **Métier** : ordres reçus, contrôlés, soumis, réglés, rejetés, non confirmés, en dépassement de deadline ; histogrammes par rail.
4. **Financière** : écritures core vs règlement CSM/TIPS vs journal moteur vs comptabilité, écarts et dossiers ouverts.

### Indicateurs et actions
| Signal | Action |
|---|---|
| \`payment_confirmation_missing_age\` | Investigation urgente, aucun retry autonome |
| \`outbox_oldest_age\` | Examiner relais, broker, deadline des commandes |
| \`mq_oldest_message_age\` | Quarantaine des commandes expirées et contrôle de capacité |
| \`kafka_consumer_lag\` | Scaling/traitement/backpressure selon rétention |
| \`reconciliation_open_critical\` | Escalade financier + preuve |
| \`owner_epoch_conflict\` | Bloquer écritures de la partition et lancer procédure fencing |
| \`core_duplicate_rejection_count\` | Vérifier la raison et l'idempotence, sans désactiver filtre |
| \`cert_expires_in\` | Rotation avant rupture de sessions externes |

### Réconciliation continue et périodique
Rapprocher identifiants de canaux, état du moteur, références core, messages de place, preuve de règlement et comptabilité. Scénarios : émission non confirmée, règlement sans mise à jour locale, débit sans preuve CSM, crédit duplicate, restauration suivi d'une confirmation tardive, notification absente.

~~~mermaid
flowchart TB
  A["Écart détecté"]
  B["Geler toute réémission financière risquée"]
  C["Collecter preuves canal, core, rail, moteur"]
  D{"Preuve autoritative suffisante ?"}
  E["Transition légale/métier + événement Outbox"]
  F["Investigation manuelle et escalade"]
  G["Journal / double validation si écriture correctrice"]
  A --> B --> C --> D
  D -->|Oui| E --> G
  D -->|Non| F --> G
~~~

**Ne jamais** forcer l'état \`SETTLED\` uniquement pour rétablir un dashboard vert. Les corrections de compte ont une référence propre et une autorisation contrôlée.

---

## 21. Livraison, migration progressive et retour arrière

### Strangler Fig plutôt que big bang
1. **AS-IS prouvé** : répertorier moteur existant, comptes, identité, réseau, CSM, contrats d'éditeurs, dépendances, interfaces et états. Ne pas inférer la topologie BPCE/BIP/FIS à partir de sources publiques.
2. **Fit-gap / buy vs build** : conserver le moteur et moderniser l'intégration si supportable ; conteneuriser seulement avec certification et support explicites, ou développer capacités manquantes si ROI/risk approuvés.
3. **Socle** : OpenShift, identité, réseau, GitOps, certificats, secrets, DB/MQ/Kafka uniquement selon arbitrages.
4. **Simulateur / tests contrats** : core sandbox, schémas ISO, retours de rail, duplications, outbox et timing.
5. **Shadow mode** : comparer règles et traitements avec l'existant **sans émettre d'ordre ni crédit en double**.
6. **Pilote** : faible périmètre/volumétrie, une route/entité, contrôle de RPO/RTO/latence, preuves d'observabilité.
7. **Bascule** : arrêter admission sur tranche, drainer, figer ownership, rapprocher ordres en vol, transférer et rouvrir progressivement.
8. **Extension** : montée en charge contrôlée avec canary, admission gates, retour arrière de code **sans réémettre** les ordres ni annuler les règlements.
9. **Décommissionnement** : retirer l'existant après preuve des invariants, historisation, audit et plan de support.

### GitOps/CI-CD
Build → tests unitaires/contract → SAST/SCA → SBOM → signature → politique admission → test intégration → chaos/performance → approbation → déploiement GitOps progressif → contrôles métier. Versionner ensemble API, événements, DB, copybooks et mapping ISO ; utiliser migrations **expand–migrate–contract** ; ne pas déclencher des migrations bloquantes au démarrage de tous les Pods.

### Limite du rollback
Le rollback d'une image OpenShift **ne** corrige **pas** un mouvement bancaire irrévocable déjà effectué. Prévoir compatibilité des messages en vol entre anciennes/nouvelles versions.

---

## 22. Catalogue d'incidents et tests d'acceptation

| ID | Injection de panne | Résultat attendu | Preuve requise |
|---|---|---|---|
| P01 | Double clic POST canal | 1 intention | UNIQUE + même paymentId |
| P02 | Deux POST concurrents vers 2 Pods | 1 seul ordre | Transaction DB et même référence |
| P03 | Même clé, bénéficiaire/montant différent | Conflit, aucun changement | HTTP + DB |
| P04 | Crash après commit DB avant publication | Outbox reprend | Recovery + traces |
| P05 | Crash publisher après envoi avant ACK | Re-publication admise, 0 double effet | eventId / core |
| P06 | Crash consumer MQ après effet core avant ACK | Redélivrance sans deuxième débit | Core Operation ID |
| P07 | Réponse core perdue après réservation | Retrouver réservation par réf | Core status |
| P08 | Confirmation de règlement perdue | UNKNOWN puis réconciliation, pas de retry indépendant | Rail/core evidences |
| P09 | Ordre MQ livré après deadline | Pas d'exécution aveugle | Horodatages + décision |
| P10 | Réponse positive tardive après restauration | Processus spécifique d'investigation/régularisation | Procédure EPC/PSP |
| P11 | Notification KO après SETTLED | Retenter uniquement notification | Pas de mouvement core |
| P12 | Double événement Kafka | Une seule projection logique | Inbox + séquence |
| P13 | Kafka perdu 1 h | Paiements continuent si Kafka hors critique | Outbox + publication tardive |
| P14 | MQ indisponible pendant la fenêtre SCT Inst | Admission/erreur/expiration conforme, pas de retard exécuté | Règles + délais |
| P15 | Fraude indisponible | Décision risque explicitement approuvée, pas fail-open arbitraire | Logs policy |
| P16 | Perte d'un Pod DB primaire | Quorum, état commit reconstitué | HA tests |
| P17 | Perte d'une zone | Pas de perte silencieuse reconnue | RPO zone |
| P18 | Perte complète d'un site | Fencing, promotion et réconciliation | PRA signé |
| P19 | Partition inter-site (split-brain) | Jamais deux écrivains sur une partition | ownerEpoch + core |
| P20 | Retard réplication inter-site après commit | Réadmission différée si données incomplètes | Journaux de commit |
| P21 | Corruption logique répliquée | Sauvegarde indépendante + restauration contrôlée | PITR restore |
| P22 | Rail STET indisponible après envoi incertain | Aucun basculement aveugle vers TIPS | Query status |
| P23 | Certificat TLS expiré sous charge | Échec contrôlé et alerte + rotation | PKI/SRE |
| P24 | Montée à charge crête + panne de zone | Respect admission et stabilité ; aucune duplication | Perf/Chaos |
| P25 | Nouvelle version de contrat ISO incompatible | Refus/quarantaine sans mouvement | Contract tests |
| P26 | AuthZ objet violée par un autre client | Accès rejeté et audité | API tests |
| P27 | Callback avec ordre de transitions inversé | Pas de régression financière d'état | stateVersion |
| P28 | Failback d'un site rétabli | Pas de deuxième propriétaire | Fencing et runbook |

### Critères « GO » de qualification
- Tous les **invariants INV-01 à INV-12** couverts par tests et preuves, avec interface core ou simulateur explicitement limité.
- Procédure SCT Inst validée par conformité/PSP/rail, y compris 5/7/9/10 s, absence de confirmation et confirmation tardive.
- Essais de split-brain et **perte de site après acquittement durable**, avant toute assertion RPO 0.
- SLO/SLI p99 sous charge, latence réseau réelle, pipeline de rotation certificats et alertes de réconciliation.
- RTO/RPO contractuels, plans de secours et runbooks réellement exercés.
- Aucun blocage P0 de sécurité, de fraude, de réglementation ou de support éditeur.

---

## 23. Matrice des patterns et ADR à faire signer

### Patterns combinés
| Pattern | Rôle dans la cible | Propriété déterminante |
|---|---|---|
| Request/Response | API d'intention et lecture statut | Temps d'attente borné |
| Messaging/Queue | Commande vers legacy si applicable | Transport durable, pas effet financier |
| Pub/Sub | Plusieurs consommateurs d'événements | Pas de dépendance directe aux abonnés |
| EDA | Réactions aux faits métier | Gouvernance des transitions |
| Event Streaming | Analytics/rejeu d'événements validés | Rétention, partition, lag |
| API Gateway | Point d'entrée sécurisé et routage | Pas de décision financière métier |
| Adapter/ACL | Traduction legacy et sémantique | ACCEPTED ≠ SETTLED |
| Saga | Coordination/compensation réversible | Pivot irréversible et état durable |
| Circuit Breaker | Couper appels à service malade | Ne stocke pas de commandes |
| Retry/Timeout/Idempotency | Reprise maîtrisée | Outcome inconnu ≠ échec |
| Transactional Outbox | Commit état + message sortant | Publication peut se répéter |
| Idempotent Consumer | Redélivrance sans double effet | Référence financière stable |
| Reconciliation | Résolution issue inconnue | Source financière autoritative |
| Bulkhead | Ressources isolées par dépendance | Protection saturation/pannes |

### Registre ADR
| ADR | Proposition retenue comme base | Alternative / condition |
|---|---|---|
| ADR-01 | Core autoritatif pour écritures/provision | Moteur à solde local **écarté sans** garantie comptable formalisée |
| ADR-02 | Unicité d'intention API **et** core | Clé HTTP seule insuffisante |
| ADR-03 | Outbox + Inbox / Idempotent Consumer | XA à évaluer uniquement si support complet démontré |
| ADR-04 | Orchestration durable compacte | Moteur existant prioritaire si fonctions conformes |
| ADR-05 | Commands vs events séparés | Un broker unique autorisé si besoins satisfaits |
| ADR-06 | Routage rail sans fallback aveugle | Multi-rail seulement après preuve d'exclusivité |
| ADR-07 | Writer exclusif par partition | Multi-writer seulement avec DB/core offrant garanties adéquates |
| ADR-08 | DR conditionnée par fencing et données | Réplication async seule **non suffisante** à RPO 0 |
| ADR-09 | Statuts paiement / compte / investigation distincts | Etat binaire SUCCESS/FAILED écarté |
| ADR-10 | Deadline réglementaire propagée | Retry au-delà deadline proscrit |
| ADR-11 | Retours post-commit + reporting découplé | Ne pas coupler notification au settlement |
| ADR-12 | Buy vs Build/FIS ouvert jusqu'au fit-gap | Aucune réécriture imposée avant audit/support |
| ADR-13 | VoP avant autorisation, avec preuve | Pas de VoP insérée tardivement sous T0 sans analyse |
| ADR-14 | Capacité/latences basées sur charge réelle | TPS et p99 illustratifs non contractuels |

**Format d'approbation :** owner fonctionnel + owner technique, options, impacts, risques, coûts/licences, tests, support, date, approbateur Design Authority et conditions de révision. Ici, ces ADR sont **candidates**, pas signées.

---

## 24. Coûts, FinOps/GreenOps et exploitation

### Coût complet
CapEx/OpEx OpenShift, stockage, base, HA/DR, brokers, interconnexion et liens CSM, moteur/licences, sécurité/HSM, PKI, API Management, instrumentation, tests, certification, astreinte et support éditeur. Comptabiliser la capacité réservée sur le second site et les répétitions de stockage de l'observabilité.

### Indicateurs
- Coût par paiement **réglé** et par paiement **traité** ; distinguer les deux dénominateurs.
- Coût de la haute disponibilité et du niveau RPO/RTO choisi.
- Émissions CO2 relatives mesurées et ressources sous-utilisées (CPU/RAM, volumes logs), sans dégrader les objectifs réglementaires.
- Licences supportées pour toutes les versions de Java, OCP, MQ, Kafka, base et moteur ; inclure coûts du PRA et certifications.
- En non-production, politique d'arrêt/parkage si compatible ; en production, dimensionnement et reprise d'abord.

### Gouvernance opérationnelle
Runbook par alerte, rotations d'astreinte, ownership par domaine, revues d'écart, exercices chaos réguliers, post-mortem, pistes d'audit, plan de mise à jour de schémas et certificats. Le progrès est mesuré en **absence de perte/double mouvement, délai de résolution des états inconnus et service réellement offert au client**, pas seulement en Pods « Running ».

---

## 25. Questions bloquantes et conditions de validation

**L'étude est une base de conception. Les réponses ci-dessous nécessitent des preuves clients/éditeurs/banque avant décision définitive.**

| Domaine | Question à résoudre | Artefact/proof attendu |
|---|---|---|
| Métier | Quel(s) PSP, entités, canaux, flows et rails sont concernés ? | Process map et responsabilités PSP/CSM |
| Core | Qui garantit réservation, débit/crédit, idempotence, statut ? | Contrat/API, tests, écritures probantes |
| Existant | Quels composants BIP/FIS/PARME/ABS et interfaces sont réels ? | Inventaire AS-IS, schémas et versions |
| Buy vs Build | Peut-on exploiter FIS OPF/legacy sur OpenShift avec support ? | Matrice éditeur certifiée + licences |
| Volume | TPS moyen/pointe, burst, montants, messages en vol ? | Mesures de production anonymisées |
| Latence | Temps de réponse core/VoP/fraude/rail p99, extrêmes ? | Traces distribuées et campagnes de charge |
| Réglementaire | Pratiques d'application 5/7/9/10 s et cas exceptionnels ? | Validation juridique/PSP et CSM |
| Données | Quelle autorité d'écriture, granularité de partition et failover ? | Design transactionnel + fencing tests |
| DR | Distance/latence intersite, réplication, quorum, RTO/RPO par périmètre ? | BIA + PRA preuve |
| Routing | Participation/joignabilité/lien et exclusivité inter-rails ? | Contrats STET/TIPS/RT1 + test |
| Intégration | MQ ou Kafka requis ? Quelles versions et schémas ? | Inventaire, support, coûts et modèles de panne |
| Sécurité | PKI, HSM, IAM, habilitations objets, séparation des fonctions ? | Dossier sécurité validé |
| Exploitation | 24/7, supervision, investigation et correction comptable ? | RACI, runbooks et preuve d'exercice |
| Données perso | Quelles durées et restrictions par type de journal ? | ROPA/rétention RGPD |
| Migration | Comment empêcher double émission lors du shadow/canary ? | Cutover plan + tests |

### Classification de maturité
- **Établi** : principes généraux et textes EPC/UE/BCE cités.
- **Proposé** : composants Java/OpenShift, choix de brokers, RTO/RPO, budgets et découpage ; soumis à arbitrage.
- **Non validé** : architecture et produits internes des organisations mentionnées, support FIS, contrats des rails, volumes réels, cohérence multisite en production.

**Critère de clôture architecture :** dossier HLD+LLD approuvé, ADR signées, contrats testés, invariants prouvés, performances et PRA exercés, conformité d'exécution validée, support éditeur confirmé et exploitation financière prête.

---

## 26. Références publiques et terminologie

### Réglementation et schemes (consultés le 18/10/2026)
1. **EPC — SCT Inst rulebook courant, version 2025 v1.2 (30/09/2026)** : https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-instant-credit-transfer-sct-inst/sepa-instant-credit-transfer
2. **EPC — détail version 1.2** : https://www.europeanpaymentscouncil.eu/document-library/rulebooks/2025-sepa-instant-credit-transfer-rulebook-version-1-2
3. **UE — Règlement (UE) 2024/886, VoP et sanctions ciblées** : https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32024R0886
4. **EPC — VoP rulebook courant** : https://www.europeanpaymentscouncil.eu/document-library/rulebooks/verification-payee-scheme-rulebook-0
5. **EPC — FAQ : VoP avant autorisation** : https://www.europeanpaymentscouncil.eu/faq/verification-payee-scheme/rulebook/are-psp-allowed-send-vop-requests-when-intention-pay
6. **BCE — TIPS, règlement final et irrévocable en monnaie de banque centrale** : https://www.ecb.europa.eu/paym/target/tips/html/index.es.html
7. **EBA — DORA** : https://www.eba.europa.eu/activities/direct-supervision-and-oversight/digital-operational-resilience-act

### Architecture et patterns
8. Transactional Outbox : https://microservices.io/patterns/data/transactional-outbox.html
9. Idempotent Consumer : https://microservices.io/patterns/communication-style/idempotent-consumer.html
10. Saga : https://microservices.io/patterns/data/saga.html
11. Anti-Corruption Layer : https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer
12. Resilience4j : https://resilience4j.readme.io/docs/circuitbreaker
13. OWASP API Security Top 10 : https://owasp.org/API-Security/editions/2023/en/0x11-t10/
14. OpenID Connect : https://openid.net/specs/openid-connect-core-1_0.html

### Définitions
- **PSP** : prestataire de services de paiement.
- **CSM** : clearing and settlement mechanism.
- **VoP** : Verification of Payee.
- **SCT Inst** : SEPA Instant Credit Transfer.
- **SCA** : Strong Customer Authentication.
- **RPO/RTO** : perte de données maximale / délai de reprise.
- **Fencing** : mécanisme empêchant un ancien propriétaire d'écrire après bascule.
- **Outbox/Inbox** : enregistrement durable d'événements sortants / contrôle de déduplication entrant.
- **Autorité financière** : système qui fait foi pour les mouvements sur compte ou la preuve de règlement.

**Copyright © 2026 Zidane Djamal. Tous droits réservés.** Ce travail d'architecture est original ; les marques, standards et publications restent la propriété de leurs titulaires. Aucun contenu interne confidentiel des établissements cités n'est repris ni prétendu vérifié.
