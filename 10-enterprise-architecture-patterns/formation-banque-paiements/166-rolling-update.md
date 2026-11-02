# Cours 166 — Rolling Update · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
La Payment API évolue sans interruption programmée et sans changement simultané incompatible des contrats.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Deployment révision N"] --> B["RollingUpdate et readiness"]
    B --> C["Pods N+1 disponibles"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** Une mise à jour remplace les pods dans les budgets sans interrompre les traitements acceptés.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** RollingUpdate n'annule pas un changement de schéma SQL irréversible.

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
2. **Test spécifique :** Déployer version incompatible, puis rollback technique : aucune perte ou duplication d'ordre.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour Rolling Update ?**
- **A.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **B.** Mettre en œuvre Rolling Update en démontrant l'invariant par un test contrôlé.
- **C.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.

**Bonne réponse théorique : B.** Une mise à jour remplace les pods dans les budgets sans interrompre les traitements acceptés.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/06-gitops-delivery/26-rolling-update/README.md)

> **Famille : Déploiement** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Une mise à jour Java ne doit pas interrompre toutes les répliques à la fois.

#### 2. Solution et illustration

Deployment RollingUpdate crée progressivement les nouveaux Pods et retire les anciens selon maxSurge/maxUnavailable, readiness, capacité et drain; zéro indisponibilité n'est pas garanti sans tests.

~~~mermaid
flowchart LR
  A0["Image v2"]
  A1["Pod v2 ready"]
  A2["trafic partagé"]
  A3["Pod v1 drain"]
  A4["fin rollout"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
  A3 --> A4
~~~

**Exemple de bout en bout :** 3 replicas Java, maxUnavailable 0, maxSurge 1 ; la nouvelle image est ajoutée puis promue lorsque ready.

#### 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Publier image OCI immuable
  C->>W: Mise à jour du Deployment
  W-->>C: Attendre nouvelles probes ready
  C-->>Ar: Désaffecter ancien Pod avec graceful shutdown
~~~

#### 4. Exemple technique (YAML partiel)

~~~yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
minReadySeconds: 5
progressDeadlineSeconds: 240
# Champs sous spec du Deployment.
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

#### 5. Arbitrages et responsabilités

- maxUnavailable 0 implique ressources pour surge.
- Readiness réelle et terminationGracePeriodSeconds nécessaires.
- Compatibilité DB, API, événements entre versions durant chevauchement.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Nouvelle image défectueuse | ProgressDeadline/rollback |
| DB migrée incompatible | Expand/Contract avant rollout |
| Surge impossible quota | Capacity planning |
| SIGTERM interrompt ordre | Drain + idempotence |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « Rolling Update / Zero-Downtime Candidate » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
