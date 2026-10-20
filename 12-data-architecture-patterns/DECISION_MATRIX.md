# Matrice de décision — Données

Chaque besoin pointe sur la fiche exacte. Tests proposés ≠ résultats de production.

| Question à trancher | Fiche applicable | Acceptation minimale |
|---|---|---|
| Propriétaire unique de l'attribut critique | [data ownership](01-data-ownership/README.md) | Invariant métier, test négatif et ADR |
| Historisation pour analyses BI | [data warehouse](02-data-warehouse/README.md) | Invariant métier, test négatif et ADR |
| Stockage de données brutes gouvernées | [data lake](03-data-lake/README.md) | Invariant métier, test négatif et ADR |
| Tables analytiques sur stockage ouvert | [lakehouse](04-lakehouse/README.md) | Invariant métier, test négatif et ADR |
| Gouvernance distribuée des produits de données | [data mesh](05-data-mesh/README.md) | Invariant métier, test négatif et ADR |
| Accès unifié à des données dispersées | [data fabric](06-data-fabric/README.md) | Invariant métier, test négatif et ADR |
| Propagez changements sans full load | [change data capture](07-change-data-capture/README.md) | Invariant métier, test négatif et ADR |
| Historisez sources et liens sans pertes | [data vault](08-data-vault/README.md) | Invariant métier, test négatif et ADR |
| Séparer brut, contrôlé et prêt à consommer | [medallion](09-medallion/README.md) | Invariant métier, test négatif et ADR |
| SLA/SLO et contrats de données versionnés | [data product contract](10-data-product-contract/README.md) | Invariant métier, test négatif et ADR |
| Dédoublonner identités et golden records | [master data management](11-master-data-management/README.md) | Invariant métier, test négatif et ADR |
| Rendre transformation et origine vérifiables | [data lineage governance](12-data-lineage-governance/README.md) | Invariant métier, test négatif et ADR |

## Règles d'arbitrage

- Définir système autoritatif, frontières transactionnelles et options de repli avant le choix technique.
- Documenter les alternatives plus simples, la réversibilité, les coûts et les licences.
- Ne pas assimiler un déploiement ou un ACK à un comportement métier démontré.
- Exiger une preuve de panne, le propriétaire du runbook et la date de réexamen.

[Sommaire](README.md) · [Guide senior](../references/GUIDE_ARCHITECTE_151_PATTERNS.md)
