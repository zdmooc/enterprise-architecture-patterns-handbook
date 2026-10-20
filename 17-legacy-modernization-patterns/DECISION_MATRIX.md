# Matrice de décision — Modernisation du legacy

Chaque besoin pointe sur la fiche exacte. Tests proposés ≠ résultats de production.

| Question à trancher | Fiche applicable | Acceptation minimale |
|---|---|---|
| Changer hébergement sans transformation | [rehost](01-rehost/README.md) | Invariant métier, test négatif et ADR |
| Adapter runtime en limitant le changement | [replatform](02-replatform/README.md) | Invariant métier, test négatif et ADR |
| Restructurer sans modifier la fonction | [refactor](03-refactor/README.md) | Invariant métier, test négatif et ADR |
| Remplacer une capacité par un nouveau produit | [replace](04-replace/README.md) | Invariant métier, test négatif et ADR |
| Retirer une application sans flux orphelins | [retire](05-retire/README.md) | Invariant métier, test négatif et ADR |
| Conserver le legacy sous risque accepté | [retain](06-retain/README.md) | Invariant métier, test négatif et ADR |
| Migrer des capacités via une façade progressive | [strangler fig migration](07-strangler-fig-migration/README.md) | Invariant métier, test négatif et ADR |
| Comparer deux implémentations sans double effet | [parallel run shadow](08-parallel-run-shadow/README.md) | Invariant métier, test négatif et ADR |
| Faire coexister deux schémas durant la migration | [expand contract db](09-expand-contract-db/README.md) | Invariant métier, test négatif et ADR |
| Bascule réversible sous garde de données | [cutover rollback](10-cutover-rollback/README.md) | Invariant métier, test négatif et ADR |

## Règles d'arbitrage

- Définir système autoritatif, frontières transactionnelles et options de repli avant le choix technique.
- Documenter les alternatives plus simples, la réversibilité, les coûts et les licences.
- Ne pas assimiler un déploiement ou un ACK à un comportement métier démontré.
- Exiger une preuve de panne, le propriétaire du runbook et la date de réexamen.

[Sommaire](README.md) · [Guide senior](../references/GUIDE_ARCHITECTE_151_PATTERNS.md)
