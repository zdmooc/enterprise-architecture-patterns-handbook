# Cours 155 — Graceful Shutdown · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
Pendant un RollingUpdate, un pod Java en cours d'envoi MQ reçoit SIGTERM alors qu'une commande est en cours.

**Invariant à préserver :** Un arrêt ne coupe pas silencieusement une transaction métier ni ne crée de deuxième effet.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["SIGTERM + retrait readiness"] --> B["Drain des traitements"]
    B --> C["Arrêt contrôlé du pod"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : Un preStop et une terminationGracePeriodSeconds trop courts entraînent des requêtes interrompues.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern Graceful Shutdown
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Envoyer SIGTERM au milieu d'une requête : vérifier drain, timeout et reprise par référence stable.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à Graceful Shutdown ?**
- **A.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **B.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.
- **C.** Définir Graceful Shutdown, ses limites et ses tests de reprise sur OpenShift.

**Bonne réponse théorique : C.** Un arrêt ne coupe pas silencieusement une transaction métier ni ne crée de deuxième effet.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/04-resilience-scaling/15-graceful-shutdown/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Une mise à jour ou éviction SIGTERM peut interrompre une requête critique ou perdre une unité de travail.

#### 2. Pattern et fonctionnement

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

#### 3. Séquence opérationnelle illustrée

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

#### 4. Exemple YAML

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

#### 5. Choix et contraintes d'architecture

- Mesurer durée d'un in-flight et délai de propagation réseau.
- preStop peut aider au drain mais consomme grace period.
- SIGKILL possible : l'idempotence/recovery reste obligatoire.

**Principale garantie :** L'application doit arrêter d'accepter de nouveaux travaux, drainer les requêtes en cours, préserver/réconcilier les opérations durables et quitter avant terminationGracePeriodSeconds.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Requête encore en vol | Conserver intention durable/reconcilier |
| Grace period expirée | SIGKILL : replay idempotent |
| MQ ACK fait trop tôt | ACK seulement après transaction métier cohérente |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « Graceful Shutdown / Drain » ?** L'application doit arrêter d'accepter de nouveaux travaux, drainer les requêtes en cours, préserver/réconcilier les opérations durables et quitter avant terminationGracePeriodSeconds. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
