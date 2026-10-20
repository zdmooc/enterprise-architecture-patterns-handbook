# Matrice de décision — Résilience

Chaque besoin pointe sur la fiche exacte. Tests proposés ≠ résultats de production.

| Question à trancher | Fiche applicable | Acceptation minimale |
|---|---|---|
| Maintenir un seul site écrivain | [active passive](01-active-passive/README.md) | Invariant métier, test négatif et ADR |
| Conserver autorité par partition | [active active partitioned](02-active-active-partitioned/README.md) | Invariant métier, test négatif et ADR |
| Accepter après quorum valide | [quorum consensus](03-quorum-consensus/README.md) | Invariant métier, test négatif et ADR |
| Élire un leader sans split brain | [leader election](04-leader-election/README.md) | Invariant métier, test négatif et ADR |
| Bloquer l'ancien leader après bascule | [fencing token](05-fencing-token/README.md) | Invariant métier, test négatif et ADR |
| Distinguer suspicion et preuve d'arrêt | [failure detector](06-failure-detector/README.md) | Invariant métier, test négatif et ADR |
| Réguler producteur si consommateur saturé | [backpressure](07-backpressure/README.md) | Invariant métier, test négatif et ADR |
| Isoler les pools et dépendances | [bulkhead](08-bulkhead/README.md) | Invariant métier, test négatif et ADR |
| Dégrader les requêtes non prioritaires | [load shedding](09-load-shedding/README.md) | Invariant métier, test négatif et ADR |
| Maintenir un service limité explicite | [graceful degradation](10-graceful-degradation/README.md) | Invariant métier, test négatif et ADR |
| Définir modèle de cohérence des copies | [replication consistency](11-replication-consistency/README.md) | Invariant métier, test négatif et ADR |
| Restaurer à un point de reprise testable | [backup pitr](12-backup-pitr/README.md) | Invariant métier, test négatif et ADR |
| Tester pannes avec garde-fous | [chaos engineering](13-chaos-engineering/README.md) | Invariant métier, test négatif et ADR |
| Exercer PRA, RTO et RPO | [disaster recovery runbook](14-disaster-recovery-runbook/README.md) | Invariant métier, test négatif et ADR |
| Reconstituer état après réponse perdue | [reconciliation unknown outcome](15-reconciliation-unknown-outcome/README.md) | Invariant métier, test négatif et ADR |

## Règles d'arbitrage

- Définir système autoritatif, frontières transactionnelles et options de repli avant le choix technique.
- Documenter les alternatives plus simples, la réversibilité, les coûts et les licences.
- Ne pas assimiler un déploiement ou un ACK à un comportement métier démontré.
- Exiger une preuve de panne, le propriétaire du runbook et la date de réexamen.

[Sommaire](README.md) · [Guide senior](../references/GUIDE_ARCHITECTE_151_PATTERNS.md)
