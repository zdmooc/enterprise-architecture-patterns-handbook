# 21 — Service Discovery / Stable Service

> **Famille : Réseau** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Un Pod change d'adresse lors du redémarrage : un consommateur Java ne doit pas contenir des IP de Pods en dur.

## 2. Solution et illustration

Un Kubernetes Service avec label selector et DNS stable expose les Pods qui passent readiness ; EndpointSlices matérialisent les destinations.

~~~mermaid
flowchart LR
  A0["Client interne"]
  A1["DNS du Service"]
  A2["Service/EndpointSlices"]
  A3["Pod Ready"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
~~~

**Exemple de bout en bout :** Un service `payments-api` appelle `account-adapter` via `http://account-adapter:8080` dans son namespace ; la protection réseau reste nécessaire.

## 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Résoudre account-adapter.default.svc.cluster.local
  C->>W: Service oriente vers endpoints ready
  W-->>C: Un Pod redémarre sous nouvelle IP
  C-->>Ar: EndpointSlices mettent à jour le routage
~~~

## 4. Exemple technique (YAML partiel)

~~~yaml
apiVersion: v1
kind: Service
metadata: {name: account-adapter}
spec:
  type: ClusterIP
  selector: {app: account-adapter}
  ports:
    - name: http
      port: 8080
      targetPort: http
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

## 5. Arbitrages et responsabilités

- DNS namespace et FQDN selon besoins.
- ClusterIP n'est pas une Gateway/API Management.
- Réseau autorisé par NetworkPolicy et authentification applicative.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Service sans endpoints | Readiness/labels à examiner |
| Pod en cours d'arrêt | Drain/termination à tester |
| DNS éphémère en panne | Budget timeout et alertes DNS |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « Service Discovery / Stable Service » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
