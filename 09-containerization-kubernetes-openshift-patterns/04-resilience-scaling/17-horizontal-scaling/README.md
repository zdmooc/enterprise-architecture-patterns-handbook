# 17 — HPA / Horizontal Pod Autoscaling

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Une montée de trafic met en saturation les replicas applicatifs.

## 2. Pattern et fonctionnement

HPA ajuste le nombre de replicas selon métriques CPU, mémoire ou métriques custom/external ; ne dépasse pas les capacités réelles des dépendances.

~~~mermaid
flowchart LR
    S0["Metrics Server"]
    S1["HPA controller"]
    S2["Deployment replicas"]
    S3["Pods"]
    S4["Service"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
~~~

**Exemple concret :** L'API Java passe de 2 à 5 replicas selon CPU sous réserve de la capacité DB/Core ; le seuil est calibré après campagne de charge.

## 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Mesurer charge et requests CPU
  K->>W: Configurer min/max replicas et cible
  O->>K: Observer HPA sous charge
  K->>W: Vérifier DB/pools et délai scale-out
  W-->>O: Etat observé, décision de validation
~~~

## 4. Exemple YAML

~~~yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: java-api-hpa}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: java-api
  minReplicas: 2
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: {type: Utilization, averageUtilization: 65}
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

## 5. Choix et contraintes d'architecture

- CPU utilization suppose requests définis.
- Autoscaling change le nombre de Pods, pas le débit core externe.
- Stabilization windows évitent oscillations.

**Principale garantie :** HPA ajuste le nombre de replicas selon métriques CPU, mémoire ou métriques custom/external ; ne dépasse pas les capacités réelles des dépendances.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| DB saturée | Limiter maxReplicas et pool |
| Métriques manquantes | HPA incapable de scaler correctement |
| Cold start Java | Prévoir buffer et replicas minimum |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « HPA / Horizontal Pod Autoscaling » ?** HPA ajuste le nombre de replicas selon métriques CPU, mémoire ou métriques custom/external ; ne dépasse pas les capacités réelles des dépendances. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
