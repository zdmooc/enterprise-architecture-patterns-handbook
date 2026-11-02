# Cours 148 — Ambassador · Kubernetes / OpenShift

> Fil rouge : Payment API Java/Spring, virement SEPA fictif de 500 EUR. **Cours publié, corrigé théorique disponible, exercice individuel non validé.**

## 1. Objectif concret
La Payment API utilise un proxy réseau local pour accéder à une dépendance externe derrière TLS et une politique de connexion.

## 2. Architecture et flux
~~~mermaid
flowchart LR
    A["App Java sur localhost"] --> B["Proxy Ambassador"]
    B --> C["Dépendance distante autorisée"]
    B -.-> F["Échec ou incident"]
    F --> G["Reprise contrôlée / diagnostic"]
~~~

**Invariant à prouver :** L'application reste isolée des détails de connexion sans élargir ses autorisations.

## 3. Contrat d'exploitation du pattern
- **Conception :** image, sécurité, capacités ou workload conformément aux responsabilités du composant.
- **Convergence :** Kubernetes réconcilie la configuration déclarée ; la logique financière garde sa propre source autoritative.
- **Sécurité :** identité de service minimale, SCC OpenShift, NetworkPolicy, secrets et image approuvée.
- **Limite :** Le proxy ne remplace ni l'autorisation métier ni l'idempotence de l'appel distant.
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
2. **Test spécifique :** Couper le proxy ou fournir une mauvaise CA : refus propre et statut métier non inventé.
3. **Sécurité :** image conforme, UID/SCC correct, secrets non exposés et réseau réduit au nécessaire.
4. **Échec :** injecter un crash ou une dépendance indisponible ; aucune nouvelle transaction bancaire aveugle.
5. **Performance :** mesurer limites CPU/mémoire, latence p95/p99, temps de redémarrage et disponibilité.
6. **Architecture :** enregistrer ADR, hypothèses de support, propriétaires des manifests et SLO.

## 6. Exercice corrigé
**Comment choisir Ambassador pour notre Payment API ?**
- **A.** Croire que Kubernetes garantit automatiquement le règlement et l'idempotence d'un paiement.
- **B.** Définir Ambassador, l'invariant, les contrats et prouver son fonctionnement sur un cluster de test.
- **C.** Éviter les tests de panne et accorder cluster-admin aux pods pour simplifier les déploiements.

**Bonne réponse théorique : B.** L'application reste isolée des détails de connexion sans élargir ses autorisations.

Le corrigé est fourni pour apprendre ; aucun examen pratique ou QCM individuel n'a encore été validé pour cette fiche.

## 7. Fiche technique du référentiel (Dockerfile/YAML, schémas, tests)
Cette section conserve les détails spécifiques du pattern, y compris les extraits de manifests et les scénarios d'échec du catalogue existant.

[Source technique d'origine](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/02-pod-design/08-ambassador/README.md)

> **Famille : Pods Kubernetes.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

#### 1. Problème d'architecture

Découpler le protocole externe de l'application sans contaminer son code.

#### 2. Solution et fonctionnement

Un proxy local dans le Pod gère TLS, retries de connexion autorisés ou adaptation au protocole externe.

~~~mermaid
flowchart LR
  N0["Java"]
  N1["localhost ambassador"]
  N2["mTLS"]
  N3["service externe"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Le Java ne voit que localhost:15001; le proxy se connecte à un service externe authentifié. Les retries de mutations financières restent interdits sans idempotence.

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
  - name: legacy-proxy
    image: registry.example.invalid/tools/proxy:stable
    ports:
      - containerPort: 15001
    resources:
      requests: {cpu: 50m, memory: 64Mi}
      limits: {memory: 128Mi}
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

#### 4. Principaux arbitrages

- Confirmer nécessité réelle du sidecar contre service mesh/gateway.
- gérer certificats, ports, timeout, observabilité et erreurs..

#### 5. Invariant et critères de choix

**À démontrer :** Le proxy n'invente pas de statut métier en cas de timeout.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

#### 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Certificat expiré | Rotation et alerte |
| Proxy répond 503 | Le service métier ne conclut pas à rejet |
| Retry dangereux | Désactiver sur opérations à effet sans idempotence |

#### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

#### 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Ambassador / Local Proxy » ? **Réponse :** Un proxy local dans le Pod gère TLS, retries de connexion autorisés ou adaptation au protocole externe. **Preuve requise :** Le proxy n'invente pas de statut métier en cas de timeout.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/README.md) · [références officielles](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au parcours](README.md)
