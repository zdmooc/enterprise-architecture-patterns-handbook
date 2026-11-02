# Cours 149 — Adapter Sidecar · Kubernetes / OpenShift

> Fil rouge : Payment API Java/Spring, virement SEPA fictif de 500 EUR. **Cours publié, corrigé théorique disponible, exercice individuel non validé.**

## 1. Objectif concret
Un composant Java historique émet des métriques au format propriétaire ; un sidecar les convertit pour Prometheus.

## 2. Architecture et flux
~~~mermaid
flowchart LR
    A["Format applicatif legacy"] --> B["Adapter Sidecar"]
    B --> C["Métriques standardisées"]
    B -.-> F["Échec ou incident"]
    F --> G["Reprise contrôlée / diagnostic"]
~~~

**Invariant à prouver :** La conversion ne modifie pas l'état ou les flux métier.

## 3. Contrat d'exploitation du pattern
- **Conception :** image, sécurité, capacités ou workload conformément aux responsabilités du composant.
- **Convergence :** Kubernetes réconcilie la configuration déclarée ; la logique financière garde sa propre source autoritative.
- **Sécurité :** identité de service minimale, SCC OpenShift, NetworkPolicy, secrets et image approuvée.
- **Limite :** La traduction d'observabilité ne doit pas devenir une dépendance bloquante du paiement.
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
2. **Test spécifique :** Introduire métrique malformée : diagnostic sans redémarrer le cœur bancaire.
3. **Sécurité :** image conforme, UID/SCC correct, secrets non exposés et réseau réduit au nécessaire.
4. **Échec :** injecter un crash ou une dépendance indisponible ; aucune nouvelle transaction bancaire aveugle.
5. **Performance :** mesurer limites CPU/mémoire, latence p95/p99, temps de redémarrage et disponibilité.
6. **Architecture :** enregistrer ADR, hypothèses de support, propriétaires des manifests et SLO.

## 6. Exercice corrigé
**Comment choisir Adapter Sidecar pour notre Payment API ?**
- **A.** Croire que Kubernetes garantit automatiquement le règlement et l'idempotence d'un paiement.
- **B.** Éviter les tests de panne et accorder cluster-admin aux pods pour simplifier les déploiements.
- **C.** Définir Adapter Sidecar, l'invariant, les contrats et prouver son fonctionnement sur un cluster de test.

**Bonne réponse théorique : C.** La conversion ne modifie pas l'état ou les flux métier.

Le corrigé est fourni pour apprendre ; aucun examen pratique ou QCM individuel n'a encore été validé pour cette fiche.

## 7. Fiche technique du référentiel (Dockerfile/YAML, schémas, tests)
Cette section conserve les détails spécifiques du pattern, y compris les extraits de manifests et les scénarios d'échec du catalogue existant.

[Source technique d'origine](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/02-pod-design/09-adapter-sidecar/README.md)

> **Famille : Pods Kubernetes.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

#### 1. Problème d'architecture

Normaliser télémétrie ou formats périphériques sans réécrire le service principal.

#### 2. Solution et fonctionnement

Un sidecar lit une sortie locale, convertit le format et transmet à un collecteur.

~~~mermaid
flowchart LR
  N0["Application logs"]
  N1["Adapter sidecar"]
  N2["schéma commun"]
  N3["Observabilité"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Un serveur Java écrit des logs applicatifs structurés; un adapter ancien convertit les champs pour l'outil d'exploitation.

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
volumes:
  - name: telemetry-buffer
    emptyDir:
      sizeLimit: 100Mi
# Si un adapter est justifié, limiter les permissions et la taille.
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

#### 4. Principaux arbitrages

- Éviter traitement de données personnelles hors contrat.
- préférer stdout+collector si possible.
- tampon borné et pas de blocage..

#### 5. Invariant et critères de choix

**À démontrer :** Un échec de normalisation de logs ne doit pas bloquer le paiement.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

#### 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Fichier mal formé | Quarantaine des lignes |
| Disque plein | Buffer borné / rotation |
| Données sensibles | Masquage et minimisation |

#### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

#### 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Adapter / Log Format Normalization » ? **Réponse :** Un sidecar lit une sortie locale, convertit le format et transmet à un collecteur. **Preuve requise :** Un échec de normalisation de logs ne doit pas bloquer le paiement.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/README.md) · [références officielles](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au parcours](README.md)
