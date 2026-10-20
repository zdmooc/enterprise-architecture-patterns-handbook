# Matrice de décision — Performance / SRE

**Version corrigée :** chaque besoin renvoie au pattern portant réellement ce nom. Aucun résultat d'un POC n'est implicitement validé.

| Besoin réel | Pattern | Preuve à fournir |
|---|---|---|
| Réduire lectures répétées et définir fraîcheur | [caching patterns](01-caching-patterns/README.md) | Contrat, cas négatif, test de panne, ADR |
| Répartir les appels selon santé et capacité | [load balancing](02-load-balancing/README.md) | Contrat, cas négatif, test de panne, ADR |
| Partitionner données et clés d'accès | [sharding](03-sharding/README.md) | Contrat, cas négatif, test de panne, ADR |
| Borner les connexions globales en multi-réplicas | [connection pooling](04-connection-pooling/README.md) | Contrat, cas négatif, test de panne, ADR |
| Déporter traitements différables | [async offload](05-async-offload/README.md) | Contrat, cas négatif, test de panne, ADR |
| Limiter requêtes et protéger l'aval | [rate limiting](06-rate-limiting/README.md) | Contrat, cas négatif, test de panne, ADR |
| Répartir les délais p99 par dépendance | [latency budget](07-latency-budget/README.md) | Contrat, cas négatif, test de panne, ADR |
| Instrumenter quatre signaux de saturation | [golden signals](08-golden-signals/README.md) | Contrat, cas négatif, test de panne, ADR |
| Arbitrer fiabilité et changements | [sli slo error budget](09-sli-slo-error-budget/README.md) | Contrat, cas négatif, test de panne, ADR |
| Dimensionner pointe et mode dégradé | [capacity planning](10-capacity-planning/README.md) | Contrat, cas négatif, test de panne, ADR |

## Méthode

1. Définir contexte métier, propriétaire de données, NFR et contraintes de licences.
2. Comparer le minimum viable avec l'option utilisant ce pattern, risques et coûts inclus.
3. Tester nominal + anomalie + reprise ; expliciter ce qui n'est pas prouvé.
4. Formaliser décision, responsable, date de revue et conditions de retour arrière.

[Sommaire famille](README.md) · [Guide de sélection](../references/GUIDE_ARCHITECTE_151_PATTERNS.md)
