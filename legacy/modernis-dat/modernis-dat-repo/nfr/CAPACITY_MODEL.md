# Modèle de capacité (exemple)

## Entrées
- RPS nominal et pic par application
- Temps CPU moyen par requête (profiling)
- Consommation mémoire (heap + native)
- Dépendances : DB (connexions), S3, API gateway

## Calcul (simplifié)
- CPU_total ≈ RPS * CPU_ms / 1000 + marge
- RAM_total ≈ somme des pods * (requests + marge) + cache

## Sorties attendues
- Plages min/nominal/max par environnement
- Paramètres HPA (target CPU/memory, min/max replicas)
- Besoins cluster (nodes, réservations, PDB)
