# Cours 158 — Queue-Based Scaling · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
Le backlog des messages MQ monte mais la CPU des consumers reste faible ; scaler uniquement sur CPU serait inadapté.

**Invariant à préserver :** Le scaling sur files respecte l'échéance métier, l'ordre de traitement et l'idempotence.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["Queue depth / oldest age"] --> B["Autoscaler par file"]
    B --> C["Consumers concurrents"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : Un scaling trop agressif augmente contention MQ/DB ; garder backpressure et plafonds.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern Queue-Based Scaling
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Créer backlog puis mesurer drain ; arrêter le core et vérifier que l'augmentation de pods n'aggrave pas la panne.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à Queue-Based Scaling ?**
- **A.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **B.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.
- **C.** Définir Queue-Based Scaling, ses limites et ses tests de reprise sur OpenShift.

**Bonne réponse théorique : C.** Le scaling sur files respecte l'échéance métier, l'ordre de traitement et l'idempotence.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/04-resilience-scaling/18-queue-based-scaling/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Des workers asynchrones doivent suivre la taille d'une file, alors que CPU ne reflète pas le travail en attente.

#### 2. Pattern et fonctionnement

Un autoscaler externe (ex. KEDA si installé et supporté) ajuste le nombre de consumers selon backlog, avec plafond de débit aval.

~~~mermaid
flowchart LR
    S0["Queue depth"]
    S1["Scaler externe"]
    S2["Deployment consumers"]
    S3["Messages traités"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
~~~

**Exemple concret :** Un worker documentaire consomme des jobs depuis une file ; sa charge augmente. Une queue de paiement ne doit pas déclencher traitement d'ordres expirés.

#### 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Mesurer backlog et oldest-message-age
  K->>W: Renseigner TriggerAuthentication
  O->>K: Fixer maxReplicas selon limite de la cible
  K->>W: Contrôler deadline et déduplication sur chaque message
  W-->>O: Etat observé, décision de validation
~~~

#### 4. Exemple YAML

~~~yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata: {name: worker-scale}
spec:
  scaleTargetRef: {name: worker}
  minReplicaCount: 1
  maxReplicaCount: 8
  triggers:
    - type: prometheus
      metadata:
        serverAddress: https://metrics.example.invalid
        metricName: work_queue_depth
        threshold: "20"
        query: sum(work_queue_depth)
# CRD optionnelle : installer et autoriser l'autoscaler compatible.
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

#### 5. Choix et contraintes d'architecture

- KEDA est une extension avec CRD, non intégrée au Kubernetes de base.
- Backlog peut grandir sans fin : capacité aval et expiration métier.
- Faire le scale-down avec drain pour ne pas perdre ACK.

**Principale garantie :** Un autoscaler externe (ex. KEDA si installé et supporté) ajuste le nombre de consumers selon backlog, avec plafond de débit aval.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Message doublé après scale down | Idempotent Consumer |
| Ordre arrivé après deadline | Refus/reconciliation, pas exécution tardive |
| Scale runaway | maxReplicaCount et quotas |
| Scaler indisponible | Backpressure et alertes |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « Queue-Length Scaling / KEDA » ?** Un autoscaler externe (ex. KEDA si installé et supporté) ajuste le nombre de consumers selon backlog, avec plafond de débit aval. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
