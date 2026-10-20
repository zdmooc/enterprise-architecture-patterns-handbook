# SLO / SLI (exemple)

## SLI (indicateurs)
- Disponibilité : % requêtes 2xx/3xx vs total
- Latence : P95/P99
- Erreurs : taux 5xx, timeouts
- Saturation : CPU throttling, mémoire, connexions DB

## SLO (objectifs)
- Disponibilité : 99,9% (Gold) / 99,5% (Silver)
- Latence : P95 < 200 ms (Gold)
- Erreurs : < 0,5% 5xx (Gold)

## Alertes (principes)
- Alertes orientées impact (SLO burn rate)
- Seuils opérationnels + runbooks associés
