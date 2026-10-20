# ADR-0012 — Architecture Toolchain

## Statut
Accepted

## Contexte

MayaBank doit documenter explicitement l’outillage que les architectes utilisent dans la pratique, sans transformer le dépôt en démonstrateur d’outils propriétaires.

## Décision

Le dépôt retient la logique suivante :

- **TOGAF** comme cadre de pensée ;
- **ArchiMate** comme langage de modélisation cible ;
- **Archi** comme outil de pratique open source ;
- **Markdown + GitHub** comme repository d’architecture simplifié ;
- mapping documenté vers **LeanIX / ADOIT / Sparx / Jira / Confluence** comme équivalents enterprise.

## Conséquences

### Positives
- cohérence entre apprentissage et posture senior ;
- distinction claire entre méthode, langage et outil ;
- dépôt plus crédible pour entretien et comité.

### Négatives
- le dépôt ne fournit pas un outillage EA enterprise complet ;
- certaines dimensions de gouvernance restent simulées et documentaires.
