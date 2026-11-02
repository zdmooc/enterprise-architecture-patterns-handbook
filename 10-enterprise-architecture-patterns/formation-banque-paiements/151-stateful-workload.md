# Cours 151 — StatefulSet · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
Des brokers ou services conservant une identité stable nécessitent réseau et stockage persistants, avec ordre de déploiement maîtrisé.

**Invariant à préserver :** Un StatefulSet fournit identité/volume, pas le consensus ni la HA d'une base.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["StatefulSet / identité stable"] --> B["PVC / stockage persistent"]
    B --> C["Workload stateful"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : Ne pas déployer une base bancaire critique en StatefulSet en concluant qu'elle est automatiquement résiliente.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern StatefulSet
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Supprimer le Pod et vérifier retour sur son PVC, cohérence des données et règles de quorum.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à StatefulSet ?**
- **A.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **B.** Définir StatefulSet, ses limites et ses tests de reprise sur OpenShift.
- **C.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.

**Bonne réponse théorique : B.** Un StatefulSet fournit identité/volume, pas le consensus ni la HA d'une base.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/03-workload-design/11-stateful-workload/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Une base ou un broker exige identité DNS et volumes persistants propres à chaque réplica.

#### 2. Pattern et fonctionnement

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

#### 3. Séquence opérationnelle illustrée

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

#### 4. Exemple YAML

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

#### 5. Choix et contraintes d'architecture

- Stable identity et PVC sont réellement nécessaires ; sinon Deployment.
- StorageClass/RWX/RWO, snapshots et expansion selon CSI.
- Politique de réplication applicative et sauvegarde indépendantes du StatefulSet.

**Principale garantie :** StatefulSet attribue une identité ordinale stable et des PVC distincts ; **il ne fournit pas à lui seul réplication, quorum, sauvegarde ou tolérance de panne**.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| PVC indisponible | Restaurer ou réparer storage, sans forcer double attachement |
| Site perdu | DR validé par applicatif, pas par StatefulSet seul |
| Rolling update bloque | Canary ordinal/partition, plan de reprise |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « StatefulSet / Stable Identity » ?** StatefulSet attribue une identité ordinale stable et des PVC distincts ; **il ne fournit pas à lui seul réplication, quorum, sauvegarde ou tolérance de panne**. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
