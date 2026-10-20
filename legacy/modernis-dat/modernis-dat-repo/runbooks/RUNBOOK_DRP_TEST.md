# Runbook — Test DRP/DRCP

## Objectifs
- Valider RTO/RPO
- Prouver la capacité de restauration et de bascule
- Documenter les résultats

## Scénarios
1) Perte d’un node worker
2) Perte namespace applicatif
3) Perte service Oracle (simulation) + reprise
4) Bascule vers site secondaire (si applicable)

## Preuves
- Captures dashboards
- Outputs commandes (oc/kubectl)
- Chronologie (timestamps)
- Rapport de test + actions correctives
