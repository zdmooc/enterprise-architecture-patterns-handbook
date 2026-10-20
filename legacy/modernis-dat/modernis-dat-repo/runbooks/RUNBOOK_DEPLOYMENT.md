# Runbook — Déploiement / Mise en production (MEP)

## Pré-requis
- Matrice de flux validée (SSI/Réseau)
- Scans images OK
- Runbooks prêts + supervision en place
- Plan rollback validé

## Étapes (exemple)
1. Déployer en préprod (GitOps)
2. Tests fumée + checks SLO/SLI
3. Bascule progressive (canary si possible)
4. Validation métier
5. Surveillance renforcée T+24h
