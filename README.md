# Enterprise Architecture Patterns Handbook

**180 patterns : référentiel de 151 fiches historiques complété par 29 fiches d'intégration EIP, GoF Java, décision et Platform Engineering.**

Référentiel d'architecture en français : principes, responsabilités, critères de choix, scénarios d'échec, diagrammes, contrats, sécurité, observabilité et exercices. Les patterns d'intégration utilisent un **virement fictif de 500 €** ; les patterns IA utilisent un **assistant documentaire et des investigations fictives**, sans outil financier opérationnel.

> **Périmètre et confidentialité.** Tous les cas bancaires sont des **illustrations fictives**. Aucun établissement, fournisseur ou client réel n'est identifié ; aucune architecture interne ou configuration de production n'est revendiquée. Les valeurs, noms de files, APIs, formats de messages et seuils sont des exemples à valider.

## Référentiel complet — 180 patterns (151 socle + 29 extensions)

**[Guide de l'architecte senior : choisir parmi 151 patterns](references/GUIDE_ARCHITECTE_151_PATTERNS.md)** · **[Bibliographie et standards](references/ARCHITECTURE_REFERENCES.md)**.

| Famille | Fiches | Cas d'étude, schémas et matrices |
|---|---:|---|
| [10 — Architecture d'entreprise et urbanisation](10-enterprise-architecture-patterns/README.md) | 12 | Capabilities, cartographies SI, cibles, transitions, roadmap, gouvernance |
| [11 — Architecture applicative](11-application-software-patterns/README.md) | 15 | DDD, architecture hexagonale, monolithe modulaire, CQRS |
| [12 — Architecture de données](12-data-architecture-patterns/README.md) | 12 | Data ownership, warehouse, lakehouse, data mesh, CDC |
| [13 — Systèmes distribués et résilience](13-resilience-distributed-systems-patterns/README.md) | 15 | Consensus, quorum, active/active contrôlé, fencing, PRA |
| [14 — Zero Trust et sécurité](14-security-zero-trust-patterns/README.md) | 12 | IAM, PEP/PDP, mTLS, clés, secrets, segmentation |
| [15 — Cloud hybride](15-cloud-hybrid-architecture-patterns/README.md) | 10 | Landing zone, réseaux hybrides, placement et exit |
| [16 — Performance et SRE](16-performance-sre-patterns/README.md) | 10 | Latence, caches, quotas, SLI/SLO, capacity planning |
| [17 — Modernisation du legacy](17-legacy-modernization-patterns/README.md) | 10 | Rehost, replatform, refactor, strangler, cutover |

Chacune des **96 nouvelles fiches** comprend deux diagrammes Mermaid, un exemple fictif, des arbitrages d'architecture, des scénarios d'échec, des tests et une question d'entretien. Chaque famille dispose aussi de son **cas d'étude et sa matrice de décision**. Les techniques déjà couvertes dans les 55 premières fiches sont référencées lorsqu'elles sont réutilisées dans un nouveau contexte, plutôt que présentées comme des inventions différentes.

## Nouveau : 30 patterns Docker / Kubernetes / OpenShift

**[Accéder aux 30 fiches de conteneurisation et de plateforme](09-containerization-kubernetes-openshift-patterns/README.md)** : 60 diagrammes Mermaid, exemples Dockerfile/YAML, sécurité OpenShift, scénarios de panne et questions d'entretien.

- [Étude complète de migration Java/JEE sur OpenShift](09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/README.md).
- [Cinq séquences de migration et de reprise](09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/sequences.md), [playbook WAR/EAR](09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/migration-playbook.md) et [30 tests d'architecture](09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/failure-tests.md).
- [Laboratoire Java / Docker / Kustomize / OpenShift](labs/java-openshift-modernization/README.md), avec Dockerfile, YAML sécurisés et 15 tests statiques.

## Nouveau : 15 patterns d'architecture IA

**[Accéder au parcours complet — Architecture IA](08-ai-architecture-patterns/README.md)**

**[Architecture de référence IA sur OpenShift](08-ai-architecture-patterns/reference-ai-platform-openshift/README.md)** · **[6 séquences de bout en bout](08-ai-architecture-patterns/reference-ai-platform-openshift/sequences.md)** · **[30 scénarios de qualification](08-ai-architecture-patterns/reference-ai-platform-openshift/risks-and-tests.md)**.

15 fiches détaillées (RAG, Advanced RAG, Model Router, Semantic Cache, ReAct/Tool Calling, Planner–Executor, Multi-Agent, Evaluator, Guardrails, HITL, AI Gateway, Model Serving, Fallback, Continuous Evaluation, Event-Driven AI), **30 diagrammes dans ces fiches**, matrice de sélection et laboratoire de contrôle d'accès et d'approbation fictive.

[Laboratoire IA : ACL documentaire, outils et validation humaine](labs/ai-rag-guardrails/README.md) — Python standard uniquement, sans vrai LLM ni connexion bancaire.

## Étude d'architecture de référence — document unique

**[Paiements instantanés SEPA / OpenShift — Architecture consolidée V1.0](07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)**

Document canonique complet : 26 sections, architecture solution et technique, flux entrants/sortants, VoP, ISO 20022, core bancaire, Java/OpenShift, MQ/Kafka, Saga/Outbox, API, cohérence financière, actif-actif et fencing, PRA, conformité SCT Inst, tests d'incidents, arbitrages et critères de qualification. **Une seule étude publiée ; les deux PDF de travail ne figurent pas dans ce dépôt.** Les technologies et configurations sont des propositions pédagogiques à valider, sans prétendre décrire le SI interne d'un établissement réel.

## Parcours illustré et audit de couverture

- **[Formation bancaire — 10 cours d'architecture d'entreprise + exercices corrigés](10-enterprise-architecture-patterns/formation-banque-paiements/README.md)** : fil rouge virement de 500 EUR, Java/JEE, IBM MQ, Kafka, Core Banking, OpenShift, diagrammes et études de migration (cas fictifs).

- **[Atlas des schémas Mermaid — 151 patterns](diagrams/INDEX_DES_SCHEMAS.md)** : 34 schémas dans les fiches d'intégration, 30 schémas dans les fiches IA, et cas transversaux.
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

**Problème → contexte et forces → solution → séquence → exemple fictif → garanties → modes de panne → sécurité/observabilité → compromis → quand éviter → critères de revue d'architecture → questions d'entretien → références.**

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

**V3 — référentiel pédagogique de 151 patterns, huit nouvelles familles et des cas d'étude d'entreprise, applicatifs, données, sécurité, résilience, cloud hybride, SRE et modernisation.** Les exemples doivent être affinés par des tests, des SLO, des contraintes réglementaires et un dossier d'architecture avant tout usage en production.

**Copyright © 2026 Zidane Djamal.** Aucun octroi de licence de réutilisation n'est implicite. Les références externes appartiennent à leurs éditeurs respectifs.

## Lab exécutable

- [Catalogue des 10 travaux pratiques](labs/README.md)
- [Simulation testée d'idempotence et d'Outbox (Python/SQLite)](labs/idempotency/README.md) — quatre tests automatisés (dont appels concurrents).

---

## Extension V4 — 29 fiches appliquées aux missions d'architecture (20/10/2026)

| Famille ajoutée | Nombre | Cas de choix |
|---|---:|---|
| [Enterprise Integration Patterns](18-enterprise-integration-patterns/README.md) | 8 | Outbox, Inbox, Router, Splitter/Aggregator, Claim Check, DLQ, consumers, schémas |
| [GoF Java/JEE](19-java-design-patterns-gof/README.md) | 11 | Strategy, Factories, Command, Decorator, Proxy, Template, Observer, State, Adapter, Singleton |
| [Plateformes décisionnelles](20-decision-management-patterns/README.md) | 5 | Contrat de décision, moteur interchangeable, version, shadow et audit |
| [Platform Engineering](21-platform-engineering-patterns/README.md) | 5 | Plans de contrôle/données, Golden Path, tenancy, politique et cells |
| **Total ajout** | **29** | **180 patterns au total** |

- [Trois études transversales](22-pattern-applications/README.md) : modernisation Java/JEE, intégration CRM, plateforme décisionnelle.
- [Guide de choix V4](references/GUIDE_EXTENSION_180_PATTERNS.md) : problèmes → patterns → preuves → limites.
- [Tests Java GoF](labs/java-gof/README.md) et validation catalogue avec `python scripts/audit-patterns.py`.

Les anciennes références portant « 151 patterns » décrivent le **socle V3**. L'extension V4 ne revendique aucune exécution de logiciel propriétaire ni compatibilité certifiée par un éditeur.

## Historical preservation — modernis-dat (20 Oct 2026)

Original archived source reference(s) are preserved without modifications under [legacy/modernis-dat/](legacy/modernis-dat/MIGRATION.md), with 62 SHA-verified files, including any binary files and original license documents. This is not a claim of runtime validation.

## Historical preservation — historical-architecture (20 Oct 2026)

Original archived source reference(s) are preserved without modifications under [legacy/historical-architecture/](legacy/historical-architecture/MIGRATION.md), with 401 SHA-verified files, including any binary files and original license documents. This is not a claim of runtime validation.
