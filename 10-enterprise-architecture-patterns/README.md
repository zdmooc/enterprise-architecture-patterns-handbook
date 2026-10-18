# Architecture d'entreprise et urbanisation — 12 patterns

> **Référentiel pédagogique et anonymisé.** Les acteurs, chiffres et environnements des cas sont fictifs ; les technologies mentionnées sont des catégories ou standards. Aucun plan de production client n'est affirmé.

**Public cible :** Architecte d'entreprise, urbaniste, architecte solutions.

## Objectif

Transformer un patrimoine de 80 applications fictives sans interrompre les fonctions critiques.

## Fiches disponibles

| N° | Pattern et dossier |
|---|---|
| 01 | [Business capability mapping](01-business-capability-mapping/README.md) |
| 02 | [Value stream mapping](02-value-stream-mapping/README.md) |
| 03 | [Business domain architecture](03-business-domain-architecture/README.md) |
| 04 | [Application landscape](04-application-landscape/README.md) |
| 05 | [Enterprise flow mapping](05-enterprise-flow-mapping/README.md) |
| 06 | [Application portfolio rationalization](06-application-portfolio-rationalization/README.md) |
| 07 | [Target architecture blueprint](07-target-architecture-blueprint/README.md) |
| 08 | [Transition architecture](08-transition-architecture/README.md) |
| 09 | [Transformation roadmap](09-transformation-roadmap/README.md) |
| 10 | [Architecture building blocks](10-architecture-building-blocks/README.md) |
| 11 | [Architecture governance adr](11-architecture-governance-adr/README.md) |
| 12 | [Architecture compliance nfr](12-architecture-compliance-nfr/README.md) |

Chaque fiche comprend : problème, architecture, **2 schémas Mermaid**, exemple métier, principes de mise en œuvre, compromis, pannes et qualification, critères d'ADR et question d'entretien. Les doublons conceptuels avec les 55 patterns existants sont traités comme **variantes de domaine** et référencés plutôt que comme de nouvelles garanties.

## Construire une architecture complète

- [Cas pratique transversal](CASE_STUDY.md) : AS-IS, proposition TO-BE, séquences, pannes et preuves.
- [Matrice de décision et ADR](DECISION_MATRIX.md).
- [Ensemble du handbook](../README.md).
- [Référentiel de sécurité Zero Trust](../14-security-zero-trust-patterns/README.md).

**Critère de conception :** appliquer le pattern uniquement lorsqu'il répond à un problème réel, puis démontrer ses invariants en test sur un contexte précisé.
