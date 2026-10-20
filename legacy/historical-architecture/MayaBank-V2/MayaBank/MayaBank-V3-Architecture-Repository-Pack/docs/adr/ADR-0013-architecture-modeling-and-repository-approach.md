# ADR-0013 — Architecture Modeling and Repository Approach

## Statut
Accepted

## Contexte

Le dépôt MayaBank contient déjà des HLD, LLD, ADR, roadmaps, runbooks et artefacts de risques.  
Il faut formaliser que ces éléments constituent ensemble un **repository d’architecture simplifié**.

## Décision

MayaBank adopte une approche repository basée sur :

- un dépôt Git versionné ;
- des documents Markdown comme source de vérité principale ;
- des modèles ArchiMate rangés dans `models/archimate/` ;
- une traçabilité vision → HLD → ADR → LLD → backlog → evidence ;
- une gouvernance explicite dans `docs/governance/`.

## Conséquences

### Positives
- meilleure reprise de chantier ;
- meilleure cohérence documentaire ;
- meilleure lisibilité de la posture d’architecte.

### Négatives
- outillage plus léger qu’un vrai repository EA d’entreprise ;
- discipline documentaire nécessaire pour maintenir la cohérence.
