# Cours 156 — PodDisruptionBudget · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
Une maintenance de nœud ne doit pas évincer simultanément tous les Pods du service de paiement.

**Invariant à préserver :** Le PDB agit sur les évictions volontaires respectant l'API, pas sur crash et disparition du nœud.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["Eviction volontaire"] --> B["PDB minAvailable"]
    B --> C["Disponibilité visée"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : PDB peut empêcher la maintenance si replicas, capacité ou placements sont insuffisants.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern PodDisruptionBudget
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Vider un nœud et confirmer respect PDB ; couper nœud brutalement et mesurer ce qui n'est pas couvert.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à PodDisruptionBudget ?**
- **A.** Définir PodDisruptionBudget, ses limites et ses tests de reprise sur OpenShift.
- **B.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **C.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.

**Bonne réponse théorique : A.** Le PDB agit sur les évictions volontaires respectant l'API, pas sur crash et disparition du nœud.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/04-resilience-scaling/16-pod-disruption-budget/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Une opération de maintenance risque d'évincer trop de Pods d'une capacité répliquée.

#### 2. Pattern et fonctionnement

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

#### 3. Séquence opérationnelle illustrée

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

#### 4. Exemple YAML

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

#### 5. Choix et contraintes d'architecture

- PDB doit être aligné sur replicas et capacité des zones.
- minAvailable 2 sur replicas 2 peut bloquer toutes les évictions.
- HA nécessite topology spread et capacité, pas PDB seulement.

**Principale garantie :** Le PDB limite les évictions **volontaires** prises en compte par l'Eviction API ; ne protège pas des pannes de nœud ou site.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Drain impossible | PDB trop contraignant : fenêtre et capacité supplémentaires |
| Nœud panne brutale | PDB n'aide pas : réplication/zones |
| Aucune readiness | PDB ne remplace pas les sondes correctes |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « PodDisruptionBudget (PDB) » ?** Le PDB limite les évictions **volontaires** prises en compte par l'Eviction API ; ne protège pas des pannes de nœud ou site. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
