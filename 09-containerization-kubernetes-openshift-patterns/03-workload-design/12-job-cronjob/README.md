# 12 — Job / CronJob

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Une tâche finie ou périodique n'est pas un serveur permanent : sa reprise et sa politique de concurrence doivent être explicites.

## 2. Pattern et fonctionnement

Job exécute un traitement jusqu'à complétion, CronJob crée des Jobs selon calendrier ; aucune garantie universelle d'exécution exactement une fois.

~~~mermaid
flowchart LR
    S0["Calendrier"]
    S1["CronJob"]
    S2["Job"]
    S3["Pod"]
    S4["Rapport durable"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
~~~

**Exemple concret :** Générer chaque nuit un rapport d'écarts en lecture seule, avec verrou métier pour empêcher des rapports simultanés.

## 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Configurer calendrier et fuseau
  K->>W: Lancer Job avec backoffLimit
  O->>K: Enregistrer état/résultat idempotent
  K->>W: Vérifier missed schedules et concurrence
  W-->>O: Etat observé, décision de validation
~~~

## 4. Exemple YAML

~~~yaml
apiVersion: batch/v1
kind: CronJob
metadata: {name: reconciliation-report}
spec:
  schedule: "0 2 * * *"
  timeZone: "Etc/UTC"
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: report
              image: registry.example.invalid/tools/report@sha256:<DIGEST>
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

## 5. Choix et contraintes d'architecture

- concurrencyPolicy Forbid / Replace / Allow à choisir.
- Deadline, retries, TTL d'historique et stockage du résultat.
- La tâche doit être idempotente même si un Job est relancé.

**Principale garantie :** Job exécute un traitement jusqu'à complétion, CronJob crée des Jobs selon calendrier ; aucune garantie universelle d'exécution exactement une fois.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Job relancé | Déduplication par date+type |
| Horloge/décalage DST | Fuseau et fenêtres de traitement définis |
| Run dépasse cadence | Forbid et alerting |
| Pod tué | Checkpoint/reprise |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « Job / CronJob » ?** Job exécute un traitement jusqu'à complétion, CronJob crée des Jobs selon calendrier ; aucune garantie universelle d'exécution exactement une fois. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
