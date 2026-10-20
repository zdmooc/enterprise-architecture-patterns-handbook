# Runbook — Accès & habilitations

## Objectif
- Contrôler les accès admin, limiter les privilèges, tracer les actions.

## Principes
- Accès nominatif (pas de comptes partagés)
- RBAC minimal
- Break-glass encadré (procédure d’urgence)

## Vérifications
- `oc auth can-i ...`
- Audit logs et revues périodiques
