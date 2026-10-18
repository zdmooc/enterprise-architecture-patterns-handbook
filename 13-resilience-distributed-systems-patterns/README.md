# Systèmes distribués et résilience — 15 patterns

> **Référentiel pédagogique et anonymisé.** Les acteurs, chiffres et environnements des cas sont fictifs ; les technologies mentionnées sont des catégories ou standards. Aucun plan de production client n'est affirmé.

**Public cible :** Architecte résilience, technique et SRE.

## Objectif

Survivre à la perte de service, de réseau et de site sans double effet autoritatif.

## Fiches disponibles

| N° | Pattern et dossier |
|---|---|
| 01 | [Active passive](01-active-passive/README.md) |
| 02 | [Active active partitioned](02-active-active-partitioned/README.md) |
| 03 | [Quorum consensus](03-quorum-consensus/README.md) |
| 04 | [Leader election](04-leader-election/README.md) |
| 05 | [Fencing token](05-fencing-token/README.md) |
| 06 | [Failure detector](06-failure-detector/README.md) |
| 07 | [Backpressure](07-backpressure/README.md) |
| 08 | [Bulkhead](08-bulkhead/README.md) |
| 09 | [Load shedding](09-load-shedding/README.md) |
| 10 | [Graceful degradation](10-graceful-degradation/README.md) |
| 11 | [Replication consistency](11-replication-consistency/README.md) |
| 12 | [Backup pitr](12-backup-pitr/README.md) |
| 13 | [Chaos engineering](13-chaos-engineering/README.md) |
| 14 | [Disaster recovery runbook](14-disaster-recovery-runbook/README.md) |
| 15 | [Reconciliation unknown outcome](15-reconciliation-unknown-outcome/README.md) |

Chaque fiche comprend : problème, architecture, **2 schémas Mermaid**, exemple métier, principes de mise en œuvre, compromis, pannes et qualification, critères d'ADR et question d'entretien. Les doublons conceptuels avec les 55 patterns existants sont traités comme **variantes de domaine** et référencés plutôt que comme de nouvelles garanties.

## Construire une architecture complète

- [Cas pratique transversal](CASE_STUDY.md) : AS-IS, proposition TO-BE, séquences, pannes et preuves.
- [Matrice de décision et ADR](DECISION_MATRIX.md).
- [Ensemble du handbook](../README.md).
- [Référentiel de sécurité Zero Trust](../14-security-zero-trust-patterns/README.md).

**Critère de conception :** appliquer le pattern uniquement lorsqu'il répond à un problème réel, puis démontrer ses invariants en test sur un contexte précisé.
