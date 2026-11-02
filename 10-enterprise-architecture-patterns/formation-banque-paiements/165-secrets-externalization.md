# Cours 165 — Secrets Externalization · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
Le mot de passe MQ, l'identité base et les certificats changent sans rebuild ni commit contenant leur valeur.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Vault / secret manager"] --> B["External Secrets / CSI selon choix"]
    B --> C["Pod / client rotatable"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** Aucun secret de production n'est stocké dans Git, l'image ou les logs.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** Le renouvellement Kubernetes Secret ne signifie pas que l'application a rechargé le secret.

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
2. **Test spécifique :** Révoquer puis renouveler un secret utilisé par le connecteur sans accès à l'ancien certificat.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour Secrets Externalization ?**
- **A.** Mettre en œuvre Secrets Externalization en démontrant l'invariant par un test contrôlé.
- **B.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **C.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.

**Bonne réponse théorique : A.** Aucun secret de production n'est stocké dans Git, l'image ou les logs.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/05-network-security/25-secrets-externalization/README.md)

> **Famille : Sécurité des secrets** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Les mots de passe et clés ne doivent pas être embarqués dans images Docker, code Java ni YAML publics.

#### 2. Solution et illustration

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

#### 3. Séquence d'exploitation

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

#### 4. Exemple technique (YAML partiel)

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

#### 5. Arbitrages et responsabilités

- Le Secret Kubernetes n'est pas une encryption de bout en bout par défaut ; chiffrer etcd et contrôler RBAC.
- Éviter injection de secrets dans image/ConfigMap et logs.
- Mettre en place tests d'expiration et retrait de clé.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Secret expiré | Alerter avant expiry et rotation |
| Coffre indisponible | Politique de cache borné validée |
| Secret exposé en logs | Masquage et restriction audit |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « Secrets Externalization / Rotation » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
