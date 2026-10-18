# 11 — StatefulSet / Stable Identity

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Une base ou un broker exige identité DNS et volumes persistants propres à chaque réplica.

## 2. Pattern et fonctionnement

StatefulSet attribue une identité ordinale stable et des PVC distincts ; **il ne fournit pas à lui seul réplication, quorum, sauvegarde ou tolérance de panne**.

~~~mermaid
flowchart LR
    S0["Service headless"]
    S1["StatefulSet"]
    S2["pod-0 / PVC-0"]
    S3["pod-1 / PVC-1"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
~~~

**Exemple concret :** Trois instances d'un stockage fictif ont un nom pod-0/1/2 et des PVC indépendants, mais leur consensus est géré par le logiciel ou son Operator.

## 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Déclarer headless Service
  K->>W: Créer StatefulSet et PVC
  O->>K: Orchestrateur de données forme quorum
  K->>W: Tester perte d'un nœud et restaurer
  W-->>O: Etat observé, décision de validation
~~~

## 4. Exemple YAML

~~~yaml
apiVersion: apps/v1
kind: StatefulSet
metadata: {name: datastore}
spec:
  serviceName: datastore-headless
  replicas: 3
  selector: {matchLabels: {app: datastore}}
  template:
    metadata: {labels: {app: datastore}}
    spec:
      containers:
        - name: store
          image: registry.example.invalid/stateful/store@sha256:<DIGEST>
          volumeMounts: [{name: data, mountPath: /data}]
  volumeClaimTemplates:
    - metadata: {name: data}
      spec:
        accessModes: [ReadWriteOnce]
        resources: {requests: {storage: 10Gi}}
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

## 5. Choix et contraintes d'architecture

- Stable identity et PVC sont réellement nécessaires ; sinon Deployment.
- StorageClass/RWX/RWO, snapshots et expansion selon CSI.
- Politique de réplication applicative et sauvegarde indépendantes du StatefulSet.

**Principale garantie :** StatefulSet attribue une identité ordinale stable et des PVC distincts ; **il ne fournit pas à lui seul réplication, quorum, sauvegarde ou tolérance de panne**.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| PVC indisponible | Restaurer ou réparer storage, sans forcer double attachement |
| Site perdu | DR validé par applicatif, pas par StatefulSet seul |
| Rolling update bloque | Canary ordinal/partition, plan de reprise |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « StatefulSet / Stable Identity » ?** StatefulSet attribue une identité ordinale stable et des PVC distincts ; **il ne fournit pas à lui seul réplication, quorum, sauvegarde ou tolérance de panne**. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
