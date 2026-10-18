# 16 — PodDisruptionBudget (PDB)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Une opération de maintenance risque d'évincer trop de Pods d'une capacité répliquée.

## 2. Pattern et fonctionnement

Le PDB limite les évictions **volontaires** prises en compte par l'Eviction API ; ne protège pas des pannes de nœud ou site.

~~~mermaid
flowchart LR
    S0["Maintenance de nœud"]
    S1["Eviction API"]
    S2["PDB check"]
    S3["Pods restants"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
~~~

**Exemple concret :** Une API Java à 3 replicas exige au moins 2 disponibles durant un drain planifié.

## 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Définir minAvailable cohérent avec replicas
  K->>W: Demander drain par Eviction API
  O->>K: PDB autorise ou bloque eviction
  K->>W: Vérifier disponibilité réelle sous maintenance
  W-->>O: Etat observé, décision de validation
~~~

## 4. Exemple YAML

~~~yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: {name: java-api-pdb}
spec:
  minAvailable: 2
  selector:
    matchLabels: {app: java-api}
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

## 5. Choix et contraintes d'architecture

- PDB doit être aligné sur replicas et capacité des zones.
- minAvailable 2 sur replicas 2 peut bloquer toutes les évictions.
- HA nécessite topology spread et capacité, pas PDB seulement.

**Principale garantie :** Le PDB limite les évictions **volontaires** prises en compte par l'Eviction API ; ne protège pas des pannes de nœud ou site.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Drain impossible | PDB trop contraignant : fenêtre et capacité supplémentaires |
| Nœud panne brutale | PDB n'aide pas : réplication/zones |
| Aucune readiness | PDB ne remplace pas les sondes correctes |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « PodDisruptionBudget (PDB) » ?** Le PDB limite les évictions **volontaires** prises en compte par l'Eviction API ; ne protège pas des pannes de nœud ou site. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
