# 29 — Strangler Fig / Side-by-Side Java/JEE Migration

> **Famille : Modernisation** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Une application EAR/WAR et ses interfaces SOAP, base partagée, sessions et MQ ne peuvent pas être réécrites sans risque majeur.

## 2. Solution et illustration

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

## 3. Séquence d'exploitation

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

## 4. Exemple technique (plan illustratif)

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

## 5. Arbitrages et responsabilités

- Vérifier compatibilité licence/support du serveur/applications dans conteneurs.
- Analyser état local, session, transactions JTA/JMS, ressources JNDI, logs et dépendances natives.
- Ne pas déplacer le système de référence financier sans modèle transactionnel validé.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| WAR dépend à un filesystem mutable | Externaliser state/volumes requis |
| Session en mémoire | Externaliser et rendre réplique-safe |
| Deux routes émettent même ordre | Single writer/routage et idempotence |
| Mauvais SDK/JDK | Tests de classloading, APIs et versions |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « Strangler Fig / Side-by-Side Java/JEE Migration » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
