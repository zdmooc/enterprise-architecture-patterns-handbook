# Cours 161 — Service Discovery · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
Le service Payment API doit joindre le connecteur MQ par un nom stable même si ses pods sont remplacés.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Service et DNS interne"] --> B["Endpoints des pods"]
    B --> C["Application appelante"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** Le nom Service reste stable malgré rotation des pods, mais les clients gèrent la coupure de connexion.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** Le DNS et le Service ne remplacent pas l'identité mTLS ou les contrats de disponibilité.

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
2. **Test spécifique :** Supprimer un pod du connecteur et vérifier la redécouverte ainsi que les délais de reconnexion.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour Service Discovery ?**
- **A.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **B.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.
- **C.** Mettre en œuvre Service Discovery en démontrant l'invariant par un test contrôlé.

**Bonne réponse théorique : C.** Le nom Service reste stable malgré rotation des pods, mais les clients gèrent la coupure de connexion.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/05-network-security/21-service-discovery/README.md)

> **Famille : Réseau** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Un Pod change d'adresse lors du redémarrage : un consommateur Java ne doit pas contenir des IP de Pods en dur.

#### 2. Solution et illustration

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

#### 3. Séquence d'exploitation

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

#### 4. Exemple technique (YAML partiel)

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

#### 5. Arbitrages et responsabilités

- DNS namespace et FQDN selon besoins.
- ClusterIP n'est pas une Gateway/API Management.
- Réseau autorisé par NetworkPolicy et authentification applicative.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Service sans endpoints | Readiness/labels à examiner |
| Pod en cours d'arrêt | Drain/termination à tester |
| DNS éphémère en panne | Budget timeout et alertes DNS |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « Service Discovery / Stable Service » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
