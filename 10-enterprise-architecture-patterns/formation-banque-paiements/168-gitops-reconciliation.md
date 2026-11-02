# Cours 168 — GitOps Reconciliation · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
OpenShift GitOps/Argo CD doit maintenir les manifests approuvés et détecter une dérive opérationnelle.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Git : état déclaré"] --> B["Argo CD / contrôle et drift"]
    B --> C["OpenShift : état observé"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** Une modification non approuvée est détectée et traitée selon politique sync/self-heal/prune.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** GitOps synchronise le déploiement, pas la base SQL ni une transaction financière.

## 4. Séquence de fonctionnement et reprise
~~~mermaid
sequenceDiagram
    participant O as Exploitant / GitOps
    participant K as Kubernetes / OpenShift
    participant A as Payment API
    participant C as Core autoritatif
    O->>K: demander état désiré ou bascule
    K->>A: exposer / configurer / remplacer workload
    A->>C: soumettre ou consulter via référence stable
    C--xA: réponse perdue possible
    A->>C: retrouver l'état du paiement
    C-->>A: résultat attesté ou UNKNOWN
    K-->>O: conditions, alertes et métriques
~~~

## 5. Tests à présenter en Design Authority
1. Démonstration nominale des objets Kubernetes, politiques et versions.
2. **Test spécifique :** Modifier une ConfigMap en cluster et vérifier la détection et correction contrôlée de dérive.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour GitOps Reconciliation ?**
- **A.** Mettre en œuvre GitOps Reconciliation en démontrant l'invariant par un test contrôlé.
- **B.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **C.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.

**Bonne réponse théorique : A.** Une modification non approuvée est détectée et traitée selon politique sync/self-heal/prune.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/06-gitops-delivery/28-gitops-reconciliation/README.md)

> **Famille : Déploiement** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

La configuration d'un cluster dérive lorsque les changements sont faits manuellement sans preuve ni revue.

#### 2. Solution et illustration

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

#### 3. Séquence d'exploitation

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

#### 4. Exemple technique (YAML partiel)

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

#### 5. Arbitrages et responsabilités

- Choisir sync auto, prune et self-heal par environnement et risque.
- Ne pas confondre ressources Kubernetes en phase desired/observed avec cohérence des données applicatives.
- Rollback Git ne défait pas une opération financière ni une migration DB non réversible.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Drift manuel | Détection, alerte, réconciliation selon politique |
| Prune involontaire | Protection ressources critiques et backup |
| Secret en Git | Secret manager/chiffrement autorisé |
| Rollback DB dangereux | Expand-Contract |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « GitOps / Declarative Reconciliation » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
