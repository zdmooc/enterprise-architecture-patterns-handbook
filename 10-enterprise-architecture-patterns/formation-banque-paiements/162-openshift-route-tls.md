# Cours 162 — OpenShift Route / TLS · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
Un portail expose uniquement l'API bancaire prévue via une Route OpenShift avec un certificat serveur correctement géré.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Client HTTPS"] --> B["OpenShift Route / IngressController"]
    B --> C["Payment API Service"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** Le flux HTTPS est protégé selon la stratégie TLS et seule la surface prévue est exposée.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** La terminaison TLS à l'entrée ne garantit pas le chiffrement du tronçon interne.

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
2. **Test spécifique :** Tester certificat expiré, host non autorisé, chemins non exposés et validation TLS bout en bout.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour OpenShift Route / TLS ?**
- **A.** Mettre en œuvre OpenShift Route / TLS en démontrant l'invariant par un test contrôlé.
- **B.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **C.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.

**Bonne réponse théorique : A.** Le flux HTTPS est protégé selon la stratégie TLS et seule la surface prévue est exposée.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/05-network-security/22-openshift-route-tls/README.md)

> **Famille : Réseau OpenShift** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Les clients externes doivent atteindre l'API du cluster avec un nom DNS et un niveau TLS défini.

#### 2. Solution et illustration

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

#### 3. Séquence d'exploitation

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

#### 4. Exemple technique (YAML partiel)

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

#### 5. Arbitrages et responsabilités

- Reencrypt exige un backend TLS configuré ; ne pas recopier une route TLS sur backend HTTP.
- Les certificats et CA doivent être gérés et renouvelés.
- L'API Gateway / WAF reste un composant séparé si nécessaire.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Certificat expiré | Rotation automatisée et alertes |
| Mauvais targetPort | Refus readiness/routage, test end-to-end |
| TLS backend mal validé | CA/certificat de destination à configurer |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « OpenShift Route / TLS Termination » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
