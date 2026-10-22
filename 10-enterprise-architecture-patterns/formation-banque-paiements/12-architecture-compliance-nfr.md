# Cours 12 — Architecture Compliance et NFR Traceability

**Niveau :** Architecture d'entreprise / qualité et assurance d'architecture | **Parcours :** fiche disponible, exercice de validation à faire | [Pattern canonique 12](../12-architecture-compliance-nfr/README.md)

> Étude **fictive et anonymisée** de paiements bancaires. Aucun chiffre de performance n'est une mesure client ni une attestation de conformité réelle. Les obligations précises du rail SEPA/SCT Inst, du droit applicable et des normes doivent être évaluées par les responsables compétents.

## Compétences visées
1. Traduire un besoin métier en une **exigence non fonctionnelle vérifiable** (NFR).
2. Relier chaque NFR à un composant, une décision d'architecture, un propriétaire, un protocole d'essai et une preuve datée.
3. Distinguer **conformité documentaire**, **conformité de conception** et **validation au runtime**.
4. Préparer une revue GO/NO-GO d'une plateforme de paiement Java/OpenShift dépendant de MQ, Kafka et Core Banking.

## 1. Quel problème résout ce pattern ?
Un diagramme peut montrer trois pods OpenShift, IBM MQ HA et Kafka répliqué. Cela ne prouve pas que les virements aboutissent dans les délais, qu'aucun double débit n'est possible, que les secrets sont protégés ou qu'un incident intersite ne provoque pas de statuts faux.

**Architecture Compliance** : contrôler le respect des principes et décisions acceptés.  
**NFR Traceability** : relier les caractéristiques de qualité (disponibilité, latence, sécurité, capacité, reprise, traçabilité, coût, maintenabilité) aux décisions, tests et résultats.

## 2. Chaîne de preuve
~~~mermaid
flowchart LR
  B["Besoin métier"] --> N["NFR mesurable / invariant"]
  N --> A["Décision architecture / ADR"]
  A --> T["Protocole de test"]
  T --> P["Mesures, logs et preuves datées"]
  P --> G{"Conforme au seuil approuvé ?"}
  G -->|Oui| OK["GO sous autres contrôles"]
  G -->|Non| NO["Écart et NO-GO ou dérogation habilitée"]
~~~

### 3. Matrice de traçabilité NFR d'une banque fictive
| NFR / invariant | Justification métier | Méthode de qualification | Responsable |
|---|---|---|---|
| Latence de bout en bout | Délai du rail de paiement applicable | Injecter charges réalistes ; mesurer p95/p99, délai total et expiration | Owner Paiements + Performance |
| Unicité de l'effet financier | Aucune double exécution du même ordre | Retransmettre, crash après commit Core, appels concurrents ; rapprocher les écritures | Core Banking + Paiements |
| Disponibilité du parcours | Paiement continu malgré panne définie | Perte pod/nœud/zone, broker et Core ; mesurer succès métier, pas seulement healthcheck | SRE + owners métier |
| RPO et RTO | Continuité selon BIA approuvée | Test de restauration réelle DB, brokers et références en cours ; mesurer pertes et délais | PRA / Risques / Exploitation |
| Sécurité des accès | Seuls les acteurs autorisés peuvent initier et consulter | Tests identité, scopes, contrôle d'objet, certificats, secrets, refus et audit | Sécurité + Métier |
| Traçabilité | Résoudre les états UNKNOWN | Corréler paymentId, messageId, correlationId, preuves et changements d'état | Paiements + Observabilité |
| Intégrité des événements | Suivi/reporting fiable | Crash publication, duplicate event, replay, lag, schéma incompatible | Data/Intégration |
| Exploitabilité | Réagir avant rupture métier | Alarmes, dashboards, runbooks, test de garde, seuils et propriété | Exploitation |
| Coûts et support | Transformation durable et supportable | TCO incl. dual-run, licences et support de Java/JMS/DB/Kafka/OpenShift | Finance / Architecture |

**Important :** les seuils de p99, RPO/RTO, volumétrie de pointe et budget d'erreur ne doivent pas être devinés. Ils proviennent des besoins métier, engagements, BIA et obligations applicables.

## 4. Exemples de NFR correctement formulées
**Vague :** « le système sera hautement disponible ».  
**Mesurable :** « pour le scénario de perte d'un nœud de la zone Z, lors d'une charge représentative définie, le taux de paiements aboutissant à un statut autoritatif et le temps de reprise restent dans les seuils validés dans la fiche NFR-PAY-HA-01. »

**Vague :** « les messages sont fiables ».  
**Mesurable :** « après crash du consommateur avant ACK MQ, deux livraisons du même paymentId n'entraînent qu'un seul effet financier attesté dans le Core ; la réponse ambiguë est réconciliée. »

**Vague :** « Kafka est tolérant aux pannes ».  
**Mesurable :** « en cas d'arrêt d'un broker Kafka pendant publication, l'Outbox conserve les événements non confirmés et la diffusion reprend sans inventer de statut SETTLED ni relancer une commande financière. »

## 5. Scénario d'architecture et chaîne d'incident
~~~mermaid
sequenceDiagram
  actor U as Client
  participant P as Payment API - OpenShift
  participant D as DB / Outbox
  participant Q as IBM MQ
  participant C as Core Banking
  participant K as Kafka
  U->>P: Virement de 500 EUR / idempotency key
  P->>D: Intention durable VIR-001
  D->>Q: Commande via relay
  Q->>C: Execute VIR-001
  C->>C: Vérification unicité et effet
  C--xP: Réponse perdue
  P->>D: UNKNOWN / TO_RECONCILE
  P->>C: QueryStatus VIR-001 (via contrat adapté)
  C-->>P: Résultat financier attesté
  P->>D: Statut durable + Outbox event
  D->>K: Fait métier diffusé
~~~
Le schéma expose une trajectoire logique ; les transactions multi-ressources et routes physiques doivent faire l'objet de contrats explicites.

## 6. Gouverner les écarts
- **NFR P0 non mesurée** : pas de GO tacite. Organiser test ou documenter un NO-GO ; une dérogation n'est possible que si le risque est explicitement accepté par l'autorité compétente et reste compatible avec les obligations incontournables.
- **Test nominal vert, reprise KO** : l'exigence « résilience » n'est pas satisfaite ; empêcher la bascule concernée.
- **Pod Running, API métier en erreur** : le check technique ne prouve pas la santé du service ; ajouter une sonde et un indicateur métier.
- **Écart sécurité critique** : formaliser action, responsable, date, contrôle compensatoire si autorisé, et preuve de fermeture.
- **Contrôle passé sur environnement de test seulement** : ne jamais marquer « client production validé » sans evidence de ce périmètre.

## 7. Fiche de conformité type
~~~text
NFR-ID : NFR-PAY-001
Capacité / processus métier :
Source de l'exigence :
Sévérité : P0 / P1 / P2
Critère observable et formule :
Périmètre de test, charge, durée, état des données :
Valeur cible approuvée / valeur mesurée :
Composants et flux concernés :
ADR / ABB / SBB correspondants :
Owner métier / IT / responsable du test :
Preuve : rapport, traces et horodatage :
Résultat : PASS / FAIL / NOT_TESTED
Écart et mitigation :
Décision GO / NO-GO et signataires :
Date de réexamen :
~~~

## 8. Pratiques OpenShift, MQ et Kafka à qualifier
- **OpenShift** : non-root, quotas, SCC, NetworkPolicy, probes, shutdown gracieux, ressources dimensionnées, déploiement GitOps, secrets et audit.
- **Java/JEE** : runtime/JNDI/JDBC/JMS/JTA-XA compatibles et supportés ; transactions et traitements en vol testés.
- **IBM MQ** : durabilité, queues, canaux, DLQ/BOQ, TLS/ACL, profondeur, âge des messages et fin d'échéance.
- **Kafka** : schémas versionnés, partitionnement, rétention, lag, sécurité, reprise depuis Outbox.
- **Core Banking** : capacité réelle, idempotence financière, statuts, délais, rapprochement, gestion des indisponibilités.
- **Transversal** : HA/PRA multi-composants, charge nominale et de pointe, coût de cohabitation, support éditeur.

## 9. Livrables
Registre des NFR et sources ; matrice exigence↔ADR↔composant↔test↔preuve ; cahier des tests nominaux et chaos autorisés ; rapport de conformité ; registre d'écarts/dérogations ; décisions GO/NO-GO ; backlog de remédiation.

## 10. Exercice corrigé (essayer avant lecture)
**Cas :** trois réplicas Java/OpenShift sont Running. La banque n'a pas testé la panne MQ, le Core Banking ni la redélivrance financière. Un chef de projet annonce que la plateforme est hautement disponible.

A. Valider : les pods sont Running.  
B. Prouver la résilience complète par des tests du parcours métier et refuser l'étiquette « conforme » tant que les NFR critiques ne sont pas qualifiées.  
C. Ajouter seulement davantage de pods Java.

**Correction : B.** La disponibilité perçue par le client dépend aussi de la DB, du middleware, des réseaux et du Core. Une propriété technique isolée n'est pas une garantie métier.

## 11. Réponse type en entretien
« Je pars des exigences métier, je les rends mesurables, je les trace vers les décisions et les composants, puis je mène des tests nominaux, de panne et de reprise. Les écarts deviennent des risques assignés et aucun niveau de conformité ne se décrète sur un simple diagramme. »

**Liens :** [Gouvernance ADR](11-architecture-governance-adr.md) · [Dossier de migration Java/JEE](../../09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/migration-playbook.md) · [Atlas incidents](schemas/cutover-et-incidents.md).
