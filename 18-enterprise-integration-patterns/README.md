# Enterprise Integration Patterns — extensions ciblées

Ces fiches approfondissent le transport et les contrats de messages. Elles ne remplacent pas les 10 patterns d'intégration du handbook.

| Fiche | Problème dominant |
|---|---|
| [Claim Check](05-claim-check/README.md) | Un message contient une pièce trop volumineuse pour le broker. |
| [Dead Letter Channel & Parking Lot](06-dead-letter-channel/README.md) | Un message constamment invalide peut monopoliser les reprises d'un consommateur. |
| [Competing Consumers / Work Queue](07-competing-consumers/README.md) | Des traitements indépendants doivent absorber des pics avec plusieurs workers. |
| [Event Schema Evolution / Compatibility Gate](08-schema-evolution/README.md) | Un producteur versionne un événement alors que les consommateurs déploient à des cadences différentes. |
| [Transactional Outbox](01-transactional-outbox/README.md) | Publication fiable après transaction locale |
| [Transactional Inbox](02-transactional-inbox/README.md) | Consommateur idempotent et déduplication durable |
| [Content-Based Router](03-content-based-router/README.md) | Sélection déterministe des cibles |
| [Splitter / Aggregator](04-splitter-aggregator/README.md) | Fan-out et recomposition avec état PARTIAL |

## Matrice de choix

- Publication après commit : **Outbox** ; réception répétée : **Inbox**.
- Type/version vers destinations : **Router** ; gros payload : **Claim Check**.
- Lot divisible : **Splitter/Aggregator** ; erreur empoisonnée : **DLQ**.
- Travail parallèle indépendant : **Competing Consumers** ; déploiements asynchrones des contrats : **Schema Evolution**.

Les garanties restent conditionnées par une transaction/contrat, des tests de crash, une source de vérité et la sécurité. Toutes les données sont fictives.
