# 13 — Operator / Reconciliation Controller

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Les bases, brokers et composants complexes nécessitent des opérations répétitives de cycle de vie impossibles à coder comme simple démarrage de Pod.

## 2. Pattern et fonctionnement

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

## 3. Séquence opérationnelle illustrée

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

## 4. Exemple YAML

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

## 5. Choix et contraintes d'architecture

- Controller leader election et RBAC minimal.
- Idempotence, requeue/backoff, conflits server-side apply.
- Finalizer : protéger ressources et ne pas bloquer suppression indéfiniment.

**Principale garantie :** Une CRD exprime l'état désiré et un controller converge vers cet état de façon idempotente, avec Conditions, Events et finalizers maîtrisés.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Deux replicas controllers | Leader election/lease ou réconciliation sûre |
| API temporairement KO | Retry borné et conditions Degraded |
| CRD change | Conversion/migration testées |
| Finalizer bloqué | Runbook de recovery |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « Operator / Reconciliation Controller » ?** Une CRD exprime l'état désiré et un controller converge vers cet état de façon idempotente, avec Conditions, Events et finalizers maîtrisés. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
