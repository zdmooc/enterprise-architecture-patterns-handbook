# ADR-006 — Stratégie DRP/DRCP
- **Statut** : Proposed
- **Date** : 2025-12-18
- **Contexte** : Continuité d’activité pour services critiques.
- **Décision** : Stratégie DRP à deux niveaux :
  - Niveau 1 : restauration automatisée (backup/restore) + IaC
  - Niveau 2 : site secondaire (actif/passif) pour services “Gold”
- **Liens** : `runbooks/RUNBOOK_DRP_TEST.md`, `nfr/SLO_SLI.md`
