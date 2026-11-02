# Cours 152 — Job / CronJob · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
Un rapprochement quotidien de statuts doit être exécuté de façon contrôlée sans le lier au cycle de vie de l'API.

**Invariant à préserver :** Un Job peut être relancé ou exécuté plus d'une fois ; effet métier idempotent indispensable.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["CronJob / programmation"] --> B["Job à état explicite"]
    B --> C["Résultat durable de rapprochement"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : Un CronJob n'est pas un orchestrateur transactionnel et n'offre pas du exactly once.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern Job / CronJob
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Introduire redémarrage, overlap et missed schedule : vérifier aucune double correction financière.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à Job / CronJob ?**
- **A.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **B.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.
- **C.** Définir Job / CronJob, ses limites et ses tests de reprise sur OpenShift.

**Bonne réponse théorique : C.** Un Job peut être relancé ou exécuté plus d'une fois ; effet métier idempotent indispensable.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/03-workload-design/12-job-cronjob/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Une tâche finie ou périodique n'est pas un serveur permanent : sa reprise et sa politique de concurrence doivent être explicites.

#### 2. Pattern et fonctionnement

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

#### 3. Séquence opérationnelle illustrée

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

#### 4. Exemple YAML

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

#### 5. Choix et contraintes d'architecture

- concurrencyPolicy Forbid / Replace / Allow à choisir.
- Deadline, retries, TTL d'historique et stockage du résultat.
- La tâche doit être idempotente même si un Job est relancé.

**Principale garantie :** Job exécute un traitement jusqu'à complétion, CronJob crée des Jobs selon calendrier ; aucune garantie universelle d'exécution exactement une fois.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Job relancé | Déduplication par date+type |
| Horloge/décalage DST | Fuseau et fenêtres de traitement définis |
| Run dépasse cadence | Forbid et alerting |
| Pod tué | Checkpoint/reprise |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « Job / CronJob » ?** Job exécute un traitement jusqu'à complétion, CronJob crée des Jobs selon calendrier ; aucune garantie universelle d'exécution exactement une fois. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
