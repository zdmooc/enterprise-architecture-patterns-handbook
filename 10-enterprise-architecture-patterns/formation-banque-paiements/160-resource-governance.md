# Cours 160 — Resource Governance · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
La JVM du service doit disposer de ressources prévisibles sans affamer les autres applications d'une plateforme mutualisée.

**Invariant à préserver :** CPU/mémoire déclarés sont cohérents avec heap Java, caches et overhead sous charge.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["Requests/limits"] --> B["Quota et LimitRange"]
    B --> C["Scheduling / QoS"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : Une limite mémoire inférieure à la consommation native + heap rend le service instable.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern Resource Governance
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Baisser la limite mémoire et vérifier OOMKill, métriques, reprise et absence de double traitement.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à Resource Governance ?**
- **A.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **B.** Définir Resource Governance, ses limites et ses tests de reprise sur OpenShift.
- **C.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.

**Bonne réponse théorique : B.** CPU/mémoire déclarés sont cohérents avec heap Java, caches et overhead sous charge.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/04-resilience-scaling/20-resource-governance/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Sans réservation, limitations et quotas, un tenant peut évincer les autres ou surconsommer CPU/mémoire.

#### 2. Pattern et fonctionnement

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

#### 3. Séquence opérationnelle illustrée

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

#### 4. Exemple YAML

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

#### 5. Choix et contraintes d'architecture

- Dimensionner JVM heap + metaspace + direct buffers à l'intérieur de la limite.
- CPU limits peuvent provoquer throttling néfaste pour faible latence.
- ResourceQuota et LimitRange doivent correspondre aux besoins du projet.

**Principale garantie :** Requests guident scheduler et QoS ; limits bornent consommation (CPU throttling, mémoire OOMKill) ; quotas gouvernent le namespace.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| OOMKill JVM | Augmenter budget ou réduire heap, diagnostiquer native |
| CPU throttling | Mesurer p99 et limites |
| Quota namespace saturé | Budget/alertes/housekeeping |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « Requests / Limits / LimitRange / ResourceQuota » ?** Requests guident scheduler et QoS ; limits bornent consommation (CPU throttling, mémoire OOMKill) ; quotas gouvernent le namespace. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
