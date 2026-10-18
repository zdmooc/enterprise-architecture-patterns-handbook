# Playbook — migrer WAR/EAR Java/JEE vers OpenShift

## Phase 0 — Clarifier les décisions
Définir le périmètre : **rehost, replatform, refactor ou re-architect**. Un conteneur est un moyen d'exécution, pas une justification d'éclatement en microservices.

### Inventaire des EAR/WAR
| Objet | Comment vérifier | Risque |
|---|---|---|
| WAR/EAR/EJB | Inventaire de l'archive, manifestes, libs embarquées | APIs et classloading non supportés |
| Java cible | `java -version` et compilation | Compatibilité bytecode / TLS / drivers |
| JNDI | Fichiers de config, datasources et factories | Ressource liée au serveur historique |
| JMS/MQ | Queue, topics, XA, redélivrance, correlation IDs | Effets métier doubles |
| DB | JDBC, SQL, séquences, batch, migrations | Schéma partagé et transactions |
| Filesystem | Lecture/écriture locales, partages NFS | Perte de données au restart |
| Sessions | In-memory, sticky, cluster session manager | Perte de session en scale-out |
| Threads | Executors manuels, timers du serveur | Lifecycle non géré sous SIGTERM |
| Sécurité | Certificats keystore, secret files, JCE, JAAS | Identifiants en image |
| Licences | Contrat runtime/support de conteneurisation | Déploiement techniquement possible mais non supporté |

**Ne jamais publier d'archives WAR/EAR commerciales ou données clients dans ce dépôt.** Utiliser un simulateur Java standard pour les ateliers.

## Phase 1 — Préflight technique en lecture seule
Collecter versions, CPU/mémoire, JVM options, dépendances, DNS, egress firewall, certificats, volumes, consommation réelle, file MQ depth, métriques de threads, connexions SQL et tracés d'usage. Cartographier les flux et identifier les owners.

## Phase 2 — Conteneurisation minimale
- Définir runtime Java et serveur JEE/servlet supporté ; packager WAR/EAR en respectant les licences.
- Compiler par multi-stage, images signées et scannées ; ports non privilégiés.
- Externaliser Configuration/Secrets ; rediriger logs vers stdout/stderr.
- Préparer répertoires pour UID arbitraire ; supprimer toute nécessité root.
- Vérifier que runtime, plugins et librairies natives sont compatibles OS/architecture/image.

## Phase 3 — Kubernetes/OpenShift
- Deployment ou StatefulSet selon vrai état applicatif, Service, probes, shutdown, requests/limits.
- SCC restrictive, ServiceAccount dédié, NetworkPolicy, Route TLS adéquate, droits minimaux.
- Config, Secret, credentials externes, stockage persistant seulement où requis.
- Ajuster cluster mono-nœud (lab) versus zones réelles (HA).

## Phase 4 — Contrats et dépendances
Rédiger contrats OpenAPI/AsyncAPI si utile, MQ et JDBC, timeouts, policies de retry, ACL des adaptateurs. Test idempotence métier, DB failure, message DUP/reorder et soumission après deadline.

## Phase 5 — Shadow, canary, cutover
~~~mermaid
flowchart LR
 A["Existant autoritatif"] --> B["Shadow READ-ONLY"]
 B --> C{"Tests et écarts 0 critique ?"}
 C -->|Non| FIX["Correction"]
 C -->|Oui| CANARY["Canary contrôlé par capacité"]
 CANARY --> CUT["Cutover unique writer + monitoring"]
 CUT --> DONE["Décommission après preuves"]
~~~
- Shadow : **aucune émission double** (transactions réelles, notifications sensibles et écritures exclues).
- Canary : limiter au périmètre approuvé, même base/contrats compatibles, metrics p99.
- Cutover : geler admission concernée, drainer, réconcilier références en vol, transférer ownership et rouvrir.
- Rollback : code uniquement si données et contrats compatibles ; ne revient pas sur un effet financier irréversible.

## Phase 6 — PRA et exploitation
RTO/RPO par capacité, backups et restore, fencing, runbooks, rotation de certificats, patchs réguliers, SLO métiers, budget de ressources et coûts de la solution. Tester panne de zone/site **avant** toute promesse de résilience.

## Critères de décision finale
Toute migration doit être **approuvée** avec preuves du support runtime/licence, résultats comparatifs, risque résiduel, failback, performance de pointe et gouvernance. Un Pod « Running » est seulement un signal technique partiel.
