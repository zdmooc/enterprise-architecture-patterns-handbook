# Matrice de preuves GO/NO-GO — 30 cours Kubernetes/OpenShift (141–170)

> Éléments **à tester** : ne pas les présenter comme réussis en laboratoire avant d'avoir des résultats d'exécution observables.

| Cours | Pattern | Propriété à démontrer | Preuve de validation attendue |
|---:|---|---|---|
| 141 | [Multi-Stage Build](../141-multi-stage-build.md) | Image finale sans outils de compilation | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 142 | [Immutable Image / Digest](../142-immutable-image.md) | Identité exacte de l'image promue par digest | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 143 | [Non-Root / Arbitrary UID](../143-non-root-container.md) | Exécution sous UID arbitraire OpenShift | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 144 | [Externalized Configuration](../144-externalized-configuration.md) | Une image unique, paramètres et secrets externes | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 145 | [Stateless Process](../145-stateless-process.md) | Reprise sur autre pod sans perdre l'état métier | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 146 | [Init Container](../146-init-container.md) | Précondition de démarrage et absence de migration concurrente | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 147 | [Sidecar](../147-sidecar.md) | Sidecar auxiliaire sans altérer la transaction | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 148 | [Ambassador](../148-ambassador.md) | Proxy local sécurisé et non source de décision métier | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 149 | [Adapter Sidecar](../149-adapter-sidecar.md) | Adaptation des métriques legacy sans modifier le métier | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 150 | [Deployment](../150-deployment.md) | Convergence des replicas, sans garantie de règlement | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 151 | [StatefulSet](../151-stateful-workload.md) | Identité et volume persistants, pas HA automatique | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 152 | [Job / CronJob](../152-job-cronjob.md) | Exécution potentiellement répétée, idempotence métier | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 153 | [Operator / Reconciliation](../153-operator-reconciliation.md) | Réconciliation idempotente et status Conditions | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 154 | [Health Probes](../154-health-probes.md) | Readiness versus liveness et dépendances externes | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 155 | [Graceful Shutdown](../155-graceful-shutdown.md) | Drain sous SIGTERM et conservation référence métier | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 156 | [PodDisruptionBudget](../156-pod-disruption-budget.md) | Protection des évictions volontaires seulement | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 157 | [HPA](../157-horizontal-scaling.md) | Scaling mesuré dans la limite du core et du broker | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 158 | [Queue-Based Scaling](../158-queue-based-scaling.md) | Concurrence et backlog MQ sans double effet | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 159 | [Topology Spread](../159-topology-spread.md) | Répartition réelle entre domaines de panne | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 160 | [Resource Governance](../160-resource-governance.md) | Requests/limits adaptés à heap et mémoire native | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 161 | [Service Discovery](../161-service-discovery.md) | Nom stable malgré remplacement des pods | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 162 | [OpenShift Route / TLS](../162-openshift-route-tls.md) | Terminaison TLS et protection jusqu'au backend | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 163 | [NetworkPolicy Default Deny](../163-default-deny-network.md) | Trafic est-ouest interdit par défaut | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 164 | [SCC / Least Privilege](../164-scc-least-privilege.md) | SCC restrictive, UID et ServiceAccount minimal | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 165 | [Secrets Externalization](../165-secrets-externalization.md) | Rotation et révocation sans secrets dans Git | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 166 | [Rolling Update](../166-rolling-update.md) | Migration compatible et reprise de requêtes | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 167 | [Blue/Green / Canary](../167-bluegreen-canary.md) | Contrôle du trafic et décision GO/NO-GO | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 168 | [GitOps Reconciliation](../168-gitops-reconciliation.md) | Drift détecté et sync conforme, sans rollback métier | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 169 | [Strangler Fig / Migration Java/JEE](../169-strangler-fig.md) | Un seul moteur autoritatif à chaque étape de bascule | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |
| 170 | [Backup / DR / Fencing](../170-disaster-recovery-fencing.md) | Pas de double writer entre clusters et reprise prouvée | Manifeste versionné + commande de test + sortie + horodatage et artefact de pipeline |

## Gates d'acceptation proposés
1. **M0 — Inventaire** : runtime Java, dépendances JTA/JMS, EJB, fichiers, sessions, flux et volumes.
2. **M1 — Build** : image immuable, SBOM, signature, scan, non-root et admission restrictive.
3. **M2 — Plateforme** : namespace, quotas, RBAC/SCC, NetworkPolicy, Routes TLS, secrets rotatifs.
4. **M3 — Disponibilité** : probes, topology spread, PDB, graceful shutdown, arrêt forcé et RTO mesuré.
5. **M4 — Scaling** : HPA, queue-based scaling et charge aval à saturation contrôlée.
6. **M5 — Déploiement** : GitOps, drift, prune, rolling/blue-green, versionnage des contrats et rollback technique.
7. **M6 — Financier** : aucune double exécution après retry, perte de réponse et replay MQ.
8. **M7 — PRA** : restauration, rejeu, fermeture ancien writer, fencing, GO/NO-GO et rapprochement.

## Tests négatifs spécifiques
- Tenter d'exécuter une image qui exige root sous SCC restrictive.
- Couper le broker MQ après commit Outbox et avant publication.
- Simuler une réponse HTTP perdue suivie de deux requêtes identiques.
- Promouvoir une mauvaise version de l'image et vérifier rollback technique sans rollback métier.
- Lancer un consumer en parallèle après partition et vérifier une seule mutation autoritative.
- Déployer avec quota mémoire JVM insuffisant et observer OOMKill.
- Supprimer un Pod hors éviction volontaire : confirmer que PDB n'est pas le mécanisme de protection.
- Empêcher le fencing du cluster principal et vérifier que le GO/NO-GO bloque la promotion.

[HLD de référence](architecture-openshift-141-170.md) · [Index des cours](../README.md)
