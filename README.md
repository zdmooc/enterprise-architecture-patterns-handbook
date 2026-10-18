# Enterprise Architecture Patterns Handbook

**De la théorie aux architectures bancaires, Java/JEE et Cloud Native (Kubernetes / OpenShift).**

Référentiel d'architecture en français : principes, responsabilités, critères de choix, scénarios d'échec, diagrammes, contrats, sécurité, observabilité et exercices. Chaque pattern est expliqué à travers un fil conducteur : **un virement bancaire de 500 €**.

> **Périmètre et confidentialité.** Les cas « CAPS » (Crédit Agricole Payment Services) sont des **illustrations fictives** inspirées de besoins génériques d'architecture applicative. Ils ne décrivent ni l'architecture interne, ni les produits effectivement déployés, ni les règles de gestion particulières de CAPS. Les valeurs, noms de files, APIs, formats de messages et seuils sont des exemples à valider.

## Étude d'architecture de référence — document unique

**[Paiements instantanés SEPA / OpenShift — Architecture consolidée V1.0](07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)**

Document canonique complet : 26 sections, architecture solution et technique, flux entrants/sortants, VoP, ISO 20022, core bancaire, Java/OpenShift, MQ/Kafka, Saga/Outbox, API, cohérence financière, actif-actif et fencing, PRA, conformité SCT Inst, tests d'incidents, arbitrages et critères de qualification. **Une seule étude publiée ; les deux PDF de travail ne figurent pas dans ce dépôt.** Les technologies et configurations sont des propositions pédagogiques à valider, sans prétention de décrire le SI interne de CAPS ou BPCE.

## Parcours : 10 patterns d'intégration et de résilience

| # | Pattern | Question de l'architecte |
|---|---|---|
| 01 | [Request/Response](01-integration-patterns/01-request-response/README.md) | Quand un résultat doit-il être obtenu immédiatement ? |
| 02 | [Messaging / Queue](01-integration-patterns/02-messaging-queue/README.md) | Comment découpler producteur et consommateur ? |
| 03 | [Publish/Subscribe](01-integration-patterns/03-publish-subscribe/README.md) | Comment distribuer un fait métier à plusieurs abonnés ? |
| 04 | [Event-Driven Architecture](01-integration-patterns/04-event-driven-architecture/README.md) | Comment organiser les traitements autour d'événements ? |
| 05 | [Event Streaming](01-integration-patterns/05-event-streaming/README.md) | Comment traiter et rejouer des flux durables ? |
| 06 | [API Gateway](01-integration-patterns/06-api-gateway/README.md) | Comment protéger, exposer et gouverner les APIs ? |
| 07 | [Adapter / Anti-Corruption Layer](01-integration-patterns/07-anti-corruption-layer/README.md) | Comment moderniser sans hériter du modèle du legacy ? |
| 08 | [Saga](01-integration-patterns/08-saga/README.md) | Comment coordonner des transactions locales ? |
| 09 | [Circuit Breaker](01-integration-patterns/09-circuit-breaker/README.md) | Comment limiter la propagation des pannes ? |
| 10 | [Retry / Timeout / Idempotency](01-integration-patterns/10-retry-timeout-idempotency/README.md) | Comment reprendre sans doubler un paiement ? |

## Mettre tous les patterns ensemble

- [Atelier pédagogique générique — flux bancaires](07-case-studies/banking-payments-reference/README.md)
- [Séquence de bout en bout et scénarios d'échec](07-case-studies/banking-payments-reference/sequences.md)
- [Matrice de choix des patterns](references/decision-matrix.md)
- [Glossaire](references/glossary.md)
- [Sources publiques et précautions](references/sources.md)

## Convention d'une fiche

**Problème → contexte et forces → solution → séquence → exemple bancaire → garanties → modes de panne → sécurité/observabilité → compromis → quand éviter → critères de revue d'architecture → questions d'entretien → références.**

## Principes non négociables sur le paiement

1. Distinguer **ordre reçu**, **ordre accepté**, **ordre soumis** et **paiement réglé**.
2. Un **timeout** ne prouve jamais qu'un paiement n'a pas eu d'effet.
3. Garantir l'idempotence **jusqu'au système d'exécution**, et pas seulement au niveau HTTP.
4. Une compensation Saga **n'annule pas** automatiquement un règlement irrévocable.
5. Un broker durable n'assure pas à lui seul le traitement métier *exactly once*.
6. Un virement instantané est gouverné par des échéances métier/réglementaires : un message ancien ne doit pas être exécuté aveuglément.
7. Séparer l'autorité financière (cœur bancaire) des vues et projections applicatives.

## Technologies d'illustration

Java / Spring Boot, OpenShift / Kubernetes, PostgreSQL, IBM MQ, Apache Kafka, OAuth 2.0 / OIDC, mTLS, Resilience4j, OpenTelemetry, Prometheus, GitOps / Argo CD. Leur utilisation dans ce dépôt **n'affirme pas** qu'elles sont exploitées chez un client particulier.

## Statut

**V1 — référentiel pédagogique et conception de référence.** Les exemples doivent être affinés par des tests, des SLO, des contraintes réglementaires et un dossier d'architecture avant tout usage en production.

**Copyright © 2026 Zidane Djamal.** Aucun octroi de licence de réutilisation n'est implicite. Les références externes appartiennent à leurs éditeurs respectifs.

## Lab exécutable

- [Catalogue des 10 travaux pratiques](labs/README.md)
- [Simulation testée d'idempotence et d'Outbox (Python/SQLite)](labs/idempotency/README.md) — quatre tests automatisés (dont appels concurrents).
