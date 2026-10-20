# Catalogue NFR (exemple)

## Disponibilité
- Objectif : 99,9% mensuel (services critiques)
- Critère : temps d’indisponibilité <= 43 min / mois

## Performance
- Latence API : P95 < 200 ms (sur endpoints critiques)
- Débit : 1000 req/s (nominal) avec montée en charge horizontale

## Scalabilité
- HPA sur workloads stateless ; autoscaling cluster (si autorisé)
- Tests de charge + capacity review trimestrielle

## Sécurité
- TLS 1.2+ (ou 1.3 si support), mTLS interne si nécessaire
- RBAC minimal + secrets gérés (Vault/SealedSecrets)

## Exploitation
- Alerting : détection < 5 min ; MTTR cible < 60 min (P1)
- Runbooks : incident, rollback, DRP, accès

## Résilience
- RTO/RPO selon criticité (ex : RTO 4h, RPO 1h pour services “Gold”)
