# 18 — Queue-Length Scaling / KEDA

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Des workers asynchrones doivent suivre la taille d'une file, alors que CPU ne reflète pas le travail en attente.

## 2. Pattern et fonctionnement

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

## 3. Séquence opérationnelle illustrée

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

## 4. Exemple YAML

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

## 5. Choix et contraintes d'architecture

- KEDA est une extension avec CRD, non intégrée au Kubernetes de base.
- Backlog peut grandir sans fin : capacité aval et expiration métier.
- Faire le scale-down avec drain pour ne pas perdre ACK.

**Principale garantie :** Un autoscaler externe (ex. KEDA si installé et supporté) ajuste le nombre de consumers selon backlog, avec plafond de débit aval.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Message doublé après scale down | Idempotent Consumer |
| Ordre arrivé après deadline | Refus/reconciliation, pas exécution tardive |
| Scale runaway | maxReplicaCount et quotas |
| Scaler indisponible | Backpressure et alertes |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « Queue-Length Scaling / KEDA » ?** Un autoscaler externe (ex. KEDA si installé et supporté) ajuste le nombre de consumers selon backlog, avec plafond de débit aval. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
