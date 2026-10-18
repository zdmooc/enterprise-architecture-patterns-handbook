# Matrice de décision — Docker / Kubernetes / OpenShift

| Besoin | Pattern | Alternative / avertissement |
|---|---|---|
| Compiler sans outillage en production | Multi-Stage Build | Runtime versionné/testé |
| Promouvoir un build identique | Immutable Image | Digest, signature, SBOM |
| Pod compatible politique restrictive | Non-Root / Arbitrary UID | Éviter SCC privilège par défaut |
| Variabiliser dev/preprod/prod | Externalized Configuration | Secrets distincts de ConfigMaps |
| Supporter rescheduling / scaling | Stateless | État durable hors Pod |
| Initialisation pré-app | Init Container | Migration DB en Job contrôlé |
| Telemetry/proxy local | Sidecar | Préférer node-agent ou mesh si moins coûteux |
| Protocole externe difficile | Ambassador | Mesurer latence et complexité |
| Format de log ancien | Adapter | Préférer stdout natif |
| API Java sans état | Deployment | StatefulSet si vraie identité stable |
| Storage propre par réplica | StatefulSet | Ne garantit ni quorum ni DR |
| Traitement ponctuel/périodique | Job/CronJob | Idempotence même en cas de relance |
| Cycle de vie ressource complexe | Operator | CRD, RBAC, finalizers et reconciler tests |
| Démarrage long ou disponibilité | Startup/Readiness/Liveness | Eviter liveness sur dépendance externe |
| Finir transactions en vol | Graceful Shutdown | Recovery après SIGKILL nécessaire |
| Drain volontaire contrôlé | PDB | Aucun effet sur panne brusque |
| Pic de charge CPU | HPA | Core/DB/rails dimensionnés |
| Backlog file de messages | Queue scaling | Autoscaler optionnel + TTL de commandes |
| HA par nœud/zone | Topology Spread | Capacité réellement indépendante |
| Multi-tenant et coûts | Requests/Quotas | OOM/throttling à mesurer |
| Adresses Pods changeantes | Service/DNS | Contrôle identité et network policy |
| Exposition HTTPS externe | OpenShift Route | API Gateway/Gouvernance en sus |
| Segmentation est-ouest | Default-Deny NetworkPolicy | Autorisations explicites, CNI support |
| Réduire privilèges runtime | SCC/RBAC/ServiceAccount | Refuser anyuid sans preuve |
| Secret en production | External Secret/Secret Volume | Rotation et coffre approuvés |
| Mettre à jour sans coupure souhaitée | RollingUpdate | maxSurge et readiness |
| Tester nouvelle version en canary | Canary / Blue Green | Séparer trafic/mutation |
| Reproductibilité de configuration | GitOps | Ne remplace pas tests ni transaction |
| Migrer EAR/WAR progressivement | Strangler Fig | Cartographie complète, licence/support |
| Survivre perte site sans double écriture | Fencing + DR | RPO0 non présumé avec réplication async |

## Arbre de choix

~~~mermaid
flowchart TB
 A{"Application sans état ?"} -->|Oui| D["Deployment + probes + PDB + topology"]
 A -->|Non| S{"Identité/volume ordonné nécessaire ?"}
 S -->|Oui| ST["StatefulSet + réplication applicative + backup"]
 S -->|Non| B["Externaliser l'état et réexaminer Deployment"]
 D --> G{"Besoin scale ?"}
 G -->|CPU| H["HPA"]
 G -->|Queue| K["Autoscaler sur backlog sous limites"]
 D --> I["SCC + NetworkPolicy + GitOps"]
 ST --> I
 B --> I
~~~

Chaque choix exige **preuves d'admission, sécurité, charge, panne et exploitation**.
