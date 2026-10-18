# 08 — Saga : coordonner des transactions distribuées

## Problème
Un parcours métier combine des transactions dans plusieurs services et bases : contrôle, réservation de fonds, décision fraude, transmission et notification. Aucun ROLLBACK SQL global ne couvre nécessairement ces systèmes. Une **Saga** coordonne des transactions locales et les compensations métier *possibles*.

## Deux familles
- **Orchestration** : un composant pilote étapes, délais, retries, statuts et compensations. Recommandée comme hypothèse pour un flux complexe très audité, à condition de rendre l'état durable et l'orchestrateur hautement disponible.
- **Chorégraphie** : chaque composant réagit à un événement et émet le suivant. Découplage organisationnel, mais compréhension des chemins d'échec plus complexe à grande échelle.

~~~mermaid
flowchart TD
  A["PaymentRequested"]
  S["Saga durable / orchestrateur"]
  C["Vérification des règles"]
  F["Réserver les fonds"]
  D{"Contrôle fraude OK ?"}
  E["Soumettre au cœur bancaire"]
  X["Compensation : libérer les fonds"]
  R["PaymentRejected"]
  W["Attendre confirmation / réconcilier"]
  K["PaymentSettled"]
  A --> S --> C --> F --> D
  D -->|Non| X --> R
  D -->|Oui| E --> W --> K
~~~

## Point décisif : irréversibilité
Une **réservation de fonds** peut être libérée. Un ordre irrévocablement réglé **ne peut pas être annulé par un simple rollback Saga**. Des procédures de retour/rappel peuvent exister selon le schéma, sans succès garanti. Le *pivot transaction* est l'étape après laquelle les compensations usuelles ne restaurent plus l'état initial : la définir avec le métier et les règles du système d'exécution.

## Saga : état durable
Chaque saga suit sagaId, paymentId, currentStep, stateVersion, businessDeadline, createdAt, lastTransitionAt, retryBudget, correlationId. Protéger les transitions par **optimistic locking** / machine à états. Éviter qu'un message en retard fasse revenir SETTLED vers PROCESSING.

Exemples d'états : RECEIVED → VALIDATING → FUNDS_RESERVED → SUBMITTED → (SETTLED | REJECTED | UNKNOWN/TO_RECONCILE). Le caractère réversible/irréversible dépend de la vraie définition métier des opérations et du schéma SEPA choisi.

## Orchestration : séquence de compensation
~~~mermaid
sequenceDiagram
  participant O as Orchestrateur
  participant F as Fonds
  participant R as Risque
  O->>F: ReserveFunds(paymentId)
  F-->>O: FundsReserved
  O->>R: AssessRisk(paymentId)
  R-->>O: Rejected
  O->>F: ReleaseFunds(same reservationId)
  F-->>O: FundsReleased
  O->>O: REJECTED + événement durable
~~~

## Échecs à traiter
| Moment de panne | Décision |
|---|---|
| Avant toute écriture | Reprise depuis la commande initiale |
| Après réservation, fraude refusée | Compensation idempotente de réservation |
| Après commande au cœur, réponse perdue | UNKNOWN, interrogation / rapprochement, pas de double exécution |
| Après règlement, notification KO | Rejouer notification, ne pas annuler le paiement |
| Compensation elle-même KO | Persister échec, retry borné, intervention/reconciliation |
| Deux orchestrateurs sur même saga | Lock/version/fencing pour éviter transitions concurrentes |

## Contraintes paiement instantané
Le schéma SCT Inst et le cadre UE imposent un parcours rapide et une deadline métier ; la Saga ne doit pas insérer des délais arbitraires. Si l'ordre atteint le délai sans confirmation, suivre les obligations de remise à disposition/notification et la gestion de confirmations tardives du rulebook applicable. Distinguer le temps de traitement technique du temps réglementaire. Source EPC : [SCT Inst Rulebook](https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-instant-credit-transfer-sct-inst/sepa-instant-credit-transfer).

## Choix de plateforme
Java/Spring + état PostgreSQL + Outbox + messagerie MQ en option ; ou moteur de workflow durable. Le langage et le broker n'apportent pas intrinsèquement la cohérence financière ; la preuve vient des invariants, états, erreurs et tests.

## Checklist et entretien
- Qui est propriétaire de l'état Saga ?
- Quelles étapes ont une compensation *sûre*, lesquelles sont irréversibles ?
- Comment empêcher une exécution tardive après deadline ?
- Comment reprendre après crash entre traitement métier et ACK broker ?
- **Q : saga = transaction ACID distribuée ?** Non. **Q : une Saga sait-elle annuler un SCT Inst réglé ?** Non.
- **Q : quand préférer orchestration ?** Processus multi-étapes réglementé nécessitant audit et coordination des compensations.

Référence : [microservices.io — Saga](https://microservices.io/patterns/data/saga.html).
