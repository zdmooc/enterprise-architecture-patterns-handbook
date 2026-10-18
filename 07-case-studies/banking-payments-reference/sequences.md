# Séquences — du canal bancaire au résultat financier

## S1 — Parcours nominal, traçable et sans mélange de garanties

~~~mermaid
sequenceDiagram
  autonumber
  actor C as Client
  participant G as API Gateway
  participant A as Payment API
  participant DB as PostgreSQL + Outbox
  participant S as Saga
  participant R as Outbox Relay
  participant MQ as IBM MQ
  participant L as Core Banking + Rail
  participant K as Kafka
  participant N as Notification

  C->>G: POST 500 EUR + Bearer + idem-key PAY-001
  G->>G: AuthN, scopes, quotas
  G->>A: Request corr-001
  A->>DB: TX: INSERT intention VIR-001 + Outbox
  DB-->>A: Commit confirmé
  A-->>C: 202 PROCESSING + VIR-001 (illustratif)
  A->>S: Signal de traitement ou reprise durable
  S->>S: Vérifier contrôles / fonds
  S->>DB: TX: état SUBMISSION_READY + Outbox commande
  DB-->>S: Commit
  R->>DB: Lire commande non publiée
  R->>MQ: PUT persistent Execute(VIR-001) sous syncpoint
  MQ-->>R: Commit transport
  MQ->>L: Délivrer commande identifiée VIR-001
  L->>L: Vérifier échéance et unicité, traiter
  L-->>MQ: PaymentResult(VIR-001, settled/rejected)
  MQ->>S: Via consumer/ACL: réponse métier
  S->>DB: TX: transition durable + Outbox événement
  DB-->>S: Commit
  R->>DB: Lire événement validé
  R->>K: Publish PaymentSettled/Rejected
  K->>N: Abonnement notification
  N-->>C: Résultat métier selon contrat
~~~

**Attention :** le 202 est **un exemple de contrat** ; une solution SCT Inst réelle doit respecter ses obligations de délai et d'information. Le broker n'est pas la preuve de règlement. Les messages entrants passent en réalité par un consommateur qui traite atomiquement déduplication et changement d'état.

## S2 — Panne après exécution, confirmation perdue
~~~mermaid
sequenceDiagram
  actor C as Client
  participant A as Payment API
  participant D as Base intentions
  participant X as Cœur bancaire
  C->>A: POST PAY-001 / 500 EUR
  A->>D: Intention VIR-001 unique
  A->>X: Execute VIR-001 (via MQ)
  X->>X: Règlement effectué
  X--xA: Réponse non reçue
  A->>D: UNKNOWN / TO_RECONCILE
  C->>A: Retry PAY-001, même payload
  A->>D: Lire VIR-001
  A-->>C: Même VIR-001, statut non inventé
  A->>X: QueryPaymentStatus(VIR-001)
  X-->>A: SETTLED (source autoritative)
  A->>D: Enregistrer SETTLED
~~~

## S3 — Compensation avant pivot irréversible
~~~mermaid
sequenceDiagram
  participant S as Saga
  participant F as Fonds
  participant R as Risk Service
  S->>F: ReserveFunds(500 EUR, reservationId)
  F-->>S: FundsReserved
  S->>R: AssessRisk
  R-->>S: Rejected
  S->>F: ReleaseFunds(reservationId)
  F-->>S: FundsReleased
  S->>S: REJECTED + événement fiable
~~~

## S4 — Contrôle d'une commande vieillie
~~~mermaid
sequenceDiagram
  participant O as Relais Outbox
  participant MQ as IBM MQ
  participant C as Cœur bancaire
  O->>MQ: Commande VIR-001, deadlineUtc
  Note over MQ: Service indisponible, message attend
  MQ->>C: Livraison après échéance
  C->>C: Vérifier deadline + statut + règles du rail
  C-->>MQ: Expired/NeedsReconciliation (sans nouvelle exécution aveugle)
~~~

## Corrélation des traces
Conserver paymentId (identifiant métier stable), idempotency-key scoped, sagaId, eventId, messageId, correlationId et causationId. Ne jamais confondre clé d'observabilité et preuve d'exécution. Un même événement peut être publié ou reçu plusieurs fois.

## Exercices de lecture
1. Où réside la première garantie durable contre perte de requête ? **Commit intention + Outbox**.
2. Où dédupliquer le paiement ? **À l'exécution autoritative**, en complément de l'API.
3. Peut-on notifier SETTLED dès l'ACK MQ ? **Non**.
4. Que faire après timeout d'exécution ? **Conserver UNKNOWN, consulter et réconcilier**.
