# Architecture cible — Modernisation progressive Java/JEE vers Kubernetes/OpenShift

**Étude de référence complète, anonymisée et pédagogique.** Hypothèse : application Java/JEE historique sous serveur applicatif traditionnel, WAR/EAR, dépendances SQL/JMS, sessions, intégrations batch et external services. **Aucun environnement d'entreprise réel n'est décrit.**

## 1. Besoin et périmètre
Transformer un patrimoine Java/JEE sans perte de fonctionnalité ni affaiblissement de la sécurité, maintenir la continuité d'activité et industrialiser build, images OCI, configuration, déploiement, observabilité et PRA. L'architecture ne présume ni réécriture microservices ni remplacement du core bancaire.

## 2. AS-IS hypothétique : les éléments à découvrir avant tout Dockerfile
| Axe | Inventaire attendu |
|---|---|
| Applications | WAR/EAR, modules EJB, API JAX-RS/SOAP, JSP, ordonnancement et bibliothèques natives |
| Runtime | Version Java, API javax/jakarta, serveur JEE, heap/GC, JDBC/JNDI, providers JMS, datasource |
| Stateful | Sessions mémoire, fichiers temporaires ou persistants, transactions locales/XA, caches |
| Données | DB, schémas, version migration, jobs nocturnes, contraintes de verrouillage |
| Interconnexions | Entrées API, sécurité mTLS/certificats, MQ, fichiers, SOAP, FTP, composants réseau |
| Non-fonctionnel | TPS, latence p95/p99, RTO/RPO, disponibilité, fenêtre de migration |
| Licences | Runtime supporté en conteneur/OpenShift, droit de redistribution, support éditeur |
| Sécurité | Comptes techniques, secrets, firewall, RBAC, correctifs, données sensibles |

### Graphe AS-IS fictif
~~~mermaid
flowchart LR
  C["Canaux externes"] --> LB["Load Balancer"]
  LB --> APP["Serveur applicatif Java/JEE historique"]
  APP --> S[("Base relationnelle")]
  APP --> MQ["Broker de messages"]
  APP --> F["Filesystem partagé"]
  APP --> JOB["Traitements batch"]
~~~

**Règle :** on ne conclut pas « l'application est stateless » seulement parce qu'elle est empaquetée en WAR. Sessions JEE, objets distribués, JNDI, transactions JTA/JMS, filesystem et caches doivent être examinés.

## 3. Architecture TO-BE : simple, contrôlée, progressive
~~~mermaid
flowchart TB
  C["Canaux / partenaires"]
  GW["API Gateway si requise"]
  R["OpenShift Route HTTPS"]
  SVC["Kubernetes Service"]
  P1["Java API Pod v1 / v2"]
  P2["Java API Pod replica"]
  DB[("DB externe / HA qualifiée")]
  MQ["Messagerie existante"]
  ACL["Adapter/ACL historique"]
  OUT["Outbox si double-écriture domaine + message"]
  V["Secrets / PKI approuvés"]
  O["Metrics / logs / traces"]
  GIT["GitOps / Reconciliation"]
  C --> GW --> R --> SVC
  SVC --> P1
  SVC --> P2
  P1 --> ACL --> MQ
  P1 --> DB
  P2 --> DB
  P1 --> OUT
  P1 --> V
  GIT --> P1
  GIT --> P2
  P1 --> O
  P2 --> O
~~~

Cette cible comprend **un petit nombre de capacités démontrées** et plusieurs replicas, pas un microservice obligatoire par classe Java. La persistance demeure sous responsabilité de la solution DB/core. Route, Gateway et ACL ont des rôles distincts.

## 4. Allocation des patterns
| Étape | Patterns mobilisés |
|---|---|
| Dockerisation | 01 Multi-Stage, 02 Immutable, 03 Arbitrary UID, 04 Config, 05 Stateless |
| Pod et services auxiliaires | 06 Init, 07 Sidecar, 08 Ambassador, 09 Adapter (uniquement si justifiés) |
| Workloads et états | 10 Deployment, 11 StatefulSet (si nécessaire), 12 Jobs, 13 Operator (si cycle complexe) |
| Résilience | 14 Probes, 15 Shutdown, 16 PDB, 17 HPA, 18 Queue Scale, 19 Topology, 20 Requests/Quotas |
| Sécurité réseau | 21 Service DNS, 22 Route, 23 NetPolicy, 24 SCC, 25 Secret Manager |
| Livraisons | 26 Rolling, 27 Canary, 28 GitOps |
| Transformation | 29 Strangler |
| PRA | 30 Backup/Restore/Fencing |

## 5. Chemin de déploiement minimal

1. **Découverte:** rendre auditable l'inventaire AS-IS et classer les contraintes bloquantes (licence, JEE API, état local, JTA).
2. **Conteneuriser sans changer le métier:** produire une image immuable, scanner, SBOM, signature et promotion.
3. **Admettre OpenShift:** UID arbitraire, non-root, ports non privilégiés, config externe et secrets protégés ; pas de SCC assouplie par défaut.
4. **Répliquer:** probes, Service, Deployment multi-replicas, état durable séparé, PDB et distribution multi-zone *si zones disponibles*.
5. **Intégrer:** contrats de dépendances SQL/JMS/HTTP, budgets timeout, retries idempotents, ACL et Outbox si nécessaires.
6. **Sécuriser:** NetworkPolicy default-deny, TLS, IAM, ServiceAccount dédié, RBAC réduit, secrets/PKI en rotation.
7. **Déployer:** GitOps, contrôle de promotion, Rolling/Canary/BlueGreen, DB migrations expand-contract.
8. **Prouver:** tests de performance et pannes, invariants métier, RTO/RPO et PRA.
9. **Migrer:** Shadow read-only, route par capacité, cutover avec contrôles d'exclusivité d'écriture, backout testé.
10. **Exploiter:** monitoring, SLO, alertes, runbooks, capacity/FinOps, mise à jour régulière des images.

## 6. Architecture technique des données

- La base durable et le broker doivent avoir **leurs propres exigences HA/backup/retention/reconciliation**.
- Les ressources `emptyDir` servent uniquement aux fichiers transitoires, pas à l'autorité métier.
- StatefulSet attribue noms/PVC ordonnés mais n'implémente pas de réplication financière.
- Pour une migration de DB, utilisez **expand–migrate–contract** ; deux versions applicatives peuvent coexister durant Canary.
- Un Pod restart après effet financier sans ACK doit être repris avec **la même référence métier**, jamais avec une nouvelle intention.

## 7. Sécurité OpenShift

1. SCC restrictive par défaut ; ne pas demander root / hostPath pour une application ordinaire.
2. Image compatible UID attribué dynamiquement par namespace.
3. `runAsNonRoot`, `allowPrivilegeEscalation: false`, `drop: [ALL]`, `seccompProfile: RuntimeDefault`.
4. ServiceAccounts propres aux services, RBAC limité et `automountServiceAccountToken: false` si API K8s non utilisée.
5. Policy réseau ingress/egress minimaliste ; exceptions DNS/probe justifiées.
6. TLS jusqu'à la frontière nécessaire : **Route edge avec backend HTTP** est une démonstration, **Route reencrypt requiert TLS backend**.
7. Secrets récupérés hors code/Git ; rotation et logs sans fuite.

## 8. SLO et performance

Les chiffres du lab sont **purement pédagogiques**. Définir p95/p99, débit nominal et pointe, mémoire JVM totale (heap+metaspace+buffers/threads), CPU throttling, temps au premier résultat, latence DB/JMS, temps de démarrage, capacité de zone survivante et quotas. HPA sur CPU est insuffisant si DB ou rail externe est le goulot.

## 9. HA / multi-cluster / PRA

- **Cluster mono-nœud** : utile pour tests de manifests et conteneurs ; **aucune preuve HA**.
- **Plusieurs workers/zones** : topologySpread, PDB et réplicas HA, vérifiés sur failure domains réels.
- **Deux clusters** : ne pas considérer les données cohérentes parce que deux Deployments sont Ready.
- **Cohérence financière** : un seul writer par partition, fencing et mécanismes de réconciliation.
- **Backup** : snapshots/PITR et restore testé indépendamment de la réplication.
- **RPO** après perte de site ne peut pas être présenté comme zéro avec réplication asynchrone seule.

## 10. Inventaire de tests

Consulter les [séquences](sequences.md), la [matrice de 30 tests](failure-tests.md) et le [guide de migration](migration-playbook.md). L'[atelier Java HTTP](../../labs/java-openshift-modernization/README.md) contient les manifests de démonstration.

## 11. ADR candidates (non validées)

| ADR | Décision candidate | Condition |
|---|---|---|
| P-01 | Conserver logique métier dans serveur compatible jusqu'à preuve de décomposition | Fit-gap Java/JEE, support/licence |
| P-02 | Image OCI multi-stage immuable, UID arbitraire | Tests OpenShift SCC et scan |
| P-03 | Stateless Deployment pour API | Sessions/état effectivement externalisés |
| P-04 | Core/DB et MQ restent autorités distinctes | Tests reprise/idempotence |
| P-05 | Default-deny NetPolicy + RBAC minimal | Flux vérifiés sur cluster réel |
| P-06 | RollingUpdate initial, Canary sur parcours de consultation | Metrics et contrôleur de trafic |
| P-07 | GitOps plus validation en préprod | ADR prune/self-heal, rollback DB |
| P-08 | PDB/topologySpread si plusieurs domaines | Capacité physique disponible |
| P-09 | PRA multi-cluster avec fencing | Tests split brain et RPO |
| P-10 | Replatform/Strangler avant réécriture de moteur | Investissement/risque approuvés |

## 12. Conditions d'acceptation

**GO** : les versions sont supportées, manifestes admis, configurations sans secrets en Git, contrat Java/JEE testé, observabilité opérationnelle, charges/pannes testées, RPO/RTO validés et équipe d'exploitation formée. Un succès du laboratoire **ne vaut pas** certification ni qualification de production.

**© 2026 Zidane Djamal — référence originale pédagogique.**
