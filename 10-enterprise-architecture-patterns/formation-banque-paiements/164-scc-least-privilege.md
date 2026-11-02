# Cours 164 — SCC / Least Privilege · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
Une application Java héritée réclame root et hostPath après son packaging en image ; OpenShift doit empêcher une élévation injustifiée.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["ServiceAccount spécifique"] --> B["SCC restrictive et securityContext"]
    B --> C["Pod non privilégié"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** Un Pod sans exception de sécurité injustifiée s'exécute sous UID compatible OpenShift.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** Ne pas ajouter anyuid/privileged simplement pour contourner des permissions d'image incorrectes.

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
2. **Test spécifique :** Essayer un Pod hostPath ou privileged sous le même ServiceAccount : admission refusée.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour SCC / Least Privilege ?**
- **A.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **B.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.
- **C.** Mettre en œuvre SCC / Least Privilege en démontrant l'invariant par un test contrôlé.

**Bonne réponse théorique : C.** Un Pod sans exception de sécurité injustifiée s'exécute sous UID compatible OpenShift.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/05-network-security/24-scc-least-privilege/README.md)

> **Famille : Sécurité OpenShift** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Un manifeste hérité peut exiger root, hostNetwork, hostPath ou des permissions excessives pour un usage ordinaire.

#### 2. Solution et illustration

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

#### 3. Séquence d'exploitation

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

#### 4. Exemple technique (YAML partiel)

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

#### 5. Arbitrages et responsabilités

- Ne pas accorder anyuid/privileged par confort de migration.
- En restricted-v2, le UID peut être issu d'une plage namespace.
- Les SecurityContext Pod/Container et SCC doivent être compatibles.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Pod refuse admission | Corriger image/volumes au lieu d'élargir SCC |
| UID fixe interdit | Retirer runAsUser hardcodé |
| Token ServiceAccount exposé | automountServiceAccountToken false si inutile |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « SCC / ServiceAccount / Least Privilege » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
