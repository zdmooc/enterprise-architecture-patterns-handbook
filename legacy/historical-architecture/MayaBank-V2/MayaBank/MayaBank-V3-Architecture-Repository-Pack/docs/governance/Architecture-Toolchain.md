# Architecture Toolchain

## 1. Objet

Ce document décrit l’**outillage de l’architecte** retenu dans MayaBank, en séparant clairement :

- la **méthode**
- le **langage de modélisation**
- les **outils**
- les **équivalents enterprise**

## 2. Niveaux à distinguer

### 2.1 Méthode
- **TOGAF** : structure la démarche de travail, les vues, les transitions, les décisions.

### 2.2 Langage
- **ArchiMate** : structure les représentations de l’architecture.

### 2.3 Outils de pratique dans MayaBank
- **Archi**
- **GitHub**
- **Markdown**
- **GitHub Issues** ou backlog simple
- **Jenkins / Argo CD / Helm / Kustomize**

### 2.4 Outils enterprise de référence
- **LeanIX**
- **ADOIT**
- **Sparx Enterprise Architect**
- **Jira**
- **Confluence**
- **OpenShift GitOps**
- **Red Hat ACM** (en référence d’exploitation multi-cluster)

## 3. Choix retenu pour MayaBank

MayaBank reste volontairement :
- versionnable ;
- open source sur son socle principal ;
- simple à reprendre ;
- assez crédible pour préparer une posture senior.

Pour cette raison, le dépôt ne tente pas d’émuler un outil enterprise complet.  
Il documente le **mapping** vers ces outils, tout en gardant un outillage léger et reproductible.

## 4. Mapping synthétique

| Besoin | Outil retenu dans MayaBank | Équivalent entreprise |
|---|---|---|
| Modélisation ArchiMate | Archi | LeanIX / ADOIT / Sparx EA |
| Documentation source de vérité | Markdown dans Git | Confluence / repository EA |
| Suivi du backlog | GitHub Issues | Jira |
| GitOps | Argo CD | OpenShift GitOps |
| Déploiement / CI | Jenkins | Jenkins / GitLab CI / autres |
| Gouvernance | docs/governance + ADR + logs | Architecture Board / Design Authority |

## 5. Décision

MayaBank retient donc une **toolchain duale** :
- **outil réel de pratique** dans le dépôt ;
- **équivalent enterprise** documenté pour la trajectoire senior.
