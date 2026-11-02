# Cours 167 — Blue/Green / Canary · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
Une nouvelle version du service de consultation est testée avec une fraction du trafic avant promotion complète.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Blue et Green / version stable"] --> B["Contrôle de trafic canary"]
    B --> C["Mesures et décision de promotion"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** La fraction canary est contrôlable et les contrats partagés restent compatibles.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** Canary de commande financière nécessite politique explicite de routage stable et d'idempotence.

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
2. **Test spécifique :** Introduire erreur HTTP dans la nouvelle version et restaurer le trafic sans réexécuter les paiements.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour Blue/Green / Canary ?**
- **A.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **B.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.
- **C.** Mettre en œuvre Blue/Green / Canary en démontrant l'invariant par un test contrôlé.

**Bonne réponse théorique : C.** La fraction canary est contrôlable et les contrats partagés restent compatibles.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/06-gitops-delivery/27-bluegreen-canary/README.md)

> **Famille : Déploiement** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Une nouvelle version doit être testée sous trafic réel sans exposer immédiatement 100 % des clients.

#### 2. Solution et illustration

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

#### 3. Séquence d'exploitation

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

#### 4. Exemple technique (YAML partiel)

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

#### 5. Arbitrages et responsabilités

- Service selector partagé ne fournit pas de pondération exacte.
- HTTPRoute/ingress/controller spécialisé pour poids précis si supporté.
- S'assurer compatibilité schémas DB et opérations en vol.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Trafic canary trop fort | Contrôleur de poids/taux |
| Erreur métier sur une commande en vol | Référence idempotente commune |
| Rollback code ≠ rollback données | Plan de compatibilité évolutive |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « Blue/Green / Canary / Progressive Delivery » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
