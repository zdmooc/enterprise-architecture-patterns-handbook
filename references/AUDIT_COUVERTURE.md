# Audit de couverture — formation aux dix patterns et architecture intégrée

**Audit réalisé : 18 octobre 2026.** Ce document vérifie la présence dans le dépôt des notions étudiées dans la formation et des **schémas illustratifs**, en langage générique et sans identification de société cliente, prestataire ou éditeur. L'objectif est une **couverture documentaire** ; l'existence des exemples **ne prouve pas** qu'une plateforme est déjà réalisée, testée et qualifiée en production.

## Matrice de vérification

| Partie expliquée | Concepts à retrouver | Emplacement vérifié |
|---|---|---|
| Cadre de besoin | API, messagerie, événements, synchrone/asynchrone et combinaisons | Fiches 01–05 et matrice de décision |
| 01 — Request/Response | appel synchrone, GET statut, POST 202, réponse immédiate, timeout, erreurs, autorisation | [01](../01-integration-patterns/01-request-response/README.md), 3 schémas |
| 02 — Queue | dépôt durable, transport distinct du règlement, consommateurs concurrents, indisponibilité, redélivrance, ACK, DLQ/BOQ | [02](../01-integration-patterns/02-messaging-queue/README.md), 3 schémas |
| 03 — Pub/Sub | topic, plusieurs abonnements, un consommateur arrêté, indépendance, différences avec queue | [03](../01-integration-patterns/03-publish-subscribe/README.md), 3 schémas |
| 04 — EDA | événement métier, chaînes de réaction, commande ≠ fait, Outbox, événements dupliqués/hors ordre | [04](../01-integration-patterns/04-event-driven-architecture/README.md), 3 schémas |
| 05 — Streaming | Kafka, topics, partitions, offsets, consumer groups, lag, retention, replay, fraude sur 5 transactions/20 s | [05](../01-integration-patterns/05-event-streaming/README.md), 3 schémas et table d'exemple |
| 06 — API Gateway | OAuth2/OIDC/JWT/mTLS, scopes, objets métier, rate limit, HTTP, Gateway ≠ API Management ≠ Route | [06](../01-integration-patterns/06-api-gateway/README.md), 3 schémas |
| 07 — Adapter / ACL | JSON ↔ legacy, statuts sémantiques, codes fictifs, MQ, Strangler Fig, erreurs et migration | [07](../01-integration-patterns/07-anti-corruption-layer/README.md), 3 schémas |
| 08 — Saga | orchestration vs chorégraphie, transactions locales, réservations et compensations, pivot irréversible | [08](../01-integration-patterns/08-saga/README.md), 5 schémas |
| 09 — Circuit Breaker | Closed/Open/Half-Open, simulation 20 appels/12 erreurs, timeout, Retry, Bulkhead, repli bancaire | [09](../01-integration-patterns/09-circuit-breaker/README.md), 4 schémas |
| 10 — Retry/Timeout/Idempotency | réponse perdue, clé stable, doublons, Backoff/Jitter, contrainte UNIQUE, Outbox, 6 pannes | [10](../01-integration-patterns/10-retry-timeout-idempotency/README.md), 4 schémas |
| Synthèse des dix patterns | chaîne API → Saga → ACL → MQ/core → événements Kafka/notification ; isolation de sécurité/résilience | [Architecture consolidée](../07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md) et [atlas](../diagrams/INDEX_DES_SCHEMAS.md) |
| Scénarios de panne | latence, réponse perdue, pub/sub consommateur KO, compensation, délai SCT Inst, site perdu | [Atelier séquences](../07-case-studies/banking-payments-reference/sequences.md), [28 scénarios](../07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md) |
| Architecture applicative & technique | Java, OpenShift, données, IAM, brokers selon besoin, coût, sécurité, monitoring, GitOps, PRA | Étude consolidée sections 5–24 |
| Questions d'entretien et vérification des acquis | question/réponse par pattern, quiz récapitulatif corrigé | Chaque fiche et [exercices](EXERCICES_CORRIGES.md) |
| Travaux pratiques | idempotence de requêtes et Outbox transactionnelle avec tests unitaires | [Lab](../labs/idempotency/README.md) |

## Ce qui est présent / ce qui reste à réaliser

**Présent :** 10 fiches enrichies, 34 diagrammes dans ces fiches, 8 diagrammes dans l'étude consolidée, 4 séquences pédagogiques supplémentaires, carte globale, matrices, quiz corrigés, lab Python/SQLite pour prouver la création d'une intention idempotente et Outbox locale.

**À ne pas confondre avec une livraison technique :**
- Pas de cluster bancaire réel ni de liaison à une infrastructure interbancaire.
- Pas de garantie de règlement « exactly-once » en environnement bancaire : elle nécessite un **contrat et des tests de l'autorité financière réelle**.
- Pas de POC de deux sites physiques vérifié par chaos et fencing.
- Pas d'implémentation complète Java et broker de bout en bout dans ce dépôt.
- Les exigences réglementaires sont documentées, mais doivent être **revérifiées et interprétées dans le contexte** du prestataire et du schéma.

## Contrôle d'anonymisation

- Aucune description d'architecture interne attribuée à une entreprise.
- Exemples **banque émettrice**, **banque bénéficiaire**, **système historique**, **core**, **CSM-A**, **service Paiements**, **client fictif**.
- Références techniques conservées sous leurs noms de **produit/standard ou protocole**, lorsque pertinentes (Java, OpenShift, Kafka, MQ, SCT Inst, OAuth2, OIDC, ISO 20022, TIPS), sans attribution à un client ou éditeur nommé.
- Les adresses de sources officielles EPC / BCE / réglementation UE ne sont pas des noms de sociétés clientes ou d'éditeurs.
- Les exemples n'utilisent pas de données bancaires réelles ; identifiants et montants sont fictifs.
