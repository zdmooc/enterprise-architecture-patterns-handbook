# Cours 153 — Operator / Reconciliation · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
Une capacité interne gère des ressources interdépendantes et doit converger automatiquement vers l'état demandé par CRD.

**Invariant à préserver :** La réconciliation d'un contrôleur est idempotente et n'applique pas d'effet financier direct.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["Custom Resource"] --> B["Reconciler / conditions"]
    B --> C["Deployment, PVC, Service"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : CRD non installée ou finalizer bloqué : prévoir conversion, reprise et runbook.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern Operator / Reconciliation
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Supprimer un objet enfant : le controller le reconstruit et expose Ready/Degraded.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à Operator / Reconciliation ?**
- **A.** Définir Operator / Reconciliation, ses limites et ses tests de reprise sur OpenShift.
- **B.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **C.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.

**Bonne réponse théorique : A.** La réconciliation d'un contrôleur est idempotente et n'applique pas d'effet financier direct.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/03-workload-design/13-operator-reconciliation/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Les bases, brokers et composants complexes nécessitent des opérations répétitives de cycle de vie impossibles à coder comme simple démarrage de Pod.

#### 2. Pattern et fonctionnement

Une CRD exprime l'état désiré et un controller converge vers cet état de façon idempotente, avec Conditions, Events et finalizers maîtrisés.

~~~mermaid
flowchart LR
    S0["Custom Resource"]
    S1["Reconciler"]
    S2["Stateful/Deploy/Service"]
    S3["Status Conditions"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
~~~

**Exemple concret :** Un Operator interne assure la création de Service/PVC/Deployment pour une capacité fictive, signale Ready/Degraded et répare un objet supprimé.

#### 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Créer/valider CRD versionnée
  K->>W: Reconciler desired vs observed
  O->>K: Appliquer par server-side apply
  K->>W: Mettre à jour Status et Events
  W-->>O: Etat observé, décision de validation
~~~

#### 4. Exemple YAML

~~~yaml
apiVersion: platform.example.invalid/v1alpha1
kind: ManagedCapability
metadata: {name: sample}
spec:
  replicas: 2
  deletionPolicy: Retain
# CRD et Operator custom à développer : ce YAML seul ne fonctionne pas.
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

#### 5. Choix et contraintes d'architecture

- Controller leader election et RBAC minimal.
- Idempotence, requeue/backoff, conflits server-side apply.
- Finalizer : protéger ressources et ne pas bloquer suppression indéfiniment.

**Principale garantie :** Une CRD exprime l'état désiré et un controller converge vers cet état de façon idempotente, avec Conditions, Events et finalizers maîtrisés.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Deux replicas controllers | Leader election/lease ou réconciliation sûre |
| API temporairement KO | Retry borné et conditions Degraded |
| CRD change | Conversion/migration testées |
| Finalizer bloqué | Runbook de recovery |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « Operator / Reconciliation Controller » ?** Une CRD exprime l'état désiré et un controller converge vers cet état de façon idempotente, avec Conditions, Events et finalizers maîtrisés. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
