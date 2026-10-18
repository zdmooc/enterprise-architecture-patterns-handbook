# 28 — GitOps / Declarative Reconciliation

> **Famille : Déploiement** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

La configuration d'un cluster dérive lorsque les changements sont faits manuellement sans preuve ni revue.

## 2. Solution et illustration

Stocker l'état désiré dans Git, valider pull request/policies et réconcilier automatiquement ou sous approbation via contrôleur GitOps ; séparer code, configuration, secrets et preuve d'exécution.

~~~mermaid
flowchart LR
  A0["Pull Request"]
  A1["CI validate/scan"]
  A2["Git branch approuvée"]
  A3["Reconciler"]
  A4["OpenShift"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
  A3 --> A4
~~~

**Exemple de bout en bout :** Une PR change la mémoire JVM ; les tests valident le YAML puis le contrôleur applique en preprod avant promotion en prod.

## 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Auteur propose modification Git
  C->>W: CI valide schémas et politiques
  W-->>C: Revue/approbation d'architecture
  C-->>Ar: Contrôleur réconcilie cluster vers état désiré
~~~

## 4. Exemple technique (YAML partiel)

~~~yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: {name: java-api}
spec:
  project: default
  source:
    repoURL: https://git.example.invalid/team/platform.git
    targetRevision: main
    path: overlays/preprod
  destination:
    server: https://kubernetes.default.svc
    namespace: java-modernization
# Custom Resource : nécessite un contrôleur GitOps compatible.
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

## 5. Arbitrages et responsabilités

- Choisir sync auto, prune et self-heal par environnement et risque.
- Ne pas confondre ressources Kubernetes en phase desired/observed avec cohérence des données applicatives.
- Rollback Git ne défait pas une opération financière ni une migration DB non réversible.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Drift manuel | Détection, alerte, réconciliation selon politique |
| Prune involontaire | Protection ressources critiques et backup |
| Secret en Git | Secret manager/chiffrement autorisé |
| Rollback DB dangereux | Expand-Contract |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « GitOps / Declarative Reconciliation » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
