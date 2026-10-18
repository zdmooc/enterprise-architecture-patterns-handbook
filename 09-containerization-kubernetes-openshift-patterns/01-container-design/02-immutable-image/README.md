# 02 — Immutable Image / Pinning

> **Famille : Conteneurisation.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Éviter les déploiements divergents causés par une image mutable.

## 2. Solution et fonctionnement

Construire une image une fois, la promouvoir entre environnements par digest et ne pas modifier son contenu au runtime.

~~~mermaid
flowchart LR
  N0["Git commit"]
  N1["image signée"]
  N2["registry"]
  N3["test"]
  N4["préprod"]
  N5["prod"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
~~~

**Exemple métier :** La version 1.0 d'un service Java est identique en test, préproduction et production grâce au digest OCI.

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
containers:
  - name: payments-api
    image: registry.example.invalid/team/payments-api@sha256:<DIGEST_VALIDÉ>
    imagePullPolicy: IfNotPresent
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Build provenance documentée.
- référence digest au déploiement.
- config et secrets séparés..

## 5. Invariant et critères de choix

**À démontrer :** Un nouveau Pod peut reproduire les mêmes binaires de l'image de référence.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Tag latest a changé | Déployer par digest |
| Image supprimée | Gérer rétention/miroir de registry |
| Rollback bloqué par DB schema | Expand-contract et tests des contrats |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Immutable Image / Pinning » ? **Réponse :** Construire une image une fois, la promouvoir entre environnements par digest et ne pas modifier son contenu au runtime. **Preuve requise :** Un nouveau Pod peut reproduire les mêmes binaires de l'image de référence.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
