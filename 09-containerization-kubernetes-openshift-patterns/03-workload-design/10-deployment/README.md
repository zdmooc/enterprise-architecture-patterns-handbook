# 10 — Deployment / ReplicaSet

> **Famille : Workloads Kubernetes.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Maintenir N instances interchangeables d'un service sans état.

## 2. Solution et fonctionnement

Déclaration du nombre de replicas, stratégie RollingUpdate et sélecteurs stables.

~~~mermaid
flowchart LR
  N0["Deployment"]
  N1["ReplicaSet"]
  N2["Pods"]
  N3["Service"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Le service de consultation Java passe à 3 replicas répartis sur plusieurs workers et reste exposé via Service.

### Séquence de mise en place

~~~mermaid
sequenceDiagram
  actor A as Architecte / Exploitant
  participant G as Plateforme
  participant W as Workload
  A->>G: Déclarer la configuration du pattern
  G->>W: Réconcilier et démarrer
  W-->>G: Etat de readiness / observation
  G-->>A: Indicateur ou anomalie à corriger
~~~

## 3. Implémentation indicative (yaml)

~~~yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: app-api}
spec:
  replicas: 3
  selector: {matchLabels: {app: app-api}}
  template:
    metadata: {labels: {app: app-api}}
    spec:
      containers:
        - name: app
          image: registry.example.invalid/team/app@sha256:<DIGEST>
          ports: [{containerPort: 8080}]
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Configurer requests/limits, startup/readiness/liveness, selectors sans collision, PDB et topology spread..

## 5. Invariant et critères de choix

**À démontrer :** La perte d'un seul Pod n'interrompt pas le service si capacité restante suffisante.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Replica indisponible | Readiness exclut du trafic |
| Node perdu | Replicas multi-zone |
| Build défectueux | Rollback image avec état de DB compatible |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Deployment / ReplicaSet » ? **Réponse :** Déclaration du nombre de replicas, stratégie RollingUpdate et sélecteurs stables. **Preuve requise :** La perte d'un seul Pod n'interrompt pas le service si capacité restante suffisante.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
