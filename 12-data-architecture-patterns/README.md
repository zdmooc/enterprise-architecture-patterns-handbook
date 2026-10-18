# Architecture de données, gouvernance et analytique — 12 patterns

> **Référentiel pédagogique et anonymisé.** Les acteurs, chiffres et environnements des cas sont fictifs ; les technologies mentionnées sont des catégories ou standards. Aucun plan de production client n'est affirmé.

**Public cible :** Architecte de données, solutions et entreprise.

## Objectif

Consolider un reporting de dossiers à partir de flux changeants tout en conservant les sources autoritatives.

## Fiches disponibles

| N° | Pattern et dossier |
|---|---|
| 01 | [Data ownership](01-data-ownership/README.md) |
| 02 | [Data warehouse](02-data-warehouse/README.md) |
| 03 | [Data lake](03-data-lake/README.md) |
| 04 | [Lakehouse](04-lakehouse/README.md) |
| 05 | [Data mesh](05-data-mesh/README.md) |
| 06 | [Data fabric](06-data-fabric/README.md) |
| 07 | [Change data capture](07-change-data-capture/README.md) |
| 08 | [Data vault](08-data-vault/README.md) |
| 09 | [Medallion](09-medallion/README.md) |
| 10 | [Data product contract](10-data-product-contract/README.md) |
| 11 | [Master data management](11-master-data-management/README.md) |
| 12 | [Data lineage governance](12-data-lineage-governance/README.md) |

Chaque fiche comprend : problème, architecture, **2 schémas Mermaid**, exemple métier, principes de mise en œuvre, compromis, pannes et qualification, critères d'ADR et question d'entretien. Les doublons conceptuels avec les 55 patterns existants sont traités comme **variantes de domaine** et référencés plutôt que comme de nouvelles garanties.

## Construire une architecture complète

- [Cas pratique transversal](CASE_STUDY.md) : AS-IS, proposition TO-BE, séquences, pannes et preuves.
- [Matrice de décision et ADR](DECISION_MATRIX.md).
- [Ensemble du handbook](../README.md).
- [Référentiel de sécurité Zero Trust](../14-security-zero-trust-patterns/README.md).

**Critère de conception :** appliquer le pattern uniquement lorsqu'il répond à un problème réel, puis démontrer ses invariants en test sur un contexte précisé.
