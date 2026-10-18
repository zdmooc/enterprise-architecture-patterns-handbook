# Modernisation des applications et systèmes historiques — 10 patterns

> **Référentiel pédagogique et anonymisé.** Les acteurs, chiffres et environnements des cas sont fictifs ; les technologies mentionnées sont des catégories ou standards. Aucun plan de production client n'est affirmé.

**Public cible :** Architecte applications, solutions, intégration.

## Objectif

Migrer une application Java/JEE historique sans interrompre ses contrats ni déclencher deux traitements.

## Fiches disponibles

| N° | Pattern et dossier |
|---|---|
| 01 | [Rehost](01-rehost/README.md) |
| 02 | [Replatform](02-replatform/README.md) |
| 03 | [Refactor](03-refactor/README.md) |
| 04 | [Replace](04-replace/README.md) |
| 05 | [Retire](05-retire/README.md) |
| 06 | [Retain](06-retain/README.md) |
| 07 | [Strangler fig migration](07-strangler-fig-migration/README.md) |
| 08 | [Parallel run shadow](08-parallel-run-shadow/README.md) |
| 09 | [Expand contract db](09-expand-contract-db/README.md) |
| 10 | [Cutover rollback](10-cutover-rollback/README.md) |

Chaque fiche comprend : problème, architecture, **2 schémas Mermaid**, exemple métier, principes de mise en œuvre, compromis, pannes et qualification, critères d'ADR et question d'entretien. Les doublons conceptuels avec les 55 patterns existants sont traités comme **variantes de domaine** et référencés plutôt que comme de nouvelles garanties.

## Construire une architecture complète

- [Cas pratique transversal](CASE_STUDY.md) : AS-IS, proposition TO-BE, séquences, pannes et preuves.
- [Matrice de décision et ADR](DECISION_MATRIX.md).
- [Ensemble du handbook](../README.md).
- [Référentiel de sécurité Zero Trust](../14-security-zero-trust-patterns/README.md).

**Critère de conception :** appliquer le pattern uniquement lorsqu'il répond à un problème réel, puis démontrer ses invariants en test sur un contexte précisé.
