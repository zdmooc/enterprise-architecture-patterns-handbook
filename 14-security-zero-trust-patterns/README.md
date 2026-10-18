# Sécurité, identité et Zero Trust — 12 patterns

> **Référentiel pédagogique et anonymisé.** Les acteurs, chiffres et environnements des cas sont fictifs ; les technologies mentionnées sont des catégories ou standards. Aucun plan de production client n'est affirmé.

**Public cible :** Architecte sécurité, technique, solutions.

## Objectif

Protéger un dossier sensible partagé entre API, workloads et documents, y compris contre un acteur interne non autorisé.

## Fiches disponibles

| N° | Pattern et dossier |
|---|---|
| 01 | [Zero trust](01-zero-trust/README.md) |
| 02 | [Policy decision enforcement](02-policy-decision-enforcement/README.md) |
| 03 | [Defense in depth](03-defense-in-depth/README.md) |
| 04 | [Identity federation](04-identity-federation/README.md) |
| 05 | [Workload identity](05-workload-identity/README.md) |
| 06 | [Rbac abac](06-rbac-abac/README.md) |
| 07 | [Secret lifecycle](07-secret-lifecycle/README.md) |
| 08 | [Mutual tls pki](08-mutual-tls-pki/README.md) |
| 09 | [Network microsegmentation](09-network-microsegmentation/README.md) |
| 10 | [Encryption key management](10-encryption-key-management/README.md) |
| 11 | [Software supply chain](11-software-supply-chain/README.md) |
| 12 | [Audit segregation duties](12-audit-segregation-duties/README.md) |

Chaque fiche comprend : problème, architecture, **2 schémas Mermaid**, exemple métier, principes de mise en œuvre, compromis, pannes et qualification, critères d'ADR et question d'entretien. Les doublons conceptuels avec les 55 patterns existants sont traités comme **variantes de domaine** et référencés plutôt que comme de nouvelles garanties.

## Construire une architecture complète

- [Cas pratique transversal](CASE_STUDY.md) : AS-IS, proposition TO-BE, séquences, pannes et preuves.
- [Matrice de décision et ADR](DECISION_MATRIX.md).
- [Ensemble du handbook](../README.md).
- [Référentiel de sécurité Zero Trust](../14-security-zero-trust-patterns/README.md).

**Critère de conception :** appliquer le pattern uniquement lorsqu'il répond à un problème réel, puis démontrer ses invariants en test sur un contexte précisé.
