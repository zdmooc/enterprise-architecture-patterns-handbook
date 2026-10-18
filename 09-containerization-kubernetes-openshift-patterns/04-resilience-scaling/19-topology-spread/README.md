# 19 — Topology Spread / Anti-Affinity

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Trois réplicas situés sur le même nœud ou la même zone ne procurent pas une haute disponibilité physique.

## 2. Pattern et fonctionnement

Contraindre la distribution sur des failure domains indépendants et tester l'effet d'une zone indisponible.

~~~mermaid
flowchart LR
    S0["Scheduler"]
    S1["zones/nœuds distincts"]
    S2["Pods distribués"]
    S3["tolérance de panne"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
~~~

**Exemple concret :** 3 replicas Java répartis sur 3 nœuds et idéalement zones disponibles; un cluster local mono-nœud ne démontre pas ce niveau HA.

## 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Identifier labels topology réels
  K->>W: Ajouter topologySpreadConstraints
  O->>K: Observer placement via kubectl/oc
  K->>W: Simuler nœud indisponible et contrôler capacité restante
  W-->>O: Etat observé, décision de validation
~~~

## 4. Exemple YAML

~~~yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels: {app: java-api}
# Pour HA forte, envisager topology.kubernetes.io/zone si disponible.
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

## 5. Choix et contraintes d'architecture

- TopologyKey doit exister sur nœuds réels.
- DoNotSchedule peut empêcher lancement si pas assez de domaines.
- Combiner node affinity, PDB et capacity planning.

**Principale garantie :** Contraindre la distribution sur des failure domains indépendants et tester l'effet d'une zone indisponible.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Labels absents | Pod Pending : valider nœuds/labels |
| Zone entière HS | Capacité survivante dimensionnée |
| Cluster mono-nœud | Assouplir en lab, documenter HA non démontrée |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « Topology Spread / Anti-Affinity » ?** Contraindre la distribution sur des failure domains indépendants et tester l'effet d'une zone indisponible. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
