# 26 — Rolling Update / Zero-Downtime Candidate

> **Famille : Déploiement** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Une mise à jour Java ne doit pas interrompre toutes les répliques à la fois.

## 2. Solution et illustration

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

## 3. Séquence d'exploitation

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

## 4. Exemple technique (YAML partiel)

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

## 5. Arbitrages et responsabilités

- maxUnavailable 0 implique ressources pour surge.
- Readiness réelle et terminationGracePeriodSeconds nécessaires.
- Compatibilité DB, API, événements entre versions durant chevauchement.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Nouvelle image défectueuse | ProgressDeadline/rollback |
| DB migrée incompatible | Expand/Contract avant rollout |
| Surge impossible quota | Capacity planning |
| SIGTERM interrompt ordre | Drain + idempotence |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « Rolling Update / Zero-Downtime Candidate » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
