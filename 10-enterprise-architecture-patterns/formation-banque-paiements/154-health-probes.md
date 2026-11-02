# Cours 154 — Health Probes · Kubernetes / OpenShift

> Banque fictive : virement SEPA 500 EUR, Java/Spring + IBM MQ + OpenShift. **Cours et corrigé théoriques publiés ; validation individuelle en attente.**

## 1. Situation de départ
Un service Java est démarré mais n'est pas encore apte à recevoir du trafic bancaire ; sa JVM peut aussi être vivante tandis que l'aval est en panne.

**Invariant à préserver :** Readiness retire le Pod du trafic sans prétendre que tous les services bancaires externes sont sains.

## 2. Architecture et frontières
~~~mermaid
flowchart LR
    A["Startup / liveness"] --> B["Readiness sur capacité locale"]
    B --> C["Service routing"]
    B -. "Incident" .-> D["Diagnostic / reprise"]
    D --> E["État métier vérifié avant nouvel effet"]
~~~

Le contrôleur Kubernetes rapproche un état désiré avec des ressources observées. Il ne se substitue pas aux processus de traitement et de règlement de la banque.

## 3. Contrats d'exploitation
1. Identifier les sources de vérité pour la configuration Kubernetes, les versions de manifestes et les statuts métier.
2. Définir la cible de disponibilité, SLO, RTO/RPO lorsqu'ils s'appliquent et la capacité CPU/mémoire.
3. Fixer ServiceAccount, RBAC/SCC, NetworkPolicy, secrets, conditions et alertes du workload.
4. Définir les limites du pattern : Liveness mal conçue amplifie les incidents externes au lieu de les résoudre.
5. Documenter dépendances MQ, base de données, persistance, ordonnancement et deadline métier.

## 4. Séquence nominale et scénario de panne
~~~mermaid
sequenceDiagram
    participant P as Plateforme / contrôleur
    participant K as Kubernetes API
    participant A as Application Java
    participant D as Source autoritative
    P->>K: déclarer le pattern Health Probes
    K->>A: créer / mettre à jour workload
    A-->>K: état Ready, Running ou Degraded
    Note over A,D: panne ou perte de réponse
    A->>D: demander preuve d'exécution par référence
    D-->>A: statut exact ou UNKNOWN
    K-->>P: état observé et conditions
~~~

## 5. Plan de qualification
- **Test nominal :** état désiré, nombre de ressources et conditions cohérents.
- **Test spécifique :** Bloquer une dépendance optionnelle : ne pas provoquer de redémarrages de liveness en boucle.
- **Test de concurrence :** deux pods/consumers ne créent pas deux ordres sur la même référence.
- **Test de panne :** disparition d'un pod, d'un nœud ou d'un aval ; aucune conclusion financière sur un simple timeout.
- **Test de sécurité :** image non-root, SCC, réseau, secrets, RBAC et certificats appropriés.
- **Test de capacité :** p95/p99, mémoire JVM, CPU, saturation, latence MQ et temps de convergence.

## 6. QCM de révision corrigé
**Quel arbitrage convient à Health Probes ?**
- **A.** Considérer que les Pods Ready prouvent qu'un paiement est réglé.
- **B.** Définir Health Probes, ses limites et ses tests de reprise sur OpenShift.
- **C.** Donner cluster-admin au processus et rejouer aveuglément les ordres après timeout.

**Bonne réponse théorique : B.** Readiness retire le Pod du trafic sans prétendre que tous les services bancaires externes sont sains.

Le corrigé accompagne la lecture et ne constitue pas un résultat individuel obtenu en session.

## 7. Fiche détaillée déjà présente dans le catalogue
Les YAML, graphes, contraintes d'admission et tests propres à ce pattern sont conservés ci-dessous.

[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/04-resilience-scaling/14-health-probes/README.md)

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

#### 1. Problème

Confondre délai de démarrage Java, panne interne et dépendance externe peut provoquer un redémarrage en boucle.

#### 2. Pattern et fonctionnement

Startup limite les redémarrages précoces, readiness retire du trafic, liveness détecte un processus bloqué ; ne pas attacher liveness à la disponibilité du core.

~~~mermaid
flowchart LR
    S0["Démarrage"]
    S1["startup OK"]
    S2["readiness OK"]
    S3["Service endpoints"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
~~~

**Exemple concret :** Une application Java met 45 secondes à charger ses classes : startup l'attend ; readiness échoue si elle ne peut plus servir ; liveness reste locale.

#### 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Pod démarre, startupProbe échoue transitoirement
  K->>W: Application termine son démarrage
  O->>K: Readiness valide le service
  K->>W: En cas d'indisponibilité, retirer endpoint sans redémarrer arbitrairement
  W-->>O: Etat observé, décision de validation
~~~

#### 4. Exemple YAML

~~~yaml
startupProbe:
  httpGet: {path: /health/startup, port: 8080}
  failureThreshold: 30
  periodSeconds: 2
readinessProbe:
  httpGet: {path: /health/ready, port: 8080}
  periodSeconds: 5
livenessProbe:
  httpGet: {path: /health/live, port: 8080}
  periodSeconds: 10
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

#### 5. Choix et contraintes d'architecture

- Seuils et periodSeconds mesurés en charge réelle.
- Readiness adaptée aux capacités réellement nécessaires.
- Liveness ne doit pas redémarrer sur panne partagée d'une dépendance externe.

**Principale garantie :** Startup limite les redémarrages précoces, readiness retire du trafic, liveness détecte un processus bloqué ; ne pas attacher liveness à la disponibilité du core.

#### 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Probe trop agressive | CrashLoopBackOff : relever thresholds après mesure |
| Dépendance DB HS | Readiness ou dégradation métier, pas cascade liveness |
| Port probe non exposé | Tests de contrat/URL |

#### 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

#### 8. Question d'entretien d'architecte

**Que garantit réellement « Startup / Readiness / Liveness Probes » ?** Startup limite les redémarrages précoces, readiness retire du trafic, liveness détecte un processus bloqué ; ne pas attacher liveness à la disponibilité du core. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [matrice de décision](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
