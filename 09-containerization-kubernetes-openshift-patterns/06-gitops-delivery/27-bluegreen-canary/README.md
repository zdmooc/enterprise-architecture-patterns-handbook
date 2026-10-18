# 27 — Blue/Green / Canary / Progressive Delivery

> **Famille : Déploiement** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Une nouvelle version doit être testée sous trafic réel sans exposer immédiatement 100 % des clients.

## 2. Solution et illustration

Blue/Green bascule explicitement la sélection de trafic entre deux versions; Canary expose une fraction mesurée du trafic et augmente seulement après vérification des SLO. Le mécanisme exact dépend du routeur/mesh/Gateway.

~~~mermaid
flowchart LR
  A0["Trafic"]
  A1["Routeur"]
  A2["Stable v1 + Canary v2"]
  A3["métriques"]
  A4["promotion ou rollback"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
  A3 --> A4
~~~

**Exemple de bout en bout :** L'API Java v2 reçoit une petite part du trafic en lecture seulement; les commandes financières doivent préserver les mêmes clés et schémas.

## 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Déployer stable et candidate séparément
  C->>W: Définir politique de trafic mesurable
  W-->>C: Comparer latence p99, erreurs, invariants métier
  C-->>Ar: Promouvoir ou rebasculer sans réémettre commandes
~~~

## 4. Exemple technique (YAML partiel)

~~~yaml
apiVersion: v1
kind: Service
metadata: {name: java-api-stable}
spec:
  selector: {app: java-api, track: stable}
  ports: [{port: 8080, targetPort: 8080}]
---
apiVersion: v1
kind: Service
metadata: {name: java-api-canary}
spec:
  selector: {app: java-api, track: canary}
  ports: [{port: 8080, targetPort: 8080}]
# La répartition entre Services exige un routeur/contrôleur distinct.
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

## 5. Arbitrages et responsabilités

- Service selector partagé ne fournit pas de pondération exacte.
- HTTPRoute/ingress/controller spécialisé pour poids précis si supporté.
- S'assurer compatibilité schémas DB et opérations en vol.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Trafic canary trop fort | Contrôleur de poids/taux |
| Erreur métier sur une commande en vol | Référence idempotente commune |
| Rollback code ≠ rollback données | Plan de compatibilité évolutive |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « Blue/Green / Canary / Progressive Delivery » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
