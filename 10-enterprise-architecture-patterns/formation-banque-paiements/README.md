# Formation complète — 57 cours d'architecture appliqués aux paiements bancaires

**57 cours publiés avec exemple bancaire, décisions, risques, tests et exercice corrigé.** Parcours progressif : métier → fonctionnel → applicatif → design patterns Java.

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

## Index — cours 13 à 57
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

**Portée des QCM :** outils d'entraînement pédagogique, pas une certification ni une preuve de conformité ou de production. Les cours 13–50 ont été consolidés en supports à partir de la progression étudiée; les exercices du dépôt sont des exercices de consolidation et peuvent différer de leur formulation orale initiale.

## Exercices
- [Cahier des exercices 01–12](exercices-et-corriges/README.md)
- [Cahier de révision et corrections 13–57](exercices-et-corriges/cours-13-57.md)

## Ressources complémentaires
- [Architecture bancaire de référence](schemas/architecture-de-reference.md)
- [Cutover, reprise et incidents](schemas/cutover-et-incidents.md)
- [Étude bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
- [Migration Java/JEE vers OpenShift](../../09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/migration-playbook.md)
- [Patterns applicatifs détaillés](../../11-application-software-patterns/README.md)
- [GoF Java détaillés](../../19-java-design-patterns-gof/README.md)

## Mode d'étude
1. Lire le besoin, les règles et l'exemple bancaire.
2. Reconstituer les frontières et la source autoritative.
3. Expliquer un cas nominal, un refus, un timeout et un doublon.
4. Répondre au QCM, lire le corrigé et justifier les alternatives.
5. Produire un livrable concret : schéma, contrat, ADR, tests ou trajectoire.

## Suite prévue après le cours 57
Cours 58–73 : autres patterns GoF Java, puis patterns Java/JEE et Spring, intégration, données, sécurité, résilience, OpenShift et IA selon le programme pédagogique. **Les cours 58 et suivants ne sont pas encore publiés dans ce dossier.**

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
