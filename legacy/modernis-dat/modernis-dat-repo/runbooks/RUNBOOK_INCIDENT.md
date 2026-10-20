# Runbook — Gestion incident (P1/P2)

## Déclenchement
- Alerte SLO burn rate / taux 5xx / latence P95
- Signalement métier

## Triage (5–10 min)
1. Identifier impact (service, environnements, utilisateurs)
2. Vérifier dashboards (latence, erreurs, saturation)
3. Examiner logs (correlation-id), erreurs récentes
4. Décider escalade (DBA, Réseau, SSI)

## Actions
- Mitigation : scale out, rollback, désactivation feature flag, bypass partiel via gateway
- Communication : point de situation toutes les 30 min

## Clôture
- Restauration service validée
- RCA (post-mortem) sous 48h
- Mise à jour DAT/ADR si changement archi
