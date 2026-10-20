# HLD Architecture Repository and Tooling

## 1. Objet

Ce document décrit le **bloc d’architecture V3** dédié au **repository d’architecture**, à la **modélisation** et à l’**outillage de l’architecte** dans MayaBank.

Il ne décrit pas un outil propriétaire complet d’Enterprise Architecture.  
Il décrit comment MayaBank organise ses artefacts pour jouer le rôle d’un **repository d’architecture simplifié**, cohérent, versionné et réutilisable.

## 2. Contexte

Un architecte senior ne travaille pas uniquement avec des HLD/LLD isolés.  
Il travaille avec :

- une vision ;
- des capacités métier ;
- des HLD ;
- des LLD ;
- des décisions d’architecture ;
- un backlog ;
- des runbooks ;
- des risques ;
- des principes de gouvernance ;
- des modèles de représentation.

MayaBank doit donc expliciter cette couche, afin d’être aussi un dépôt d’entraînement à la posture d’architecte.

## 3. Principes

### 3.1 Séparation méthode / langage / outil

- **TOGAF** = cadre de démarche
- **ArchiMate** = langage de modélisation
- **Archi / LeanIX / ADOIT / Sparx / Jira / Confluence** = outils

Ces trois niveaux ne doivent jamais être confondus.

### 3.2 Le dépôt comme repository d’architecture

Dans MayaBank, le dépôt Git sert de **source de vérité architecturale** simplifiée.

Le repository d’architecture s’appuie sur :
- Markdown versionné ;
- HLD / LLD ;
- ADR ;
- roadmaps ;
- Decision Log ;
- fichiers de risques ;
- répertoire `models/archimate/` pour les modèles cibles.

### 3.3 Mapping open source → enterprise

L’objectif n’est pas de reproduire un outillage entreprise complet.  
L’objectif est de documenter un **chemin crédible** entre un dépôt open source et les outils que les architectes utilisent en environnement enterprise.

## 4. Outillage retenu dans MayaBank

### 4.1 Outillage principal du dépôt

- **GitHub** : versioning du repository
- **Markdown** : format documentaire principal
- **Archi** : modélisation ArchiMate open source
- **GitHub Issues** ou backlog simple : suivi du travail
- **Jenkins / Argo CD / Helm / Kustomize** : outillage d’industrialisation côté plateforme

### 4.2 Outils enterprise mappés

- **Archi** ↔ **LeanIX / ADOIT / Sparx Enterprise Architect**
- **Markdown / GitHub** ↔ **Confluence / repository EA**
- **GitHub Issues** ↔ **Jira**
- **Argo CD** ↔ **OpenShift GitOps**
- gouvernance du dépôt ↔ **Design Authority / Architecture Board**

## 5. Structure cible

Le bloc V3 introduit ou renforce :

- `docs/governance/Architecture-Toolchain.md`
- `docs/governance/Documentation-and-Decision-Flow.md`
- `docs/governance/Backlog-and-Design-Authority-Process.md`
- `docs/adr/ADR-0012-architecture-toolchain.md`
- `docs/adr/ADR-0013-architecture-modeling-and-repository-approach.md`
- `models/archimate/`

## 6. Flux de travail cible

Le flux cible est le suivant :

1. **Vision / capacités**
2. **HLD**
3. **ADR**
4. **LLD**
5. **Backlog / Sprint**
6. **Implémentation semi-exécutable**
7. **Runbooks / evidence**
8. **Mise à jour du repository**

## 7. Livrables attendus

À ce stade, MayaBank doit produire :
- un outillage d’architecture explicite ;
- une démarche de modélisation lisible ;
- une trace claire des décisions ;
- un lien clair entre architecture et réalisation.

## 8. Limites assumées

- le dépôt n’embarque pas un véritable outil EA propriétaire ;
- la modélisation ArchiMate reste volontairement progressive ;
- la traçabilité backlog outillée reste simple à ce stade ;
- MayaBank privilégie la **lisibilité et l’apprentissage** à l’exhaustivité outillée.

## 9. Références internes

- `README.md`
- `docs/governance/Architecture-Toolchain.md`
- `docs/governance/Documentation-and-Decision-Flow.md`
- `docs/governance/Backlog-and-Design-Authority-Process.md`
- `models/archimate/README.md`
