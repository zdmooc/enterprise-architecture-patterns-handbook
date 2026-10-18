# 24 — SCC / ServiceAccount / Least Privilege

> **Famille : Sécurité OpenShift** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Un manifeste hérité peut exiger root, hostNetwork, hostPath ou des permissions excessives pour un usage ordinaire.

## 2. Solution et illustration

Mettre en place un ServiceAccount dédié, RBAC minimal, securityContext non privilégié et admission par une SCC restrictive ; une exception nécessite justification et revue.

~~~mermaid
flowchart LR
  A0["ServiceAccount"]
  A1["RBAC & SCC admission"]
  A2["Pod sans privilèges"]
  A3["API limitée"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
~~~

**Exemple de bout en bout :** Une application Java ne demande ni hostPath ni UID fixe; ses ressources sont accessibles sans root grâce à permissions compatibles UID alloué.

## 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Créer compte de service dédié
  C->>W: Déployer sous SCC restrictive
  W-->>C: Contrôler UID réellement attribué
  C-->>Ar: Vérifier RBAC et absence d'accès cluster-admin
~~~

## 4. Exemple technique (YAML partiel)

~~~yaml
spec:
  serviceAccountName: java-api
  automountServiceAccountToken: false
  securityContext:
    seccompProfile: {type: RuntimeDefault}
  containers:
    - name: java-api
      image: registry.example.invalid/team/java-api@sha256:<DIGEST>
      securityContext:
        runAsNonRoot: true
        allowPrivilegeEscalation: false
        capabilities: {drop: ["ALL"]}
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

## 5. Arbitrages et responsabilités

- Ne pas accorder anyuid/privileged par confort de migration.
- En restricted-v2, le UID peut être issu d'une plage namespace.
- Les SecurityContext Pod/Container et SCC doivent être compatibles.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Pod refuse admission | Corriger image/volumes au lieu d'élargir SCC |
| UID fixe interdit | Retirer runAsUser hardcodé |
| Token ServiceAccount exposé | automountServiceAccountToken false si inutile |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « SCC / ServiceAccount / Least Privilege » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
