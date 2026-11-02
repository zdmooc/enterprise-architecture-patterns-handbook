# Cours 157 — Horizontal Pod Autoscaler · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
La charge HTTP augmente ; la Payment API doit adapter son nombre de replicas à des métriques pertinentes.

**Invariant à préserver :** La montée en replicas ne dépasse pas la capacité du broker ou core bancaire en aval.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["Métrique HPA qualifiée"] --> B["Controller HPA"]
    B --> C["Replicas Deployment"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : Réglages requests CPU, stabilisation, limites max et temps de démarrage déterminent l'effet réel.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern Horizontal Pod Autoscaler
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Saturer la dépendance centrale : constater que HPA n'élimine pas le bottleneck aval.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à Horizontal Pod Autoscaler ?**
- **A.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **B.** Définir Horizontal Pod Autoscaler, ses limites et ses tests de reprise sur OpenShift.
- **C.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.

**Bonne réponse théorique : B.** La montée en replicas ne dépasse pas la capacité du broker ou core bancaire en aval.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/04-resilience-scaling/17-horizontal-scaling/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Une montée de trafic met en saturation les replicas applicatifs.

#### 2. Pattern et fonctionnement

HPA ajuste le nombre de replicas selon métriques CPU, mémoire ou métriques custom/external ; ne dépasse pas les capacités réelles des dépendances.

~~~mermaid
flowchart LR
    S0["Metrics Server"]
    S1["HPA controller"]
    S2["Deployment replicas"]
    S3["Pods"]
    S4["Service"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
~~~

**Exemple concret :** L'API Java passe de 2 à 5 replicas selon CPU sous réserve de la capacité DB/Core ; le seuil est calibré après campagne de charge.

#### 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Mesurer charge et requests CPU
  K->>W: Configurer min/max replicas et cible
  O->>K: Observer HPA sous charge
  K->>W: Vérifier DB/pools et délai scale-out
  W-->>O: Etat observé, décision de validation
~~~

#### 4. Exemple YAML

~~~yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: java-api-hpa}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: java-api
  minReplicas: 2
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: {type: Utilization, averageUtilization: 65}
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

#### 5. Choix et contraintes d'architecture

- CPU utilization suppose requests définis.
- Autoscaling change le nombre de Pods, pas le débit core externe.
- Stabilization windows évitent oscillations.

**Principale garantie :** HPA ajuste le nombre de replicas selon métriques CPU, mémoire ou métriques custom/external ; ne dépasse pas les capacités réelles des dépendances.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| DB saturée | Limiter maxReplicas et pool |
| Métriques manquantes | HPA incapable de scaler correctement |
| Cold start Java | Prévoir buffer et replicas minimum |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « HPA / Horizontal Pod Autoscaling » ?** HPA ajuste le nombre de replicas selon métriques CPU, mémoire ou métriques custom/external ; ne dépasse pas les capacités réelles des dépendances. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
