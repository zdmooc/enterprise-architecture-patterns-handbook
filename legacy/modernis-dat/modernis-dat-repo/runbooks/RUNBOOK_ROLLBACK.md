# Runbook — Rollback

## Quand rollback ?
- Taux 5xx > seuil, latence non tenable, corruption données suspectée

## Procédure
1. Stopper la propagation (désactiver canary)
2. Revenir à la version N-1 (GitOps / tag)
3. Vérifier intégrité (DB, messages, logs)
4. Communiquer + ouvrir RCA
