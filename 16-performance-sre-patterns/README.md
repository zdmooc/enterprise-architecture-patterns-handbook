# Performance et SRE — 10 patterns

> **Référentiel pédagogique et anonymisé.** Les acteurs, chiffres et environnements des cas sont fictifs ; les technologies mentionnées sont des catégories ou standards. Aucun plan de production client n'est affirmé.

**Public cible :** Architecte performance, technique, SRE.

## Objectif

Respecter les délais d'une API critique malgré pics de charge, dépendance lente et perte d'une zone.

## Fiches disponibles

| N° | Pattern et dossier |
|---|---|
| 01 | [Caching patterns](01-caching-patterns/README.md) |
| 02 | [Load balancing](02-load-balancing/README.md) |
| 03 | [Sharding](03-sharding/README.md) |
| 04 | [Connection pooling](04-connection-pooling/README.md) |
| 05 | [Async offload](05-async-offload/README.md) |
| 06 | [Rate limiting](06-rate-limiting/README.md) |
| 07 | [Latency budget](07-latency-budget/README.md) |
| 08 | [Golden signals](08-golden-signals/README.md) |
| 09 | [Sli slo error budget](09-sli-slo-error-budget/README.md) |
| 10 | [Capacity planning](10-capacity-planning/README.md) |

Chaque fiche comprend : problème, architecture, **2 schémas Mermaid**, exemple métier, principes de mise en œuvre, compromis, pannes et qualification, critères d'ADR et question d'entretien. Les doublons conceptuels avec les 55 patterns existants sont traités comme **variantes de domaine** et référencés plutôt que comme de nouvelles garanties.

## Construire une architecture complète

- [Cas pratique transversal](CASE_STUDY.md) : AS-IS, proposition TO-BE, séquences, pannes et preuves.
- [Matrice de décision et ADR](DECISION_MATRIX.md).
- [Ensemble du handbook](../README.md).
- [Référentiel de sécurité Zero Trust](../14-security-zero-trust-patterns/README.md).

**Critère de conception :** appliquer le pattern uniquement lorsqu'il répond à un problème réel, puis démontrer ses invariants en test sur un contexte précisé.
