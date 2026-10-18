# 25 — Secrets Externalization / Rotation

> **Famille : Sécurité des secrets** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Les mots de passe et clés ne doivent pas être embarqués dans images Docker, code Java ni YAML publics.

## 2. Solution et illustration

Intégrer le secret à partir d'un système de gestion approuvé via un mécanisme contrôlé (Secret Kubernetes, CSI secret provider, opérateur externe si installé), gérer rotation et révocation.

~~~mermaid
flowchart LR
  A0["Coffre approuvé"]
  A1["mécanisme de synchronisation"]
  A2["Secret/Volume"]
  A3["Service Java"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
~~~

**Exemple de bout en bout :** L'application récupère son mot de passe DB dans un volume monté; sa rotation entraîne un reload ou redémarrage contrôlé.

## 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Définir owner et politique de rotation
  C->>W: Donner accès seulement au ServiceAccount
  W-->>C: Monter secret et démarrer app
  C-->>Ar: Révoquer/renouveler et tester reprise
~~~

## 4. Exemple technique (YAML partiel)

~~~yaml
volumeMounts:
  - name: db-credentials
    mountPath: /var/run/secrets/app-db
    readOnly: true
volumes:
  - name: db-credentials
    secret:
      secretName: app-db-credentials
      defaultMode: 0400
# Secret créé par processus externe approuvé, non ajouté en clair dans Git.
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

## 5. Arbitrages et responsabilités

- Le Secret Kubernetes n'est pas une encryption de bout en bout par défaut ; chiffrer etcd et contrôler RBAC.
- Éviter injection de secrets dans image/ConfigMap et logs.
- Mettre en place tests d'expiration et retrait de clé.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Secret expiré | Alerter avant expiry et rotation |
| Coffre indisponible | Politique de cache borné validée |
| Secret exposé en logs | Masquage et restriction audit |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « Secrets Externalization / Rotation » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
