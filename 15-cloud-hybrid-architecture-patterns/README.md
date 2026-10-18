# Architecture cloud hybride et multienvironnement — 10 patterns

> **Référentiel pédagogique et anonymisé.** Les acteurs, chiffres et environnements des cas sont fictifs ; les technologies mentionnées sont des catégories ou standards. Aucun plan de production client n'est affirmé.

**Public cible :** Architecte cloud, infrastructure et entreprise.

## Objectif

Déployer des services applicatifs hybrides avec réseau, IAM et coûts maîtrisés, sans déplacement non autorisé des données.

## Fiches disponibles

| N° | Pattern et dossier |
|---|---|
| 01 | [Landing zone](01-landing-zone/README.md) |
| 02 | [Hub spoke](02-hub-spoke/README.md) |
| 03 | [Transit connectivity](03-transit-connectivity/README.md) |
| 04 | [Private connectivity](04-private-connectivity/README.md) |
| 05 | [Multi account governance](05-multi-account-governance/README.md) |
| 06 | [Multi region strategy](06-multi-region-strategy/README.md) |
| 07 | [Hybrid workload placement](07-hybrid-workload-placement/README.md) |
| 08 | [Cloud bursting](08-cloud-bursting/README.md) |
| 09 | [Infrastructure as code](09-infrastructure-as-code/README.md) |
| 10 | [Cloud exit portability](10-cloud-exit-portability/README.md) |

Chaque fiche comprend : problème, architecture, **2 schémas Mermaid**, exemple métier, principes de mise en œuvre, compromis, pannes et qualification, critères d'ADR et question d'entretien. Les doublons conceptuels avec les 55 patterns existants sont traités comme **variantes de domaine** et référencés plutôt que comme de nouvelles garanties.

## Construire une architecture complète

- [Cas pratique transversal](CASE_STUDY.md) : AS-IS, proposition TO-BE, séquences, pannes et preuves.
- [Matrice de décision et ADR](DECISION_MATRIX.md).
- [Ensemble du handbook](../README.md).
- [Référentiel de sécurité Zero Trust](../14-security-zero-trust-patterns/README.md).

**Critère de conception :** appliquer le pattern uniquement lorsqu'il répond à un problème réel, puis démontrer ses invariants en test sur un contexte précisé.
