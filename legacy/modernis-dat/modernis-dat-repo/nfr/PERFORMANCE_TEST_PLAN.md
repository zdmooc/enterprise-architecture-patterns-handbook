# Plan de test performance (exemple)

## Objectifs
- Valider les SLO : latence, débit, stabilité (soak)
- Identifier points de saturation (app, gateway, DB, réseau)

## Méthode
- Scénarios réalistes : endpoints critiques + mix de parcours
- Montée progressive (ramp-up) + plateau + décharge
- Mesures : P95/P99, CPU/RAM, GC, pools connexions, erreurs

## Outils (exemples)
- k6 / Gatling / Locust (selon stack)
- Observabilité : Prometheus/Grafana + logs corrélés

## Livrables
- Rapport perf : courbes, seuils, recommandations
- ADR si changement d’archi requis
