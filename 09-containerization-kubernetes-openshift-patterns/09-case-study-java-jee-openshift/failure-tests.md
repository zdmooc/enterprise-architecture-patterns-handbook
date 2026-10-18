# 30 tests de panne — conteneurisation et migration OpenShift

**Objectif :** tests reproductibles, mais **aucun test de production n'est revendiqué exécuté dans ce dépôt**.

| ID | Injection / incident | Résultat attendu / preuve |
|---|---|---|
| K01 | Docker build échoue | Pas d'image publiée sans artefact |
| K02 | Image base compromise/non approuvée | Scan/policy bloquent la promotion |
| K03 | Image mutable modifiée après qualification | Digest de prod stable |
| K04 | Admission SCC UID arbitraire | Pod non-root sans SCC assouplie |
| K05 | Application exige écrire sous /app read-only | Crash explicite puis correction image/volume |
| K06 | ConfigMap clé absente | Erreur contrôlée, aucune config par défaut dangereuse |
| K07 | Secret révoqué | Rotation et redémarrage/reload sans fuite |
| K08 | InitContainer jamais terminé | Pod non ready, alerte et runbook |
| K09 | Sidecar saturé | Isolation ressources, impact borné |
| K10 | Proxy local TLS expiré | Erreur explicite, aucun faux statut métier |
| K11 | Pod Replica 1 supprimé | Autres replicas servent, état hors Pod |
| K12 | Réplica StatefulSet perd son PVC | Remédiation storage, aucune donnée recréée silencieusement |
| K13 | CronJob lancé deux fois | Idempotence métier, un résultat logique |
| K14 | Operator leader tué | Nouveau leader réconcilie sans conflit |
| K15 | Startup Java 45 s | startupProbe évite restart trop tôt |
| K16 | DB externe tombe | Pas de restart storm liveness |
| K17 | SIGTERM pendant requête | Drain et statut durable ou réconciliation |
| K18 | Drain d'un worker | PDB protège évictions volontaires |
| K19 | Node coupé brutalement | PDB seul insuffisant, replicas survivent si réels |
| K20 | Charge CPU x3 | HPA agit sans dépasser capacité DB |
| K21 | Queue backlog puis reprise worker | Scaling sous quotas, duplications dédupliquées |
| K22 | Pods tous dans même zone | Topology spread détecté/corrigé |
| K23 | JVM OOMKill sous limite | Mémoire heap/native corrigée, pas fake failover |
| K24 | Endpoint Pod disparu | Service redirige vers ready endpoints |
| K25 | Route TLS cert expiré | Alarmes et rotation vérifiée |
| K26 | Flux entrant non autorisé | NetworkPolicy default deny le bloque |
| K27 | Token ServiceAccount volé | RBAC minimal, token absent si inutile |
| K28 | Rollout v2 introduit échec | Contrôles progressive delivery et rollback sans perte état |
| K29 | Deux chemins ancien/nouveau exécutent même commande | Fencing/ownership + idempotence empêchent double effet |
| K30 | Perte site après commit avant replication async | Promotion bloquée ou rapprochement complet ; pas de RPO 0 fictif |

### Preuve minimale par test
- Précondition : version image, commit Git, version cluster et namespace.
- Injection : commande ou expérience non destructive dans un environnement de lab autorisé.
- Observation : Pod events, état API, métriques, logs expurgés, statut durable si applicable.
- Invariant : références métier et nombre de vrais effets, sans s'appuyer sur ACK réseau seul.
- Résultat : PASS/FAIL/BLOCKED, hash des preuves, date et responsable.
- Pour les tests destructifs (site, core, stockage), exiger une fenêtre de test, backups et approbation préalable.

Le [lab Java](../../labs/java-openshift-modernization/README.md) ne démontre que les aspects applicatifs/manifestes. Les tests de débit bancaire, split-brain physique et restaurations réelles requièrent un environnement spécialisé.
