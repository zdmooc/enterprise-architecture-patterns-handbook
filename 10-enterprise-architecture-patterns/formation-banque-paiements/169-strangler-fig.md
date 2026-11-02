# Cours 169 — Strangler Fig / Migration Java/JEE · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
Un module J2EE WebSphere historique expose des paiements ; on modernise progressivement certaines fonctions sur Liberty ou Spring/OpenShift.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Canal/API de façade"] --> B["Routage legacy ou cible"]
    B --> C["Ancien et nouveau modules coexistants"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** Pour chaque commande, un seul moteur autoritatif doit exécuter l'effet financier.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** Strangler nécessite inventaire EJB, transactions JMS/JTA et compatibilité des sessions avant migration.

## 4. Séquence de fonctionnement et reprise
~~~mermaid
sequenceDiagram
    participant O as Exploitant / GitOps
    participant K as Kubernetes / OpenShift
    participant A as Payment API
    participant C as Core autoritatif
    O->>K: demander état désiré ou bascule
    K->>A: exposer / configurer / remplacer workload
    A->>C: soumettre ou consulter via référence stable
    C--xA: réponse perdue possible
    A->>C: retrouver l'état du paiement
    C-->>A: résultat attesté ou UNKNOWN
    K-->>O: conditions, alertes et métriques
~~~

## 5. Tests à présenter en Design Authority
1. Démonstration nominale des objets Kubernetes, politiques et versions.
2. **Test spécifique :** Comparer shadow read-only et production, basculer route sans double traitement ; vérifier retour arrière.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour Strangler Fig / Migration Java/JEE ?**
- **A.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **B.** Mettre en œuvre Strangler Fig / Migration Java/JEE en démontrant l'invariant par un test contrôlé.
- **C.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.

**Bonne réponse théorique : B.** Pour chaque commande, un seul moteur autoritatif doit exécuter l'effet financier.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/07-legacy-modernization/29-strangler-fig/README.md)

> **Famille : Modernisation** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Une application EAR/WAR et ses interfaces SOAP, base partagée, sessions et MQ ne peuvent pas être réécrites sans risque majeur.

#### 2. Solution et illustration

Inventorier l'existant, placer une façade/ACL contrôlée, migrer par capacité, comparer les résultats hors effets financiers, puis basculer de façon progressive et réversible.

~~~mermaid
flowchart LR
  A0["Canaux"]
  A1["Façade / ACL"]
  A2["service historique + capacité Java modernisée"]
  A0 --> A1
  A1 --> A2
~~~

**Exemple de bout en bout :** Un ancien module d'accès au statut est remplacé par Java sur OpenShift; la tenue de compte et l'exécution restent dans le moteur existant.

#### 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Découvrir EAR/WAR, JNDI, threads, filesystem, sessions et licences
  C->>W: Construire image compatible et tests contrats
  W-->>C: Shadow read-only comparé à l'existant
  C-->>Ar: Basculer une capacité et conserver rollback encadré
~~~

#### 4. Exemple technique (plan illustratif)

~~~yaml
# Plan de migration illustratif (pas une API Kubernetes)
phases:
  - inventory: [war-ear, dependencies, jndi, jms, jdbc, native-libs]
  - containerize: [runtime-supported, uid-arbitrary, external-config]
  - test: [contracts, load, security, failure-injection]
  - shadow: [read-only, no-double-side-effects]
  - cutover: [route-one-capability, idempotent, rollback-plan]
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

#### 5. Arbitrages et responsabilités

- Vérifier compatibilité licence/support du serveur/applications dans conteneurs.
- Analyser état local, session, transactions JTA/JMS, ressources JNDI, logs et dépendances natives.
- Ne pas déplacer le système de référence financier sans modèle transactionnel validé.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| WAR dépend à un filesystem mutable | Externaliser state/volumes requis |
| Session en mémoire | Externaliser et rendre réplique-safe |
| Deux routes émettent même ordre | Single writer/routage et idempotence |
| Mauvais SDK/JDK | Tests de classloading, APIs et versions |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « Strangler Fig / Side-by-Side Java/JEE Migration » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
