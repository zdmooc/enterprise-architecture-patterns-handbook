# Cours 05 — Enterprise Flow Mapping / Cartographie des flux inter-SI
**Niveau :** Architecture d'entreprise / intégration | **Progression :** QCM B validé | [Fiche canonique](../05-enterprise-flow-mapping/README.md)

## Objectifs
Cartographier les **échanges** avec émetteur, destinataire, sémantique, format, SLA, sécurité, débit, reprise et preuve. Expliquer la différence entre API synchrone, commande IBM MQ et événement Kafka, et traiter les issues inconnues.

## 1. Parcours du virement fictif de 500 EUR
L'ordre VIR-001 est initié via une API. Le moteur valide et enregistre durablement l'intention ; une commande est transmise vers le Core Banking par MQ et une fois l'état confirmé, des faits métier sont diffusés vers les abonnés Kafka.

~~~mermaid
flowchart TB
  UI["Mobile"] -->|"F01 HTTPS + idempotency key"| API["Payment API"]
  API -->|"F02 appel métier"| M["Moteur Java"]
  M -->|"F03 vérification"| R["Contrôles / risque"]
  M -->|"F04 tx ordre + outbox"| DB[("PostgreSQL")]
  DB --> REL["Outbox relay"]
  REL -->|"F05 PUT persistent"| Q["IBM MQ - commande"]
  Q -->|"F06 livraison"| AD["Adaptateur Core"]
  AD <--> CORE["Core Banking"]
  CORE <--> SEPA["Passerelle / Rail SEPA"]
  AD -->|"F07 réponse MQ"| M
  DB --> EVT["Outbox relay événements"]
  EVT -->|"F08 publish"| K["Kafka"]
  K -->|"F09 consommation"| N["Notifications et reporting"]
~~~

## 2. Catalogue des flux (extrait)
| ID | Source → cible | Contrat logique | Nature / preuve nécessaire |
|---|---|---|---|
| F01 | Mobile → API | CreatePayment + idem-key | HTTPS ; réponse = réception/intention, pas règlement |
| F02 | API → Moteur | SubmitIntent | Interne ; référence immuable VIR-001 |
| F03 | Moteur → Risque | AssessPayment | Décision validée / indéterminée |
| F04 | Moteur → PostgreSQL | Intention + outbox | Commit DB atomique |
| F05 | Relay → MQ | Execute(VIR-001, échéance) | ACK MQ = transport uniquement |
| F06 | MQ → Adaptateur/Core | Instruction versionnée | Déduplication, échéance et effet autoritatif |
| F07 | Core → Moteur | PaymentResult | Statut métier corrélé, enregistré durablement |
| F08 | DB → Kafka | PaymentSettled / Rejected | Événement après état attesté |
| F09 | Kafka → abonné | StatusChanged | Notification/rejeu, sans commande de re-débit |

Décrire aussi la **route physique**, les ACL, certificats, classification, volumes nominaux/de pointe, pics, SLO, propriétaires et preuves. Ne jamais déduire un accord métier d'un simple OK transport.

## 3. Séquence avec réponse perdue
~~~mermaid
sequenceDiagram
  actor C as Client
  participant A as Payment API
  participant Q as IBM MQ
  participant B as Core Banking
  participant R as Reconciliation
  C->>A: Virement 500 EUR / idem PAY-001
  A->>Q: Execute VIR-001 via outbox durable
  Q->>B: Commande VIR-001
  B->>B: Traiter avec unicité + échéance
  B--xA: Réponse perdue
  A-->>C: Statut UNKNOWN / en rapprochement
  C->>A: Réessai PAY-001 même contenu
  A-->>C: Même paiement VIR-001
  R->>B: QueryStatus(VIR-001)
  B-->>R: Preuve métier autoritative
  R->>A: Transition justifiée
~~~

## 4. Trois garanties différentes
1. **ACK HTTP** : service contacté et contrat de réponse exécuté ; ne prouve pas le règlement.
2. **ACK MQ / commit transport** : broker a accepté/persisté un message selon configuration ; ne prouve pas un débit.
3. **Confirmation métier** : statut obtenu du Core/rail autoritatif et corrélé à la référence.

**Idempotence :** conserver une identité de commande et contrôler l'unicité jusqu'à la transaction qui effectue le mouvement. La clé de requête HTTP seule est insuffisante.

**Réconciliation :** après timeout, conserver UNKNOWN, interroger une source autoritative, comparer références et écritures puis enregistrer seulement une transition attestée. Une réémission aveugle avec un nouvel ID expose au double débit.

## 5. MQ ou Kafka ? Comparaison contextuelle
| Besoin | MQ | Kafka |
|---|---|---|
| Travail commandé, consommateur identifié | Files et request/reply adaptés | Possible avec conception spécifique |
| Diffuser événements aux abonnés indépendants | Pub/Sub possible | Topics / consumer groups adaptés |
| Relecture historique sous rétention | Gestion applicative des messages consommés | Offsets et rétention |
| Effet financier exactly once externe | **Non garanti seul** | **Non garanti seul** |

La coexistence peut être rationnelle : **MQ pour commandes legacy, Kafka pour diffusion dérivée**. Elle a un coût d'exploitation à évaluer.

## 6. Pannes et vérifications
- Consumer MQ arrêté : messages conservés si configurés durables ; surveiller profondeur/ancienneté, délai d'ordre et reprise admissible.
- Crash entre effet Core et ACK : redélivrance possible ; vérifier unicité dans Core.
- Échec de publication Kafka : Outbox à rejouer ; ne pas refaire le règlement.
- Message empoisonné : quarantaine contrôlée, BOQ/DLQ selon responsabilité ; procédure de reprise métier.
- Dérive de schéma : contrat/version/schéma incompatibles détectés avant production.

## 7. Livrables d'intégration
Matrice des flux avec identifiants ; diagrammes logique/physique ; contrats API/MQ/événements ; champs de corrélation ; modèle de statuts ; matrice de panne ; exigences de sécurité et capacité ; owners ; ADRs.

## 8. Exercice corrigé
**Incident :** 500 EUR réglés, réponse perdue. (A) nouveau paiement avec nouvel identifiant, (B) conserver VIR-001, vérifier le statut auprès de Core et réconcilier, (C) publier SETTLED sur Kafka sans preuve.

**Correction : B.** Le timeout n'est pas un rejet ; l'autorité financière tranche. A crée un risque de double exécution ; C diffuse un état inventé.

## 9. Questions d'entretien
- **Pourquoi ne pas publier SETTLED après un PUT MQ ?** Parce que MQ confirme le transport, pas le règlement.
- **Comment auditer les flux ?** Contrat, version, propriété, corrélation, donnée, droits, mesures et preuve de test.
- **Que change le SCT Inst ?** Les échéances métier rendent dangereuse la reprise tardive et imposent la gestion stricte des statuts selon le scheme.

---

## Cadre et limites
Architecture pédagogique **fictive et anonymisée**, non description d'une banque réelle ni preuve de production. Tous les débits, chiffres, fichiers, indicateurs et interfaces sont illustratifs. Toute décision réelle demande inventaire, approbation métier, analyse de risque, vérification réglementaire et tests. Un accusé HTTP, MQ ou Kafka ne prouve jamais à lui seul le règlement ; l'idempotence doit couvrir l'effet financier et une échéance expirée doit être contrôlée avant toute reprise.
