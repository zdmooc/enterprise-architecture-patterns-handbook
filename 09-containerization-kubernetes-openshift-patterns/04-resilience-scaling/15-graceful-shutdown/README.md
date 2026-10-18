# 15 — Graceful Shutdown / Drain

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Une mise à jour ou éviction SIGTERM peut interrompre une requête critique ou perdre une unité de travail.

## 2. Pattern et fonctionnement

L'application doit arrêter d'accepter de nouveaux travaux, drainer les requêtes en cours, préserver/réconcilier les opérations durables et quitter avant terminationGracePeriodSeconds.

~~~mermaid
flowchart LR
    S0["SIGTERM"]
    S1["readiness false"]
    S2["drain in-flight"]
    S3["checkpoint/ack"]
    S4["exit"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
~~~

**Exemple concret :** Lors d'une mise à jour d'API Java, le Pod sort des endpoints, termine les requêtes encore en vol et conserve les références d'ordres en DB.

## 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Pod passe en terminaison
  K->>W: Application reçoit SIGTERM et stoppe admission
  O->>K: Travaux durables sont finis ou marqués à reprendre
  K->>W: Pod sort avant fin de grace period
  W-->>O: Etat observé, décision de validation
~~~

## 4. Exemple YAML

~~~yaml
spec:
  terminationGracePeriodSeconds: 60
  containers:
    - name: java
      image: registry.example.invalid/team/java-api@sha256:<DIGEST>
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "sleep 5"]
# Le shell/sleep peut manquer dans une image distroless.
# Le code applicatif doit réellement gérer SIGTERM.
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

## 5. Choix et contraintes d'architecture

- Mesurer durée d'un in-flight et délai de propagation réseau.
- preStop peut aider au drain mais consomme grace period.
- SIGKILL possible : l'idempotence/recovery reste obligatoire.

**Principale garantie :** L'application doit arrêter d'accepter de nouveaux travaux, drainer les requêtes en cours, préserver/réconcilier les opérations durables et quitter avant terminationGracePeriodSeconds.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Requête encore en vol | Conserver intention durable/reconcilier |
| Grace period expirée | SIGKILL : replay idempotent |
| MQ ACK fait trop tôt | ACK seulement après transaction métier cohérente |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « Graceful Shutdown / Drain » ?** L'application doit arrêter d'accepter de nouveaux travaux, drainer les requêtes en cours, préserver/réconcilier les opérations durables et quitter avant terminationGracePeriodSeconds. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
