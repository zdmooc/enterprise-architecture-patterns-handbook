# Cours 07 — Target Architecture Blueprint
**Niveau :** Architecture d'entreprise / solutions | **Progression :** QCM C validé | [Fiche canonique](../07-target-architecture-blueprint/README.md)

## Objectifs
Traduire les besoins métier en une **architecture cible cohérente** métier, fonctionnelle, applicative, données et technique, avec contrats, invariants, exigences NFR et décisions justifiées. Ne pas confondre schéma cible et réalisation démontrée.

## 1. Demande métier de la banque fictive
Moderniser les services de virements SEPA et instantanés, réduire l'obsolescence Java/JEE, maîtriser les incidents, préserver la chaîne financière et éviter les doubles débits. L'existant comporte un moteur Java/JEE sur VM, IBM MQ, Core Banking et passerelle interbancaire. L'hypothèse de cible introduit Java modernisé/OpenShift et Kafka pour les événements dérivés.

## 2. Construire la cible par couches
| Vue | Objets à préciser | Exemple |
|---|---|---|
| Métier | Capacités, valeur, acteurs, règles | Initier, contrôler, exécuter, réconcilier |
| Fonctionnelle | Domaines et responsabilités | Paiements, Clients, Comptes, Fraude |
| Applicative | Services, API, flux et contrats | Payment API, orchestrateur, adaptateur MQ |
| Données | Source de vérité, modèle et propriétaires | Core = exécution financière ; DB = suivi |
| Technique | Runtime, brokers, stockage et sécurité | OpenShift, MQ, Kafka, PostgreSQL |
| Opérations | SLO, risques, PRA, runbook, FinOps | Latence, reprise, restauration testée |

## 3. Blueprint logique et distinction des autorités
~~~mermaid
flowchart TB
  U["Canaux clients"] --> ID["API Gateway / identité / SCA"]
  subgraph MOD["Couche applicative modernisée - OpenShift candidat"]
    API["Payment API Java"]
    O["Orchestrateur / Saga"]
    DB[("PostgreSQL intentions + Outbox")]
    REL["Relay durable commandes"]
    EVT["Relay événements"]
    ACL["Adaptateur de résultats Core"]
    API --> DB
    API --> O
    O --> DB
    DB --> REL
    DB --> EVT
    ACL --> O
  end
  ID --> API
  O --> F["Contrôles / anti-fraude"]
  REL --> Q["IBM MQ"]
  Q --> A["Adaptateur commandes Core"]
  A --> C["Core Banking - autorité financière"]
  C <--> SEPA["Passerelle / rail interbancaire"]
  C -->|"Réponse métier via MQ"| ACL
  EVT --> K["Kafka - faits dérivés"]
  K --> N["Notifications / Reporting"]
~~~
Les flèches sont des **responsabilités logiques** : la route physique, les protocoles exacts, l'outbox de résultats et les unités transactionnelles doivent être détaillés séparément.

## 4. Les invariants avant le choix des produits
1. **Une identité d'ordre stable** pour la déduplication API et Core.
2. **Une autorité financière** : l'état de suivi local et Kafka n'écrivent pas le grand livre.
3. **États distincts** : RECEIVED, VALIDATING, SUBMITTED, SETTLED, REJECTED, UNKNOWN/TO_RECONCILE selon un contrat versionné.
4. **Atomicité locale explicite** : ordre + Outbox dans une transaction DB ; aucune atomicité DB/MQ/Core supposée.
5. **Résultat attesté** : ne déclarer SETTLED qu'après confirmation pertinente de la source autoritative.
6. **Échéance et reprise** : pas de réexécution aveugle d'une instruction SCT Inst expirée.
7. **Audit et confidentialité** : identité, droit d'accès, corrélation, minimisation des données et conservation.

## 5. Arbitrages structurants
| Sujet | Choix candidat | Alternative et critère d'arbitrage |
|---|---|---|
| Moteur Java | Replatform/refactor progressif sur OpenShift | Rehost si support/risque le justifient |
| Core | Préserver source autoritative | Remplacement séparé, gouverné |
| Commandes Core | Conserver IBM MQ durant transition | Kafka ou API : étude de contrats, coût, garanties |
| Événements | Kafka pour abonnés indépendants | MQ Pub/Sub possible si besoin et coûts adaptés |
| API vs asynchrone | Intention durable + suivi de statut | Synchrone complet si contraintes réellement compatibles |
| Saga | Coordination durable avec compensations réversibles | Chorégraphie si parcours et responsabilité maîtrisés |

## 6. NFR et tests à négocier
- Latence : parcours de bout en bout, p95/p99, mesures par rail, dépendance Core, délais réglementaires applicables.
- Résilience : panne pod/nœud, arrêt MQ, réponse perdue, redélivrance et rechute du Core.
- Sécurité : OIDC/SCA appropriée, autorisation par compte/ordre, mTLS où requis, gestion des secrets et journal d'audit.
- Exploitabilité : traces transactionnelles corrélées, queue depth, oldest-message age, consumer lag, incidents et SLO métier.
- PRA : RTO/RPO issus de l'analyse d'impact métier, sauvegardes, restauration, fencing si multi-site.
- Coût et support : licences, qualification des runtimes Java, coûts d'exploitation de la coexistence.

**Un Pod Running et trois réplicas ne constituent pas une preuve de disponibilité de bout en bout.**

## 7. Gouvernance et livrables
Dossier AS-IS ; blueprint à vues multiples ; responsabilités/contrats ; matrice décisions↔exigences ; registre d'invariants ; catalogue NFR et tests ; ADR ; trajectoire de transition ; risques/acceptations.

## 8. Exercice corrigé
Le Core fonctionne, le moteur Java/JEE vieillit. (A) tout remplacer simultanément, (B) conteneuriser sans analyse, (C) moderniser le moteur, garder Core comme autorité et définir MQ/Kafka/NFR/validation.

**Correction : C.** L'architecture découple objectifs métier et options techniques, limite le périmètre de risque et démontre ses garanties.

## 9. Question d'entretien
**« Comment prouvez-vous la pertinence du TO-BE ? »** Chaque bloc se rattache à un besoin, un invariant, une décision arbitrée, un propriétaire et un protocole de test. L'architecture cible est une proposition qualifiable, jamais une preuve de disponibilité à elle seule.

---

## Périmètre et intégrité pédagogique
Tous les exemples représentent un **SI bancaire fictif** et non l'architecture réelle d'un client. Les SLO, volumes, technologies et stratégies sont des hypothèses de conception ; les preuves de production ne sont pas revendiquées. Pour des paiements, un statut de transport n'est pas un règlement, un timeout ne démontre pas un échec, et une compensation applicative ne défait pas nécessairement un règlement irréversible. Les échéances métier et règles effectives du scheme doivent être validées.
