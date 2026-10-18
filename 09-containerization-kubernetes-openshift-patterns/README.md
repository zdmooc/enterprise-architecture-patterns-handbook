# 09 — Containerization / Kubernetes / OpenShift Architecture Patterns

**30 patterns de conteneurisation, conception de Pods, exploitation Kubernetes, sécurité OpenShift, déploiement GitOps et modernisation Java/JEE**, chacun avec deux schémas Mermaid, scénario concret, YAML/Dockerfile illustratif, modes de panne, tests et critères de revue.

> **Anonymisation :** toutes les applications, entreprises, éditeurs historiques et établissements présentés sont fictifs. Les noms Docker, Kubernetes, OpenShift, Java, Kafka, etc. sont des **noms de technologies/standards**, pas des références à une entreprise cliente. Les URLs de registry en \`example.invalid\` sont volontairement non fonctionnelles. Les détails de support et versions sont à vérifier sur l'installation réelle.

## Parcours des 30 patterns

| Famille | N° | Fiche |
|---|---:|---|
| Images et conteneurs | 01 | [Multi-Stage Build](01-container-design/01-multi-stage-build/README.md) |
| | 02 | [Immutable Image / digest](01-container-design/02-immutable-image/README.md) |
| | 03 | [Non-Root / Arbitrary UID](01-container-design/03-non-root-container/README.md) |
| | 04 | [Externalized Configuration](01-container-design/04-externalized-configuration/README.md) |
| | 05 | [Stateless Process](01-container-design/05-stateless-process/README.md) |
| Design des Pods | 06 | [Init Container](02-pod-design/06-init-container/README.md) |
| | 07 | [Sidecar](02-pod-design/07-sidecar/README.md) |
| | 08 | [Ambassador](02-pod-design/08-ambassador/README.md) |
| | 09 | [Adapter Sidecar](02-pod-design/09-adapter-sidecar/README.md) |
| Workloads / Controller | 10 | [Deployment](03-workload-design/10-deployment/README.md) |
| | 11 | [StatefulSet](03-workload-design/11-stateful-workload/README.md) |
| | 12 | [Job / CronJob](03-workload-design/12-job-cronjob/README.md) |
| | 13 | [Operator / Reconciliation](03-workload-design/13-operator-reconciliation/README.md) |
| Résilience et capacité | 14 | [Health Probes](04-resilience-scaling/14-health-probes/README.md) |
| | 15 | [Graceful Shutdown](04-resilience-scaling/15-graceful-shutdown/README.md) |
| | 16 | [PodDisruptionBudget](04-resilience-scaling/16-pod-disruption-budget/README.md) |
| | 17 | [HPA](04-resilience-scaling/17-horizontal-scaling/README.md) |
| | 18 | [Queue-Based Scaling](04-resilience-scaling/18-queue-based-scaling/README.md) |
| | 19 | [Topology Spread](04-resilience-scaling/19-topology-spread/README.md) |
| | 20 | [Resource Governance](04-resilience-scaling/20-resource-governance/README.md) |
| Réseau / sécurité | 21 | [Service Discovery](05-network-security/21-service-discovery/README.md) |
| | 22 | [OpenShift Route / TLS](05-network-security/22-openshift-route-tls/README.md) |
| | 23 | [NetworkPolicy Default Deny](05-network-security/23-default-deny-network/README.md) |
| | 24 | [SCC / Least Privilege](05-network-security/24-scc-least-privilege/README.md) |
| | 25 | [Secrets Externalization](05-network-security/25-secrets-externalization/README.md) |
| Livraison / migration / PRA | 26 | [Rolling Update](06-gitops-delivery/26-rolling-update/README.md) |
| | 27 | [Blue/Green / Canary](06-gitops-delivery/27-bluegreen-canary/README.md) |
| | 28 | [GitOps Reconciliation](06-gitops-delivery/28-gitops-reconciliation/README.md) |
| | 29 | [Strangler Fig / Migration Java/JEE](07-legacy-modernization/29-strangler-fig/README.md) |
| | 30 | [Backup / DR / Fencing](08-multicluster-dr/30-disaster-recovery-fencing/README.md) |

## Atelier transversal Java/JEE / OpenShift

- **[Architecture de référence et parcours pas à pas](09-case-study-java-jee-openshift/README.md)** : AS-IS, décisions, cible, composants, sécurité, capacité, ADR.
- [Séquences nominales et de panne](09-case-study-java-jee-openshift/sequences.md).
- [Stratégie de migration WAR/EAR : inventaire, POC, shadow, bascule](09-case-study-java-jee-openshift/migration-playbook.md).
- [30 tests de panne et d'admission](09-case-study-java-jee-openshift/failure-tests.md).
- [Laboratoire Java conteneurisé et manifests](../labs/java-openshift-modernization/README.md) : Dockerfile multi-stage, microservice HTTP Java standard, Kubernetes manifests, Route OpenShift optionnelle, tests et commandes de validation.
- [Matrice de sélection des patterns](DECISION_MATRIX.md).
- [Références techniques officielles](REFERENCES.md).

## Distinctions indispensables

1. **Une image Docker/OCI n'est pas une architecture HA** : l'orchestration, les données et les dépendances restent à définir.
2. **ReplicaSet / Deployment n'est pas un système transactionnel** ; il remplace des Pods, pas les paiements.
3. **StatefulSet n'est pas une base HA** : il gère identité/stockage, mais le consensus, les backups et les tests appartiennent à la solution.
4. **PDB ne couvre pas les pannes brutales** ; il influence les évictions volontaires.
5. **HPA ne crée pas du débit bancaire** si une dépendance externe a un plafond.
6. **SCC restrictive + UID arbitraire** : une image compatible doit supporter un UID non fixé à la construction.
7. **GitOps ne fait pas rollback d'une transaction métier** ni d'un schéma SQL incompatible.
8. **Multi-cluster actif-actif ne signifie pas deux writers financiers pour la même partition** ; fencing et preuve de durabilité priment.
9. **Canary** et **blue/green** décrivent la gestion des versions et du trafic ; leur implémentation exacte dépend du contrôleur de routage.
10. Le cas d'étude est une **référence pédagogique**, pas l'attestation qu'une application Java/JEE historique est techniquement ou contractuellement supportée sur OpenShift.

**Copyright © 2026 Zidane Djamal. Tous droits réservés.**
