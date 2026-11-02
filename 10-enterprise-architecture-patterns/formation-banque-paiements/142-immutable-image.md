# Cours 142 — Immutable Image / Digest · Kubernetes / OpenShift

> Fil rouge : Payment API Java/Spring, virement SEPA fictif de 500 EUR. **Cours publié, corrigé théorique disponible, exercice individuel non validé.**

## 1. Objectif concret
Le même binaire du Payment API doit être promu de préproduction en production sans reconstruction ni surprise liée à un tag mutable.

## 2. Architecture et flux
~~~mermaid
flowchart LR
    A["Commit / image construite"] --> B["Digest OCI immuable"]
    B --> C["Promotion de l'image identique"]
    B -.-> F["Échec ou incident"]
    F --> G["Reprise contrôlée / diagnostic"]
~~~

**Invariant à prouver :** Le digest validé en tests est le digest réellement déployé.

## 3. Contrat d'exploitation du pattern
- **Conception :** image, sécurité, capacités ou workload conformément aux responsabilités du composant.
- **Convergence :** Kubernetes réconcilie la configuration déclarée ; la logique financière garde sa propre source autoritative.
- **Sécurité :** identité de service minimale, SCC OpenShift, NetworkPolicy, secrets et image approuvée.
- **Limite :** Un digest prouve l'identité des octets, pas leur sûreté ni la conformité.
- **Preuves :** versions du cluster et opérateurs, manifests validés, tests runtime et ADR de conception.

## 4. Séquence d'incident à expliquer
~~~mermaid
sequenceDiagram
    participant O as Opérateur / GitOps
    participant K as Kubernetes API
    participant W as Workload Java
    participant S as Service financier autoritatif
    O->>K: appliquer état désiré du pattern
    K->>W: créer ou réconcilier le Pod
    W-->>K: readiness / anomalie
    Note over W,S: Panne de pod ou perte de confirmation
    W->>S: rechercher l'état par référence stable
    S-->>W: statut attesté ou UNKNOWN
    K-->>O: conditions et preuves observées
~~~

## 5. Tests d'architecture
1. **Nominal :** comparer état désiré, ressources effectivement créées et source métier des données.
2. **Test spécifique :** Déplacer le tag vers un autre digest : détection de dérive et refus si signature/provenance non conformes.
3. **Sécurité :** image conforme, UID/SCC correct, secrets non exposés et réseau réduit au nécessaire.
4. **Échec :** injecter un crash ou une dépendance indisponible ; aucune nouvelle transaction bancaire aveugle.
5. **Performance :** mesurer limites CPU/mémoire, latence p95/p99, temps de redémarrage et disponibilité.
6. **Architecture :** enregistrer ADR, hypothèses de support, propriétaires des manifests et SLO.

## 6. Exercice corrigé
**Comment choisir Immutable Image / Digest pour notre Payment API ?**
- **A.** Croire que Kubernetes garantit automatiquement le règlement et l'idempotence d'un paiement.
- **B.** Définir Immutable Image / Digest, l'invariant, les contrats et prouver son fonctionnement sur un cluster de test.
- **C.** Éviter les tests de panne et accorder cluster-admin aux pods pour simplifier les déploiements.

**Bonne réponse théorique : B.** Le digest validé en tests est le digest réellement déployé.

Le corrigé est fourni pour apprendre ; aucun examen pratique ou QCM individuel n'a encore été validé pour cette fiche.

## 7. Fiche technique du référentiel (Dockerfile/YAML, schémas, tests)
Cette section conserve les détails spécifiques du pattern, y compris les extraits de manifests et les scénarios d'échec du catalogue existant.

[Source technique d'origine](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/01-container-design/02-immutable-image/README.md)

> **Famille : Conteneurisation.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

#### 1. Problème d'architecture

Éviter les déploiements divergents causés par une image mutable.

#### 2. Solution et fonctionnement

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

#### Séquence de mise en place

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

#### 3. Implémentation indicative (yaml)

~~~yaml
containers:
  - name: payments-api
    image: registry.example.invalid/team/payments-api@sha256:<DIGEST_VALIDÉ>
    imagePullPolicy: IfNotPresent
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

#### 4. Principaux arbitrages

- Build provenance documentée.
- référence digest au déploiement.
- config et secrets séparés..

#### 5. Invariant et critères de choix

**À démontrer :** Un nouveau Pod peut reproduire les mêmes binaires de l'image de référence.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

#### 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Tag latest a changé | Déployer par digest |
| Image supprimée | Gérer rétention/miroir de registry |
| Rollback bloqué par DB schema | Expand-contract et tests des contrats |

#### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

#### 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Immutable Image / Pinning » ? **Réponse :** Construire une image une fois, la promouvoir entre environnements par digest et ne pas modifier son contenu au runtime. **Preuve requise :** Un nouveau Pod peut reproduire les mêmes binaires de l'image de référence.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/README.md) · [références officielles](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au parcours](README.md)
