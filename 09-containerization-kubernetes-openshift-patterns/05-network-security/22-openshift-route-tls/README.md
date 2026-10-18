# 22 — OpenShift Route / TLS Termination

> **Famille : Réseau OpenShift** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Les clients externes doivent atteindre l'API du cluster avec un nom DNS et un niveau TLS défini.

## 2. Solution et illustration

Une Route OpenShift expose un Service ; mode edge, reencrypt ou passthrough selon frontière de confiance. Elle n'offre pas à elle seule la gouvernance d'une Gateway API.

~~~mermaid
flowchart LR
  A0["Client HTTPS"]
  A1["Route OpenShift"]
  A2["TLS backend"]
  A3["Service"]
  A4["Pod Java"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
  A3 --> A4
~~~

**Exemple de bout en bout :** Une API Java est exposée via TLS en mode reencrypt vers le Service, avec hostname public fictif, certificat et politique réseau.

## 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Contrôler DNS et terminaison TLS
  C->>W: Créer Route vers Service nommé
  W-->>C: Vérifier certificat chaîne externe et backend
  C-->>Ar: Tester connexion et expiration des certificats
~~~

## 4. Exemple technique (YAML partiel)

~~~yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata: {name: java-api}
spec:
  host: api.example.invalid
  to: {kind: Service, name: java-api}
  port: {targetPort: https}
  tls:
    termination: reencrypt
    insecureEdgeTerminationPolicy: Redirect
# Nécessite un Service avec un vrai endpoint TLS nommé https.
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

## 5. Arbitrages et responsabilités

- Reencrypt exige un backend TLS configuré ; ne pas recopier une route TLS sur backend HTTP.
- Les certificats et CA doivent être gérés et renouvelés.
- L'API Gateway / WAF reste un composant séparé si nécessaire.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Certificat expiré | Rotation automatisée et alertes |
| Mauvais targetPort | Refus readiness/routage, test end-to-end |
| TLS backend mal validé | CA/certificat de destination à configurer |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « OpenShift Route / TLS Termination » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
