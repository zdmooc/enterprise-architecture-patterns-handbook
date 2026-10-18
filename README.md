# Enterprise Architecture Patterns Handbook

**De la théorie aux architectures bancaires, Java/JEE et Cloud Native (Kubernetes / OpenShift).**

Référentiel d'architecture en français : principes, responsabilités, critères de choix, scénarios d'échec, diagrammes, contrats, sécurité, observabilité et exercices. Chaque pattern est expliqué à travers un fil conducteur : **un virement bancaire de 500 €**.

> **Périmètre et confidentialité.** Tous les cas bancaires sont des **illustrations fictives**. Aucun établissement, fournisseur ou client réel n'est identifié ; aucune architecture interne ou configuration de production n'est revendiquée. Les valeurs, noms de files, APIs, formats de messages et seuils sont des exemples à valider.

## Étude d'architecture de référence — document unique

**[Paiements instantanés SEPA / OpenShift — Architecture consolidée V1.0](07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)**

Document canonique complet : 26 sections, architecture solution et technique, flux entrants/sortants, VoP, ISO 20022, core bancaire, Java/OpenShift, MQ/Kafka, Saga/Outbox, API, cohérence financière, actif-actif et fencing, PRA, conformité SCT Inst, tests d'incidents, arbitrages et critères de qualification. **Une seule étude publiée ; les deux PDF de travail ne figurent pas dans ce dépôt.** Les technologies et configurations sont des propositions pédagogiques à valider, sans prétendre décrire le SI interne d'un établissement réel.

## Parcours illustré et audit de couverture

- **[Atlas des schémas Mermaid — 10 patterns](diagrams/INDEX_DES_SCHEMAS.md)** : 34 diagrammes dans les dix fiches, navigation par scénario, carte transversale.
- **[Audit de couverture des notions étudiées](references/AUDIT_COUVERTURE.md)** : correspondance détaillée entre cours, exemples, diagrammes et fichiers.
- **[10 exercices corrigés et cas transversal](references/EXERCICES_CORRIGES.md)** : auto-évaluation par pattern et panne multisite.
- Tous les noms d'établissements, de sociétés clientes, de fournisseurs et d'éditeurs sont **neutralisés** dans les documents publiés sur la branche courante.

## Architecture IA — 15 patterns supplémentaires

**[Accéder au référentiel IA générative, agentique et MLOps](08-ai-architecture-patterns/README.md)** : quinze fiches illustrées (RAG, Advanced RAG, Router, cache, agents, Guardrails, HITL, AI Gateway, Serving, évaluation, EDA IA), schémas Mermaid et tests d'architecture.

- [Architecture IA de référence sur OpenShift](08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) : RAG et ACL, services d'inférence, outils, contrôle humain, sécurité et résilience.
- [Matrice de décision IA](08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md).
- [Laboratoire Python IA : RAG ACL, politiques et approbations](labs/ai-rag-guardrails/README.md).

Ce référentiel est **générique et anonymisé**, sans noms d'entreprises clientes ni revendication de déploiement de production.

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

Java / Spring Boot, OpenShift / Kubernetes, PostgreSQL, messagerie MQ, Apache Kafka, OAuth 2.0 / OIDC, mTLS, Resilience4j, OpenTelemetry, Prometheus, GitOps / Argo CD. Leur utilisation dans ce dépôt **n'affirme pas** qu'elles sont exploitées chez un client particulier.

## Statut

**V1 — référentiel pédagogique et conception de référence.** Les exemples doivent être affinés par des tests, des SLO, des contraintes réglementaires et un dossier d'architecture avant tout usage en production.

**Copyright © 2026 Zidane Djamal.** Aucun octroi de licence de réutilisation n'est implicite. Les références externes appartiennent à leurs éditeurs respectifs.

## Lab exécutable

- [Catalogue des 10 travaux pratiques](labs/README.md)
- [Simulation testée d'idempotence et d'Outbox (Python/SQLite)](labs/idempotency/README.md) — quatre tests automatisés (dont appels concurrents).
