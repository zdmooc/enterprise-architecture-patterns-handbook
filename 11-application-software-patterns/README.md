# Architecture applicative et conception logicielle — 15 patterns

> **Référentiel pédagogique et anonymisé.** Les acteurs, chiffres et environnements des cas sont fictifs ; les technologies mentionnées sont des catégories ou standards. Aucun plan de production client n'est affirmé.

**Public cible :** Architecte applicatif, architecte solutions, Tech Lead.

## Objectif

Moderniser un système fictif de dossiers avec logique Java et plusieurs consommateurs sans explosion de microservices.

## Fiches disponibles

| N° | Pattern et dossier |
|---|---|
| 01 | [Layered architecture](01-layered-architecture/README.md) |
| 02 | [Hexagonal ports adapters](02-hexagonal-ports-adapters/README.md) |
| 03 | [Clean architecture](03-clean-architecture/README.md) |
| 04 | [Modular monolith](04-modular-monolith/README.md) |
| 05 | [Microservices decomposition](05-microservices-decomposition/README.md) |
| 06 | [Ddd bounded context](06-ddd-bounded-context/README.md) |
| 07 | [Aggregate invariants](07-aggregate-invariants/README.md) |
| 08 | [Cqrs read write](08-cqrs-read-write/README.md) |
| 09 | [Event sourcing](09-event-sourcing/README.md) |
| 10 | [Api contract first](10-api-contract-first/README.md) |
| 11 | [Dependency inversion](11-dependency-inversion/README.md) |
| 12 | [Anti corruption domain](12-anti-corruption-domain/README.md) |
| 13 | [Backend for frontend](13-backend-for-frontend/README.md) |
| 14 | [Unit of work](14-unit-of-work/README.md) |
| 15 | [Branch by abstraction](15-branch-by-abstraction/README.md) |

Chaque fiche comprend : problème, architecture, **2 schémas Mermaid**, exemple métier, principes de mise en œuvre, compromis, pannes et qualification, critères d'ADR et question d'entretien. Les doublons conceptuels avec les 55 patterns existants sont traités comme **variantes de domaine** et référencés plutôt que comme de nouvelles garanties.

## Construire une architecture complète

- [Cas pratique transversal](CASE_STUDY.md) : AS-IS, proposition TO-BE, séquences, pannes et preuves.
- [Matrice de décision et ADR](DECISION_MATRIX.md).
- [Ensemble du handbook](../README.md).
- [Référentiel de sécurité Zero Trust](../14-security-zero-trust-patterns/README.md).

**Critère de conception :** appliquer le pattern uniquement lorsqu'il répond à un problème réel, puis démontrer ses invariants en test sur un contexte précisé.
