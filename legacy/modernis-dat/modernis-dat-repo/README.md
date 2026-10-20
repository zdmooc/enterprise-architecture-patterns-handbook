# ModernIS — Modernisation du SI Interne Entreprises — Dépôt DAT (fictif professionnalisant)

- **Auteur (Architecte)** : Zidane Djamal
- **Version** : 1.0
- **Date** : 2025-12-18
- **Plateforme cible** : Kubernetes / Red Hat OpenShift 4.x
- **Socles** : API Management, Oracle, moteur de règles, S3, sécurité & réseau, RUN/DRP

## Objectif du dépôt
Ce dépôt fournit un **DAT complet** et des livrables associés (NFR, sécurité, matrices de flux, ADR, runbooks, cahiers des charges) afin de démontrer une maîtrise :
- Architecture technique (Java middleware, infra d’exécution, dimensionnement, HA)
- Rédaction (DAT, fiches, exigences, appels d’offres)
- Modélisation (ArchiMate / vues + diagrammes Mermaid)
- Kubernetes/OpenShift (RBAC, NetworkPolicies, quotas, GitOps)

## Démarrage rapide
1. Lire le DAT principal : **[`docs/DAT.md`](docs/DAT.md)**
2. Vérifier les décisions d’architecture : **[`adr/`](adr/)**
3. Consulter la sécurité + matrice de flux : **[`security/`](security/)** + **[`matrices/`](matrices/)**
4. Parcourir le plan RUN/DRP : **[`runbooks/`](runbooks/)**
5. Voir les exemples K8s/GitOps : **[`k8s/`](k8s/)**

## Convention de rédaction
- Les sections **“À compléter”** indiquent où adapter selon l’entreprise/mission.
- Les chiffres de dimensionnement sont donnés sous forme **d’hypothèses + plages** (min/nominal/max) et non comme valeurs arbitraires.
- Les décisions structurantes sont tracées via **ADR** (Architecture Decision Records).

## Génération (optionnel)
Ce dépôt est **utilisable tel quel** (lecture Markdown).
Optionnellement, vous pouvez générer un PDF (si `pandoc` est installé) :
```bash
bash scripts/build-pdf.sh
```
Sortie attendue : `dist/ModernIS_DAT.pdf`.

## Arborescence
Voir : **[`docs/REPO_STRUCTURE.md`](docs/REPO_STRUCTURE.md)**

## Avertissement
Ce projet est **fictif** (données/nom d’entreprise inventés) et sert à illustrer une approche professionnelle conforme aux pratiques d’architecture technique en contexte “Entreprise & SI interne”.
