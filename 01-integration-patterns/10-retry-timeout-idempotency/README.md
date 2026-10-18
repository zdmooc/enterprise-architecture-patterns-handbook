# 10 — Retry / Timeout / Idempotency : sécurité des reprises

## Objectif et règle prioritaire
Dans un virement, la **réponse peut se perdre après l'exécution réelle**. Un retry naïf peut doubler les fonds. Il faut distinguer :
- **Timeout** = délai maximal d'attente ; ne dit rien à lui seul du résultat métier.
- **Retry** = nouvelle tentative techniquement appropriée, limitée dans le temps, en nombre et en charge.
- **Idempotency** = répétition de la *même intention métier* sans nouvel effet financier.

## Scénario central
~~~mermaid
sequenceDiagram
  participant C as Client
  participant A as Payment API
  participant D as DB + contrainte unique
  participant X as Système bancaire
  C->>A: POST 500 EUR / Idempotency-Key PAY-001
  A->>D: Enregistrer intention VIR-001 + Outbox
  A->>X: ExecutePayment(VIR-001)
  X->>X: Exécution unique autoritative
  X--xA: Confirmation perdue
  A-->>C: Timeout / statut inconnu
  C->>A: Retry même clé PAY-001
  A->>D: Retrouver VIR-001, mêmes paramètres
  A-->>C: Même ordre ; statut actuel / réconciliation
  Note over A,X: Jamais de nouvel ordre VIR-002 pour la même intention
~~~
Le diagramme simplifie le chemin MQ et le relais, détaillés dans le cas d'étude.

## Algorithme défendable
1. **Valider identité, autorisation et payload**.
2. Construire scope=(tenant/client, endpoint/operation, idempotencyKey) ; calculer une empreinte canonique du payload et de l'identité pertinente.
3. Transaction SQL : UNIQUE(scope) ; soit INSERT ordre + Outbox, soit lire ordre existant. Refuser même clé avec paramètres différents (409 ou erreur contractuelle).
4. Retourner le même paymentId ; tenir un état durable au fil du cycle de vie.
5. Utiliser paymentId comme référence métier stable sur MQ, dans les consommateurs et le système exécutant ; dédupliquer **l'effet financier**, pas seulement l'appel HTTP.
6. Sur « response lost », consulter l'état autoritatif et réconcilier avant toute nouvelle action susceptible d'exécuter un paiement.
7. Couvrir par la conservation des clés tout le cycle de retry/redélivrance, la durée de vie des ordres et les exigences d'archivage ; ne jamais purger des clés sans stratégie empêchant les vieilles redélivrances.

## SQL schématique
~~~sql
CREATE TABLE payment_intents (
  payment_id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload_fingerprint TEXT NOT NULL,
  amount_minor BIGINT NOT NULL,
  currency CHAR(3) NOT NULL,
  status TEXT NOT NULL,
  state_version BIGINT NOT NULL DEFAULT 0,
  UNIQUE (client_id, idempotency_key)
);
-- Dans la même transaction: INSERT payment_intents + INSERT outbox(...)
-- Le composant de règlement applique lui aussi une contrainte métier idempotente.
~~~

## Timeout et budget de Retry
Comparer deadline réglementaire et budget bout en bout ; fixer connect timeout, read timeout, transaction timeout et deadline business. Les retries sont bornés et espacés (exponential backoff + jitter). Pas de retry automatique des 4xx métier ni des POST non idempotents. 429 / 503 peuvent justifier un retry selon contrat, sans dépasser deadline.

## Matrice des pannes
| Panne | Statut | Suite |
|---|---|---|
| Avant commit DB | Non confirmé | Relire la clé et déterminer présence de l'ordre |
| Après commit DB avant publication | Ordre durable | Relais Outbox après reprise |
| Après publication avant ACK | Livraison incertaine | Republier **même** messageId métier ; consommateur idempotent |
| Après effet financier avant réponse | Issue inconnue côté appelant | Interroger/réconcilier l'autorité financière |
| Double POST simultané sur deux Pods | Conflit de concurrence | UNIQUE + transaction / verrou de version |
| Kafka/MQ redélivre | Message dupliqué | Inbox/dedup consommation, aucune double exécution |
| Paiement instantané expiré | Deadline franchie | Règles SCT Inst, pas de soumission tardive aveugle |
| Notification échoue après SETTLED | Paiement fini | Retenter notification seulement |

## Transactional Outbox et Idempotent Consumer
Outbox enregistre événement/commande **dans la même transaction locale** que l'état métier, puis publie. Le relais peut publier plusieurs fois. Le consommateur doit enregistrer les messages traités atomiquement avec son effet local et fournir une déduplication forte à l'exécution bancaire.

## Observabilité et audit
Tracer duplicate_suppressed_count, payment_outcome_unknown, stale_command_rejected, retry_attempts, timeout_rate, MQ oldest message age, Kafka consumer lag, reconciliation_age. Ne jamais logguer des secrets ou numéros complets. Définir alertes et runbooks pour les états UNKNOWN.

## Tests essentiels
- Double clic client ; collision simultanée sur plusieurs replicas.
- Couper réseau après commit bancaire, avant ACK/response.
- Crasher relais Outbox après publication, avant marquage de sortie.
- Redélivrer MQ après commit métier.
- Modifier amount avec même clé : refus.
- Réinjecter une commande expirée après indisponibilité.
- Rejouer notifications sans réexécuter le paiement.

## Entretien
**Q : exactly-once Kafka garantit-il exactement un débit bancaire ?** Non, garantie Kafka à périmètre délimité. **Q : timeout = échec financier ?** Non. **Q : pourquoi conserver la même clé ?** Elle identifie l'intention durable et empêche une deuxième création.

Sources : [Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html), [Idempotent Consumer](https://microservices.io/patterns/communication-style/idempotent-consumer.html), [EPC SCT Inst](https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-instant-credit-transfer-sct-inst/sepa-instant-credit-transfer).

---

## Illustrations complémentaires — doubles requêtes et scénario de panne

### Deux appels, une seule intention
~~~mermaid
flowchart TB
    A["POST 500 EUR, clé PAY-001"] --> D{"Clé déjà connue dans DB ACID ?"}
    B["Retry POST 500 EUR, même PAY-001"] --> D
    D -->|"Non, insertion atomique"| ONE["Créer VIR-001 + Outbox une seule fois"]
    D -->|"Oui + même empreinte"| OLD["Retrouver VIR-001 / son statut"]
    D -->|"Oui + paramètres différents"| FAIL["Refuser conflit, aucun nouvel ordre"]
    ONE --> K["Core : exécution via référence financière stable"]
    OLD --> K
    K --> CHECK["Un seul effet autoritatif"]
~~~

### Le paiement a réussi, mais la réponse a été perdue
~~~mermaid
sequenceDiagram
    actor U as Client
    participant A as Payment API
    participant D as Stockage d'idempotence
    participant K as Core bancaire
    U->>A: POST 500 EUR + clé PAY-001
    A->>D: VIR-001 enregistré
    A->>K: Execute(VIR-001)
    K->>K: Un seul mouvement comptable
    K--xA: Réponse perdue
    A-->>U: TIMEOUT / état non confirmé
    U->>A: Retry avec PAY-001
    A->>D: Retrouver VIR-001
    A->>K: QueryStatus(VIR-001)
    K-->>A: SETTLED avec preuve
    A-->>U: Statut réel, aucune seconde exécution
~~~

### Retry borné (exemple technique, hors chemin de règlement irréversible)
~~~mermaid
flowchart LR
    A["Appel T0"] -->|"Attente 200 ms + jitter"| R1["Retry 1"]
    R1 -->|"Attente 500 ms + jitter"| R2["Retry 2"]
    R2 -->|"Attente 1100 ms + jitter"| R3["Retry 3 ou abandon"]
~~~
Le budget exact doit intégrer les deadlines ; la même clé et la même référence métier sont **obligatoires** si une répétition de commande est permise.

### Les six incidents à tester
| Incident | Réaction sûre |
|---|---|
| Panne avant commit | Relecture de la clé, pas de supposition |
| Panne après commit avant MQ | Reprise Outbox |
| Broker redélivre | Idempotent Consumer |
| Réponse core perdue | UNKNOWN puis QueryStatus |
| Deux Pods reçoivent même clé | Unicité transactionnelle |
| Événement tardif / transaction expirée | Comparer deadline et preuve avant toute action |

