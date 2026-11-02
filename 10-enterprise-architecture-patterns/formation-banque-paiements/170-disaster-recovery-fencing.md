# Cours 170 — Backup / DR / Fencing · Kubernetes / OpenShift

> Parcours technique bancaire fictif : ordre SEPA de 500 EUR, Java/JEE, Spring, IBM MQ et OpenShift. Corrigé théorique fourni ; **exercice individuel non validé**.

## 1. Besoin et arbitrage
La plateforme bascule sur un second cluster après incident régional sans autoriser deux writers sur les mêmes ordres.

## 2. Architecture logique
~~~mermaid
flowchart LR
    A["Cluster actif / état durable"] --> B["Bascule et fencing vérifié"]
    B --> C["Cluster de reprise autorisé"]
    B -. "Défaillance / dérive" .-> D["Contrôle / rollback / investigation"]
~~~

**Invariant à protéger :** L'ancien cluster ne peut plus écrire lorsque le nouveau est promu propriétaire.

## 3. Frontières et responsabilités
- La plateforme est autoritative pour l'état déclaré des ressources, mais pas pour le règlement bancaire.
- Les identités et privilèges ServiceAccount/SCC sont réduits, les flux réseau et secrets sont explicitement gouvernés.
- Les manifestes et les images sont versionnés et associés à une politique d'admission et de signature.
- Les scénarios de migration et rollback distinguent retours arrière techniques et corrections financières.
- **Limite :** Des backups et deux clusters ne garantissent ni RPO zéro ni reprise financière cohérente.

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
2. **Test spécifique :** Isoler le cluster primaire et déclencher la bascule ; rejeter ses écritures tardives.
3. Incident : suppression de pod, réponse perdue, dérive GitOps ou panne de l'aval.
4. Non-régression sécurité : identité valide, NetworkPolicy, SCC, secrets et admission.
5. Non-régression métier : aucun double règlement, statut UNKNOWN lorsque le résultat n'est pas prouvé.
6. Indicateurs : readiness, p95/p99, saturation, métriques de restauration, RTO/RPO si pertinents.

## 6. Exercice corrigé
**Quel choix défendrais-tu pour Backup / DR / Fencing ?**
- **A.** Exécuter le paiement une deuxième fois lorsque le pod redémarre.
- **B.** Désactiver RBAC, SCC et contrôles d'admission pour éviter les erreurs.
- **C.** Mettre en œuvre Backup / DR / Fencing en démontrant l'invariant par un test contrôlé.

**Bonne réponse théorique : C.** L'ancien cluster ne peut plus écrire lorsque le nouveau est promu propriétaire.

L'auto-évaluation est à réaliser individuellement ; la publication ne constitue pas une preuve d'exécution sur un cluster réel.

## 7. Fiche du référentiel original
[Ouvrir le pattern et ses exemples YAML](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/08-multicluster-dr/30-disaster-recovery-fencing/README.md)

> **Famille : PRA & multi-cluster** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

#### 1. Problème

Deux clusters OpenShift ne garantissent pas la continuité d'une base ni l'absence de split-brain sur une application qui écrit des données critiques.

#### 2. Solution et illustration

Définir une autorité d'écriture unique par partition, durabilité prouvée, fencing avant promotion, sauvegardes vérifiées et réconciliation des opérations en vol. Une réplication asynchrone seule ne garantit pas RPO 0.

~~~mermaid
flowchart LR
  A0["Site primaire"]
  A1["panne"]
  A2["fencing prouvé"]
  A3["vérification logs/core"]
  A4["promotion secondaire"]
  A5["réconciliation"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
  A3 --> A4
  A4 --> A5
~~~

**Exemple de bout en bout :** Site A indisponible après commit financier confirmé mais avant réplication; site B n'ouvre pas les écritures tant que les journaux reconnus et les preuves du core ne sont pas réconciliés.

#### 3. Séquence d'exploitation

~~~mermaid
sequenceDiagram
  actor Ar as Architecte / Exploitant
  participant C as Plateforme
  participant W as Service
  Ar->>C: Détecter panne et stopper admission à risque
  C->>W: Prouver fencing de l'ancien propriétaire
  W-->>C: Comparer commits reconnus et journaux survivants
  C-->>Ar: Promouvoir, réconcilier et rouvrir prudemment
~~~

#### 4. Exemple technique (plan illustratif)

~~~yaml
# Runbook READ-ONLY préalable à une bascule, pas commande automatisée
steps:
  - identify_affected_partition
  - freeze_risky_admission
  - prove_old_writer_fenced
  - compare_acknowledged_commits_and_replication
  - reconcile_inflight_with_authoritative_source
  - approve_promotion
  - monitor_duplicate_and_unknown_outcomes
# Toute promotion doit être autorisée par procédure dédiée.
~~~

> Pour utiliser les configurations : remplacer les placeholders fictifs, valider la version API et les contrôleurs disponibles, tenir compte des SCC, et consulter les manifests du cas d'étude. Il ne s'agit pas systématiquement d'un manifeste autonome.

#### 5. Arbitrages et responsabilités

- RPO/RTO issus du BIA et tests d'injection site/zone.
- Snapshot/PITR indépendant de la réplication, clés et restore testés.
- GSLB/DNS ne sérialise pas les écritures : ownership à imposer là où l'effet se produit.

#### 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Split-brain | Fencing token vérifié par stockage/core |
| Réplication async en retard | Stop et rapprochement avant admission |
| Backup illisible | Restore périodique avec preuve |
| Retour ancien site | Failback distinct sans double writer |

#### 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

#### 8. Question d'entretien d'architecte

**Pourquoi « Backup / Restore / Fencing / Controlled Failover » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/REFERENCES.md).

[Retour au programme](README.md)
