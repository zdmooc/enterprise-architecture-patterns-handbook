# Formation complète — 170 cours d'architecture appliqués aux paiements bancaires

**170 cours publiés avec exemple bancaire, décisions, risques, tests et exercice corrigé.** Parcours progressif : métier → fonctionnel → applicatif → design patterns Java.

Référentiel : [Architecture d'entreprise](../README.md) · [Handbook de patterns](../../README.md).

> **Pédagogie et anonymisation.** Cas fictif d'une banque traitant des virements SEPA et instantanés de 500 EUR ; aucun SI client, dessin confidentiel ni performance de production n'est reproduit. Les produits Java, IBM MQ, Kafka, PostgreSQL et OpenShift sont des exemples techniques, pas une déclaration de technologie chez un établissement. La conformité aux règles de paiement doit être examinée sur les textes applicables.

## Objectif du parcours
Savoir partir de la stratégie et des capacités métier, expliquer le parcours de valeur, attribuer des responsabilités, cartographier les applications et les flux, puis préparer une modernisation progressive avec une architecture cible argumentée, un plan de transition, une roadmap et un catalogue ABB/SBB.

## Index — cours 01 à 12 (architecture d'entreprise)
| N° | Leçon | Question de l'architecte | Fiche source | Exercice |
|---:|---|---|---|---|
| 01 | [Business Capability Mapping](01-business-capability.md) | Que doit savoir faire la banque ? | [01](../01-business-capability-mapping/README.md) | B corrigé |
| 02 | [Value Stream Mapping](02-value-stream.md) | Où la valeur et le temps se perdent-ils ? | [02](../02-value-stream-mapping/README.md) | B corrigé |
| 03 | [Business Domain Architecture](03-business-domains.md) | Qui porte les responsabilités et données maîtresses ? | [03](../03-business-domain-architecture/README.md) | B corrigé |
| 04 | [Application Landscape](04-application-landscape.md) | Quelles applications et dépendances réelles ? | [04](../04-application-landscape/README.md) | B corrigé |
| 05 | [Enterprise Flow Mapping](05-enterprise-flow-mapping.md) | Qui échange quoi, comment et sous quelle garantie ? | [05](../05-enterprise-flow-mapping/README.md) | B corrigé |
| 06 | [Portfolio Rationalization / TIME](06-portfolio-rationalization.md) | Quoi conserver, investir, migrer ou retirer ? | [06](../06-application-portfolio-rationalization/README.md) | B corrigé |
| 07 | [Target Architecture Blueprint](07-target-architecture.md) | Quelle cible métier/applicative/technique défendre ? | [07](../07-target-architecture-blueprint/README.md) | C corrigé |
| 08 | [Transition Architecture](08-transition-architecture.md) | Comment faire coexister et basculer sans double débit ? | [08](../08-transition-architecture/README.md) | B corrigé |
| 09 | [Transformation Roadmap](09-transformation-roadmap.md) | Quelles vagues et quelles gates GO/NO-GO ? | [09](../09-transformation-roadmap/README.md) | C corrigé |
| 10 | [ABB / SBB](10-architecture-building-blocks.md) | Quel contrat d'architecture et quelle solution le réalise ? | [10](../10-architecture-building-blocks/README.md) | B corrigé |
| 11 | [Architecture Governance / ADR](11-architecture-governance-adr.md) | Qui décide et sur quelles preuves ? | [11](../11-architecture-governance-adr/README.md) | À valider en session |
| 12 | [Architecture Compliance / NFR](12-architecture-compliance-nfr.md) | Comment prouver la conformité aux exigences ? | [12](../12-architecture-compliance-nfr/README.md) | À étudier et valider |

## Index — cours 13 à 170
| N° | Cours | Domaine | Corrigé |
|---:|---|---|---|
| 13 | [Business Process Architecture et BPMN](13-business-process-bpmn.md) | Métier | C (corrigé dans le cours) |
| 14 | [Business Actors, Pools, Lanes et RACI](14-actors-pools-lanes-raci.md) | Métier | B (corrigé dans le cours) |
| 15 | [Business Rules Architecture](15-business-rules.md) | Métier | A (corrigé dans le cours) |
| 16 | [Business Information Model](16-business-information-model.md) | Métier | B (corrigé dans le cours) |
| 17 | [Business State Model](17-business-state-model.md) | Métier | C (corrigé dans le cours) |
| 18 | [Business Events Architecture](18-business-events.md) | Métier | A (corrigé dans le cours) |
| 19 | [Business KPI, SLA et SLO](19-business-kpi-sla.md) | Métier | B (corrigé dans le cours) |
| 20 | [Business Architecture AS-IS et TO-BE](20-business-as-is-to-be.md) | Métier | C (corrigé dans le cours) |
| 21 | [Synthèse d'architecture métier](21-business-architecture-synthesis.md) | Métier | A (corrigé dans le cours) |
| 22 | [Introduction à l'architecture fonctionnelle](22-functional-architecture-introduction.md) | Fonctionnelle | B (corrigé dans le cours) |
| 23 | [Décomposition fonctionnelle](23-functional-decomposition.md) | Fonctionnelle | B (corrigé dans le cours) |
| 24 | [Flux fonctionnels](24-functional-flows.md) | Fonctionnelle | C (corrigé dans le cours) |
| 25 | [Contrats fonctionnels](25-functional-contracts.md) | Fonctionnelle | A (corrigé dans le cours) |
| 26 | [Gestion fonctionnelle des exceptions](26-functional-exceptions.md) | Fonctionnelle | B (corrigé dans le cours) |
| 27 | [Orchestration fonctionnelle](27-functional-orchestration.md) | Fonctionnelle | C (corrigé dans le cours) |
| 28 | [Orchestration et chorégraphie](28-orchestration-vs-choreography.md) | Fonctionnelle | A (corrigé dans le cours) |
| 29 | [Responsabilités et source autoritative](29-functional-responsibility-authoritative-source.md) | Fonctionnelle | B (corrigé dans le cours) |
| 30 | [Traçabilité fonctionnelle](30-functional-traceability.md) | Fonctionnelle | C (corrigé dans le cours) |
| 31 | [Analyse d'impact fonctionnelle](31-functional-impact-analysis.md) | Fonctionnelle | B (corrigé dans le cours) |
| 32 | [Tests de non-régression fonctionnelle](32-functional-non-regression.md) | Fonctionnelle | C (corrigé dans le cours) |
| 33 | [Critères d'acceptation fonctionnelle](33-functional-acceptance-criteria.md) | Fonctionnelle | B (corrigé dans le cours) |
| 34 | [Dossier d'architecture fonctionnelle](34-functional-architecture-dossier.md) | Fonctionnelle | C (corrigé dans le cours) |
| 35 | [Introduction à l'architecture applicative](35-application-architecture-introduction.md) | Applicative | B (corrigé dans le cours) |
| 36 | [Layered Architecture](36-layered-architecture.md) | Applicative | C (corrigé dans le cours) |
| 37 | [Architecture hexagonale : Ports & Adapters](37-hexagonal-ports-adapters.md) | Applicative | B (corrigé dans le cours) |
| 38 | [Clean Architecture](38-clean-architecture.md) | Applicative | B (corrigé dans le cours) |
| 39 | [Modular Monolith](39-modular-monolith.md) | Applicative | C (corrigé dans le cours) |
| 40 | [Microservices Decomposition](40-microservices-decomposition.md) | Applicative | B (corrigé dans le cours) |
| 41 | [DDD : Bounded Context](41-ddd-bounded-context.md) | Applicative | B (corrigé dans le cours) |
| 42 | [DDD : Aggregate et invariants](42-aggregate-invariants.md) | Applicative | C (corrigé dans le cours) |
| 43 | [CQRS](43-cqrs-read-write.md) | Applicative | B (corrigé dans le cours) |
| 44 | [Event Sourcing](44-event-sourcing.md) | Applicative | C (corrigé dans le cours) |
| 45 | [API Contract First](45-api-contract-first.md) | Applicative | B (corrigé dans le cours) |
| 46 | [Dependency Inversion](46-dependency-inversion.md) | Applicative | A (corrigé dans le cours) |
| 47 | [Anti-Corruption Layer](47-anti-corruption-layer.md) | Applicative | B (corrigé dans le cours) |
| 48 | [Backend for Frontend](48-backend-for-frontend.md) | Applicative | B (corrigé dans le cours) |
| 49 | [Unit of Work](49-unit-of-work.md) | Applicative | C (corrigé dans le cours) |
| 50 | [Branch by Abstraction](50-branch-by-abstraction.md) | Applicative | B (corrigé dans le cours) |
| 51 | [Factory Method (Java GoF)](51-factory-method.md) | Java / GoF | B (corrigé dans le cours) |
| 52 | [Abstract Factory (Java GoF)](52-abstract-factory.md) | Java / GoF | C (corrigé dans le cours) |
| 53 | [Builder (Java GoF)](53-builder.md) | Java / GoF | C (validé en session) |
| 54 | [Prototype (Java GoF)](54-prototype.md) | Java / GoF | A (validé en session) |
| 55 | [Singleton (Java GoF)](55-singleton.md) | Java / GoF | B (validé en session) |
| 56 | [Adapter (Java GoF)](56-adapter.md) | Java / GoF | C (validé en session) |
| 57 | [Bridge (Java GoF)](57-bridge.md) | Java / GoF | B (validé en session) |
| 58 | [Composite (Java GoF)](58-composite.md) | Java / GoF | C (validé en session) |
| 59 | [Decorator (Java GoF)](59-decorator.md) | Java / GoF structurel | Étudié, auto-évaluation à valider |
| 60 | [Facade (Java GoF)](60-facade.md) | Java / GoF structurel | Étudié, auto-évaluation à valider |
| 61 | [Flyweight (Java GoF)](61-flyweight.md) | Java / GoF structurel | Étudié, auto-évaluation à valider |
| 62 | [Proxy (Java GoF)](62-proxy.md) | Java / GoF structurel | B correct ; réponse A corrigée en session |
| 63 | [Chain of Responsibility (GoF)](63-chain-of-responsibility.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 64 | [Command (GoF)](64-command.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 65 | [Interpreter (GoF)](65-interpreter.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 66 | [Iterator (GoF)](66-iterator.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 67 | [Mediator (GoF)](67-mediator.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 68 | [Memento (GoF)](68-memento.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 69 | [Observer (GoF)](69-observer.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 70 | [State (GoF)](70-state.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 71 | [Strategy (GoF)](71-strategy.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 72 | [Template Method (GoF)](72-template-method.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 73 | [Visitor (GoF)](73-visitor.md) | Java / GoF comportemental | Étudié ; quiz individuel à valider |
| 74 | [Dependency Injection](74-dependency-injection.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 75 | [Inversion of Control (IoC)](75-inversion-of-control.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 76 | [Bean Scopes et Lifecycle](76-bean-scopes-lifecycle.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 77 | [Spring AOP](77-spring-aop.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 78 | [Spring Transactions](78-spring-transactions.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 79 | [Spring Data / JPA](79-spring-data-jpa.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 80 | [Spring MVC / REST](80-spring-mvc-rest.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 81 | [Exception Handling Spring](81-exception-handling.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 82 | [Tests unitaires et d'intégration](82-spring-testing.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 83 | [Configuration Spring Boot](83-spring-boot-configuration.md) | Java/JEE et Spring | Corrigé publié ; quiz individuel à valider |
| 84 | [Request/Response](84-request-response.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 85 | [Messaging / Queue IBM MQ/JMS](85-messaging-queue.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 86 | [Publish/Subscribe](86-publish-subscribe.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 87 | [Event-Driven Architecture](87-event-driven-architecture.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 88 | [Event Streaming (Kafka)](88-event-streaming.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 89 | [API Gateway](89-api-gateway.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 90 | [Adapter / Anti-Corruption Layer](90-anti-corruption-layer-integration.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 91 | [Saga](91-saga-integration.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 92 | [Circuit Breaker](92-circuit-breaker-integration.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 93 | [Retry / Timeout / Idempotency](93-retry-timeout-idempotency.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 94 | [Transactional Outbox](94-transactional-outbox.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 95 | [Transactional Inbox](95-transactional-inbox.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 96 | [Content-Based Router](96-content-based-router.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 97 | [Splitter / Aggregator](97-splitter-aggregator.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 98 | [Claim Check](98-claim-check.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 99 | [Dead Letter Channel / Parking Lot](99-dead-letter-channel.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 100 | [Competing Consumers](100-competing-consumers.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 101 | [Event Schema Evolution](101-schema-evolution.md) | Intégration | Corrigé publié ; quiz individuel à valider |
| 102 | [Data Ownership](102-data-ownership.md) | Données | Corrigé publié ; quiz individuel à valider |
| 103 | [Data Warehouse](103-data-warehouse.md) | Données | Corrigé publié ; quiz individuel à valider |
| 104 | [Data Lake](104-data-lake.md) | Données | Corrigé publié ; quiz individuel à valider |
| 105 | [Lakehouse](105-lakehouse.md) | Données | Corrigé publié ; quiz individuel à valider |
| 106 | [Data Mesh](106-data-mesh.md) | Données | Corrigé publié ; quiz individuel à valider |
| 107 | [Data Fabric](107-data-fabric.md) | Données | Corrigé publié ; quiz individuel à valider |
| 108 | [Change Data Capture](108-change-data-capture.md) | Données | Corrigé publié ; quiz individuel à valider |
| 109 | [Data Vault](109-data-vault.md) | Données | Corrigé publié ; quiz individuel à valider |
| 110 | [Medallion Architecture](110-medallion.md) | Données | Corrigé publié ; quiz individuel à valider |
| 111 | [Data Product Contract](111-data-product-contract.md) | Données | Corrigé publié ; quiz individuel à valider |
| 112 | [Master Data Management](112-master-data-management.md) | Données | Corrigé publié ; quiz individuel à valider |
| 113 | [Data Lineage & Governance](113-data-lineage-governance.md) | Données | Corrigé publié ; quiz individuel à valider |
| 114 | [Active / Passive](114-active-passive.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 115 | [Active / Active Partitioned](115-active-active-partitioned.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 116 | [Quorum / Consensus](116-quorum-consensus.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 117 | [Leader Election](117-leader-election.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 118 | [Fencing Token](118-fencing-token.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 119 | [Failure Detector](119-failure-detector.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 120 | [Backpressure](120-backpressure.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 121 | [Bulkhead](121-bulkhead.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 122 | [Load Shedding](122-load-shedding.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 123 | [Graceful Degradation](123-graceful-degradation.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 124 | [Replication & Consistency](124-replication-consistency.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 125 | [Backup / PITR](125-backup-pitr.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 126 | [Chaos Engineering](126-chaos-engineering.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 127 | [Disaster Recovery Runbook](127-disaster-recovery-runbook.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 128 | [Reconciliation / Unknown Outcome](128-reconciliation-unknown-outcome.md) | Résilience | Corrigé publié ; quiz individuel à valider |
| 129 | [Zero Trust / Never Trust by Network](129-zero-trust.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 130 | [PDP / PEP](130-policy-decision-enforcement.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 131 | [Defense in Depth](131-defense-in-depth.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 132 | [Identity Federation / OIDC](132-identity-federation.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 133 | [Workload Identity](133-workload-identity.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 134 | [RBAC / ABAC / BOLA](134-rbac-abac.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 135 | [Secret Lifecycle](135-secret-lifecycle.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 136 | [Mutual TLS / PKI](136-mutual-tls-pki.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 137 | [Network Micro-Segmentation](137-network-microsegmentation.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 138 | [Encryption at Rest / KMS](138-encryption-key-management.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 139 | [Software Supply Chain](139-software-supply-chain.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 140 | [Audit Trail / Segregation of Duties](140-audit-segregation-duties.md) | Sécurité et Zero Trust | Corrigé théorique ; quiz individuel à valider |
| 141 | [Multi-Stage Build](141-multi-stage-build.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 142 | [Immutable Image / Digest](142-immutable-image.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 143 | [Non-Root / Arbitrary UID](143-non-root-container.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 144 | [Externalized Configuration](144-externalized-configuration.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 145 | [Stateless Process](145-stateless-process.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 146 | [Init Container](146-init-container.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 147 | [Sidecar](147-sidecar.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 148 | [Ambassador](148-ambassador.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 149 | [Adapter Sidecar](149-adapter-sidecar.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 150 | [Deployment](150-deployment.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 151 | [StatefulSet](151-stateful-workload.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 152 | [Job / CronJob](152-job-cronjob.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 153 | [Operator / Reconciliation](153-operator-reconciliation.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 154 | [Health Probes](154-health-probes.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 155 | [Graceful Shutdown](155-graceful-shutdown.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 156 | [PodDisruptionBudget](156-pod-disruption-budget.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 157 | [HPA](157-horizontal-scaling.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 158 | [Queue-Based Scaling](158-queue-based-scaling.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 159 | [Topology Spread](159-topology-spread.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 160 | [Resource Governance](160-resource-governance.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 161 | [Service Discovery](161-service-discovery.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 162 | [OpenShift Route / TLS](162-openshift-route-tls.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 163 | [NetworkPolicy Default Deny](163-default-deny-network.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 164 | [SCC / Least Privilege](164-scc-least-privilege.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 165 | [Secrets Externalization](165-secrets-externalization.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 166 | [Rolling Update](166-rolling-update.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 167 | [Blue/Green / Canary](167-bluegreen-canary.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 168 | [GitOps Reconciliation](168-gitops-reconciliation.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 169 | [Strangler Fig / Migration Java/JEE](169-strangler-fig.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |
| 170 | [Backup / DR / Fencing](170-disaster-recovery-fencing.md) | Kubernetes / OpenShift | Corrigé théorique ; quiz individuel à valider |

**Portée des QCM :** outils d'entraînement pédagogique, pas une certification ni une preuve de conformité ou de production. Les cours 13–50 ont été consolidés en supports à partir de la progression étudiée; les exercices du dépôt sont des exercices de consolidation et peuvent différer de leur formulation orale initiale. Les cours 59–62 ont été présentés ensemble : seule la question transversale Proxy a reçu une réponse en session (A, incorrecte, corrigée B). Les cours 63–73 sont publiés avec leurs exercices théoriquement corrigés, non validés individuellement en session. Les cours 74–83 sont désormais publiés de la même manière : théorie couverte et corrigés fournis, sans validation individuelle de leurs exercices.

## Exercices
- [Cahier des exercices 01–12](exercices-et-corriges/README.md)
- [Cahier de révision et corrections 13–58](exercices-et-corriges/cours-13-58.md)
- [Cahier de révision et corrections 59–62](exercices-et-corriges/cours-59-62.md)
- [Cahier de révision et corrections 63–73](exercices-et-corriges/cours-63-73.md)
- [Cahier de révision et corrections Java/JEE et Spring 74–83](exercices-et-corriges/cours-74-83.md)
- [Cahier Intégration 84–101](exercices-et-corriges/cours-84-101.md)
- [Cahier Données 102–113](exercices-et-corriges/cours-102-113.md)
- [Cahier Résilience 114–128](exercices-et-corriges/cours-114-128.md)
- [Cahier Sécurité et Zero Trust 129–140](exercices-et-corriges/cours-129-140.md)
- [Cahier 141–150 : Images, conteneurs et design des Pods](exercices-et-corriges/cours-141-150.md)
- [Cahier 151–160 : Controllers, workloads, résilience et capacité](exercices-et-corriges/cours-151-160.md)
- [Cahier 161–170 : Réseau, OpenShift, GitOps, migration et DR](exercices-et-corriges/cours-161-170.md)

## Ressources complémentaires
- [Architecture bancaire de référence](schemas/architecture-de-reference.md)
- [Cutover, reprise et incidents](schemas/cutover-et-incidents.md)
- [Étude bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
- [Migration Java/JEE vers OpenShift](../../09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/migration-playbook.md)
- [Patterns applicatifs détaillés](../../11-application-software-patterns/README.md)
- [GoF Java détaillés](../../19-java-design-patterns-gof/README.md)
- [Schéma de synthèse Java / Spring et cas bancaire](schemas/spring-paiement-74-83.md)
- [Architecture de synthèse Intégration 84–101](schemas/integration-84-101.md)
- [Architecture de synthèse Données 102–113](schemas/donnees-102-113.md)
- [Architecture de synthèse Résilience 114–128](schemas/resilience-114-128.md)
- [Architecture de synthèse Zero Trust 129–140](schemas/zero-trust-129-140.md)
- [Matrice exigences et preuves Zero Trust 129–140](schemas/matrice-preuves-zero-trust-129-140.md)
- [Architecture bancaire OpenShift 141–170](schemas/architecture-openshift-141-170.md)
- [Matrice des 30 tests Kubernetes / OpenShift](schemas/matrice-tests-openshift-141-170.md)

## Mode d'étude
1. Lire le besoin, les règles et l'exemple bancaire.
2. Reconstituer les frontières et la source autoritative.
3. Expliquer un cas nominal, un refus, un timeout et un doublon.
4. Répondre au QCM, lire le corrigé et justifier les alternatives.
5. Produire un livrable concret : schéma, contrat, ADR, tests ou trajectoire.

## Bilan et suite après le cours 170
Le programme compte **170 cours** : architecture métier/fonctionnelle/applicative, 23 GoF (51–73), Java/JEE Spring (74–83), Intégration (84–101), Données (102–113), Résilience (114–128), Sécurité Zero Trust (129–140), **30 cours Docker/Kubernetes/OpenShift (141–170)**.

Les cours 141–170 consolident les 30 patterns techniques déjà documentés dans la famille [09 Kubernetes/OpenShift](../../09-containerization-kubernetes-openshift-patterns/README.md). Les 30 nouvelles leçons ne changent pas le total des patterns du catalogue. Les corrigés sont théoriques, **pas des réponses individuelles validées ni des preuves runtime**.

Suite possible : architecture IA/agentique, cloud hybride, performance/SRE, modernisation, décision et Platform Engineering.

## Glossaire
- **AS-IS / TO-BE** : existant constaté / cible argumentée.
- **BPMN / RACI** : description des processus / matrice de responsabilités.
- **DAF** : dossier d'architecture fonctionnelle.
- **DDD / Bounded Context** : modélisation métier / frontière de vocabulaire et modèle.
- **Aggregate / Invariant** : frontière transactionnelle locale / règle devant toujours être vraie.
- **CQRS / Event Sourcing** : séparation commandes–lectures / reconstitution d'état par événements.
- **Ports & Adapters / DIP** : isolation des interfaces / orientation des dépendances vers les abstractions.
- **Idempotence** : répétition sans répétition de l'effet métier.
- **Source autoritative** : autorité responsable du fait concerné.
- **Outbox** : enregistrement atomique d'une intention de publication avec la transaction locale.

**Copyright © 2026 Zidane Djamal — matériel pédagogique original.** Marques et produits appartiennent à leurs titulaires.
