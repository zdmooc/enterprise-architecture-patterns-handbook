# Guide ArchiMate (pragmatique)

## Objectif
Produire des vues lisibles pour comités métiers/techniques/sécurité et maintenir la traçabilité des décisions.

## Vues recommandées
1. **Motivation** : drivers, objectifs, exigences (NFR) + parties prenantes
2. **Métier** : processus RH/CRM/Finance (haut niveau)
3. **Applicative** : composants, services, interfaces, dépendances
4. **Technologique** : plateformes (OpenShift, DB, S3), zones réseau, LB, WAF

## Bonnes pratiques
- Une vue = un message. Limiter la densité.
- Nommer les interfaces (contrats, protocoles, ports).
- Lier chaque exigence à un contrôle (sécurité/perf/DRP).
- Traçabilité : décisions via ADR + liens depuis les vues.
