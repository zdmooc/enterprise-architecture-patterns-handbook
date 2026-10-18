# 30 — Backup / Restore / Fencing / Controlled Failover

> **Famille : PRA & multi-cluster** · Exemple générique et anonymisé de migration Java/JEE vers OpenShift ; produits cités uniquement en tant que technologies de conception.

## 1. Problème

Deux clusters OpenShift ne garantissent pas la continuité d'une base ni l'absence de split-brain sur une application qui écrit des données critiques.

## 2. Solution et illustration

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

## 3. Séquence d'exploitation

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

## 4. Exemple technique (plan illustratif)

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

## 5. Arbitrages et responsabilités

- RPO/RTO issus du BIA et tests d'injection site/zone.
- Snapshot/PITR indépendant de la réplication, clés et restore testés.
- GSLB/DNS ne sérialise pas les écritures : ownership à imposer là où l'effet se produit.

## 6. Pannes et prévention

| Incident | Comportement requis |
|---|---|
| Split-brain | Fencing token vérifié par stockage/core |
| Réplication async en retard | Stop et rapprochement avant admission |
| Backup illisible | Restore périodique avec preuve |
| Retour ancien site | Failback distinct sans double writer |

## 7. Tests et critères de passage

1. Vérifier contractuellement API/protocoles, identité, privilèges, chiffrement et restrictions réseau.
2. Tester déploiement, mise à jour, rollback/retour arrière et comportement sur crash de Pod ou dépendance.
3. Mesurer latence p95/p99, disponibilité, temps de reprise, consommation et budgets d'admission.
4. Exécuter une injection d'au moins deux modes de panne du tableau avec une preuve reproductible.
5. Documenter propriétaire, runbook d'astreinte et *ce que ce pattern ne garantit pas*.

## 8. Question d'entretien d'architecte

**Pourquoi « Backup / Restore / Fencing / Controlled Failover » ne suffit-il pas, seul, à rendre un paiement bancaire résilient ?** Parce que la stratégie décrite règle un problème d'architecture technique précis, mais ne remplace pas les références financières autoritatives, les transactions, l'idempotence de bout en bout et la réconciliation après perte de réponse.

[Cas d'étude Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [Matrice des patterns](../../DECISION_MATRIX.md) · [Références](../../REFERENCES.md).
