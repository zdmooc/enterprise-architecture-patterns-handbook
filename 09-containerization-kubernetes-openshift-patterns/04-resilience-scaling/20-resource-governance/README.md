# 20 — Requests / Limits / LimitRange / ResourceQuota

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Sans réservation, limitations et quotas, un tenant peut évincer les autres ou surconsommer CPU/mémoire.

## 2. Pattern et fonctionnement

Requests guident scheduler et QoS ; limits bornent consommation (CPU throttling, mémoire OOMKill) ; quotas gouvernent le namespace.

~~~mermaid
flowchart LR
    S0["Mesures JVM"]
    S1["requests/limits"]
    S2["Scheduler & cgroups"]
    S3["alertes throttling/OOM"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
~~~

**Exemple concret :** Un service Java demande 250m CPU et 512Mi RAM, plafonne mémoire à 768Mi après mesure de heap/native memory.

## 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Profiler heap + native + threads
  K->>W: Configurer requests et limites
  O->>K: Tester GC/latence p99 sous quota
  K->>W: Surveiller throttling, OOMKill, QoS
  W-->>O: Etat observé, décision de validation
~~~

## 4. Exemple YAML

~~~yaml
resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    memory: 768Mi
# CPU limit optionnel selon politique du cluster et preuve p99.
# Heap JVM à dimensionner < limite conteneur.
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

## 5. Choix et contraintes d'architecture

- Dimensionner JVM heap + metaspace + direct buffers à l'intérieur de la limite.
- CPU limits peuvent provoquer throttling néfaste pour faible latence.
- ResourceQuota et LimitRange doivent correspondre aux besoins du projet.

**Principale garantie :** Requests guident scheduler et QoS ; limits bornent consommation (CPU throttling, mémoire OOMKill) ; quotas gouvernent le namespace.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| OOMKill JVM | Augmenter budget ou réduire heap, diagnostiquer native |
| CPU throttling | Mesurer p99 et limites |
| Quota namespace saturé | Budget/alertes/housekeeping |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « Requests / Limits / LimitRange / ResourceQuota » ?** Requests guident scheduler et QoS ; limits bornent consommation (CPU throttling, mémoire OOMKill) ; quotas gouvernent le namespace. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
