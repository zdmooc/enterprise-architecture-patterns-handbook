# Cours 163 — NetworkPolicy Default Deny · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
Un pod Reporting ne doit pas accéder à la base ou aux services internes du domaine Paiements.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Namespace / Pod"] --> B["Default deny ingress et egress"]
    B --> C["Flux explicitement autorisés"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** Un workload non autorisé ne peut atteindre les ports sensibles, y compris depuis le cluster.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** Une NetworkPolicy ne valide ni token OIDC ni droit d'accès à un ordre spécifique.

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
2. **Test spécifique :** Tester un pod intrus vers PostgreSQL et vérifier que le seul flux métier approuvé fonctionne.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour NetworkPolicy Default Deny ?**
- **A.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **B.** Mettre en œuvre NetworkPolicy Default Deny en démontrant l'invariant par un test contrôlé.
- **C.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.

**Bonne réponse théorique : B.** Un workload non autorisé ne peut atteindre les ports sensibles, y compris depuis le cluster.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/05-network-security/23-default-deny-network/README.md)

> **Famille : Sécurité réseau** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Par défaut, de nombreuses configurations autorisent trop de communications est-ouest entre Pods.

#### 2. Solution et illustration

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

#### 3. Séquence d'exploitation

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

#### 4. Exemple technique (YAML partiel)

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

#### 5. Arbitrages et responsabilités

- Les NetworkPolicies sont appliquées si le CNI cible les supporte.
- Une politique ingress seule n'assure pas l'egress.
- Tester résolution DNS, télémétrie, probes et opérateurs.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| DNS bloqué | Autoriser egress DNS vers resolver approuvé |
| Health checks bloqués | Adapter politiques au plan de sondes |
| Port ouvert à tous | Réduire podSelector et namespaceSelector |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « NetworkPolicy Default Deny / Zero Trust Segmentation » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
