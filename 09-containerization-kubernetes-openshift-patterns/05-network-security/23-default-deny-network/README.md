# 23 — NetworkPolicy Default Deny / Zero Trust Segmentation

> **Famille : Sécurité réseau** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Par défaut, de nombreuses configurations autorisent trop de communications est-ouest entre Pods.

## 2. Solution et illustration

Bloquer ingress/egress puis autoriser explicitement les flux justifiés ; les contrôles d'identité, d'API et la segmentation réseau sont complémentaires.

~~~mermaid
flowchart LR
  A0["Pod appelant"]
  A1["Policy ingress/egress"]
  A2["Service"]
  A3["Pod cible"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
~~~

**Exemple de bout en bout :** Seuls des Pods `role: api-client` peuvent joindre `java-api` en 8080; toute sortie DB/MQ est autorisée par politique explicite.

## 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Appliquer default-deny dans namespace
  C->>W: Ajouter allow DNS nécessaire
  W-->>C: Ajouter allow ingress applicative précise
  C-->>Ar: Tester flux autorisés et refusés
~~~

## 4. Exemple technique (YAML partiel)

~~~yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny}
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-api-ingress}
spec:
  podSelector: {matchLabels: {app: java-api}}
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector: {matchLabels: {role: api-client}}
      ports: [{protocol: TCP, port: 8080}]
# Les policies egress nécessaires sont à définir séparément.
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

## 5. Arbitrages et responsabilités

- Les NetworkPolicies sont appliquées si le CNI cible les supporte.
- Une politique ingress seule n'assure pas l'egress.
- Tester résolution DNS, télémétrie, probes et opérateurs.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| DNS bloqué | Autoriser egress DNS vers resolver approuvé |
| Health checks bloqués | Adapter politiques au plan de sondes |
| Port ouvert à tous | Réduire podSelector et namespaceSelector |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « NetworkPolicy Default Deny / Zero Trust Segmentation » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
