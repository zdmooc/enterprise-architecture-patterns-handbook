# Cahier de révision — cours 13 à 54

> Banque fictive. QCM de consolidation, distincts le cas échéant des formulations orales. Lire le cours avant le corrigé. Les réponses ne constituent ni certification ni preuve de conformité.

## Métier — cours 13 à 21

### 13. Business Process Architecture et BPMN
**Cours :** [Ouvrir la leçon](../13-business-process-bpmn.md).

**Réponse : C.** Un BPMN identifie activités, décisions et issues sans confondre transmission et règlement.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 14. Business Actors, Pools, Lanes et RACI
**Cours :** [Ouvrir la leçon](../14-actors-pools-lanes-raci.md).

**Réponse : B.** Pools, lanes et RACI distinguent participants, rôles et responsabilités.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 15. Business Rules Architecture
**Cours :** [Ouvrir la leçon](../15-business-rules.md).

**Réponse : A.** Des règles traçables et versionnées rendent les décisions reproductibles.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 16. Business Information Model
**Cours :** [Ouvrir la leçon](../16-business-information-model.md).

**Réponse : B.** Le sens métier précède le schéma physique des données.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 17. Business State Model
**Cours :** [Ouvrir la leçon](../17-business-state-model.md).

**Réponse : C.** Chaque état et transition doit correspondre à un fait prouvé.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 18. Business Events Architecture
**Cours :** [Ouvrir la leçon](../18-business-events.md).

**Réponse : A.** Un événement indique un fait constaté, non une intention.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 19. Business KPI, SLA et SLO
**Cours :** [Ouvrir la leçon](../19-business-kpi-sla.md).

**Réponse : B.** Une mesure utile a un périmètre et une source de preuve.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 20. Business Architecture AS-IS et TO-BE
**Cours :** [Ouvrir la leçon](../20-business-as-is-to-be.md).

**Réponse : C.** La cible exige un diagnostic AS-IS et une trajectoire contrôlée.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 21. Synthèse d'architecture métier
**Cours :** [Ouvrir la leçon](../21-business-architecture-synthesis.md).

**Réponse : A.** La vue métier rassemble les décisions, règles et capacités.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

## Fonctionnelle — cours 22 à 34

### 22. Introduction à l'architecture fonctionnelle
**Cours :** [Ouvrir la leçon](../22-functional-architecture-introduction.md).

**Réponse : B.** La vue fonctionnelle explique ce que le SI assure, pas quels logiciels il utilise.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 23. Décomposition fonctionnelle
**Cours :** [Ouvrir la leçon](../23-functional-decomposition.md).

**Réponse : B.** La décomposition suit les responsabilités métier.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 24. Flux fonctionnels
**Cours :** [Ouvrir la leçon](../24-functional-flows.md).

**Réponse : C.** Un flux exprime un échange sémantique entre fonctions.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 25. Contrats fonctionnels
**Cours :** [Ouvrir la leçon](../25-functional-contracts.md).

**Réponse : A.** Le contrat précise les résultats et exceptions.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 26. Gestion fonctionnelle des exceptions
**Cours :** [Ouvrir la leçon](../26-functional-exceptions.md).

**Réponse : B.** Un timeout n'est pas un refus métier.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 27. Orchestration fonctionnelle
**Cours :** [Ouvrir la leçon](../27-functional-orchestration.md).

**Réponse : C.** Un orchestrateur coordonne les étapes et reprises.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 28. Orchestration et chorégraphie
**Cours :** [Ouvrir la leçon](../28-orchestration-vs-choreography.md).

**Réponse : A.** Un pilote central se distingue des réactions par événements.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 29. Responsabilités et source autoritative
**Cours :** [Ouvrir la leçon](../29-functional-responsibility-authoritative-source.md).

**Réponse : B.** La source faisant foi dépend du fait métier concerné.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 30. Traçabilité fonctionnelle
**Cours :** [Ouvrir la leçon](../30-functional-traceability.md).

**Réponse : C.** Tout besoin prioritaire doit être couvert et testé.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 31. Analyse d'impact fonctionnelle
**Cours :** [Ouvrir la leçon](../31-functional-impact-analysis.md).

**Réponse : B.** Une règle changée impacte des fonctions et leurs contrats.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 32. Tests de non-régression fonctionnelle
**Cours :** [Ouvrir la leçon](../32-functional-non-regression.md).

**Réponse : C.** Tester le nouveau et les comportements existants.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 33. Critères d'acceptation fonctionnelle
**Cours :** [Ouvrir la leçon](../33-functional-acceptance-criteria.md).

**Réponse : B.** Les critères métier sont vérifiables et validés.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 34. Dossier d'architecture fonctionnelle
**Cours :** [Ouvrir la leçon](../34-functional-architecture-dossier.md).

**Réponse : C.** Le DAF assemble fonctions, flux, règles et preuves.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

## Applicative — cours 35 à 50

### 35. Introduction à l'architecture applicative
**Cours :** [Ouvrir la leçon](../35-application-architecture-introduction.md).

**Réponse : B.** La cible applicative suit l'analyse de l'existant.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 36. Layered Architecture
**Cours :** [Ouvrir la leçon](../36-layered-architecture.md).

**Réponse : C.** Séparer domaine et infrastructure préserve les règles.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 37. Architecture hexagonale : Ports & Adapters
**Cours :** [Ouvrir la leçon](../37-hexagonal-ports-adapters.md).

**Réponse : B.** Les ports permettent la substitution d'adaptateurs.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 38. Clean Architecture
**Cours :** [Ouvrir la leçon](../38-clean-architecture.md).

**Réponse : B.** Les dépendances logicielles pointent vers le métier.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 39. Modular Monolith
**Cours :** [Ouvrir la leçon](../39-modular-monolith.md).

**Réponse : C.** Un déploiement unique peut contenir des modules isolés.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 40. Microservices Decomposition
**Cours :** [Ouvrir la leçon](../40-microservices-decomposition.md).

**Réponse : B.** L'extraction progressive répond à un vrai besoin d'autonomie.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 41. DDD : Bounded Context
**Cours :** [Ouvrir la leçon](../41-ddd-bounded-context.md).

**Réponse : B.** Chaque contexte possède son modèle et son vocabulaire.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 42. DDD : Aggregate et invariants
**Cours :** [Ouvrir la leçon](../42-aggregate-invariants.md).

**Réponse : C.** L'agrégat valide les mutations et ses invariants.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 43. CQRS
**Cours :** [Ouvrir la leçon](../43-cqrs-read-write.md).

**Réponse : B.** Le modèle d'écriture autoritatif reste distinct des projections de lecture.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 44. Event Sourcing
**Cours :** [Ouvrir la leçon](../44-event-sourcing.md).

**Réponse : C.** L'état se reconstruit à partir d'événements métier immuables et versionnés.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 45. API Contract First
**Cours :** [Ouvrir la leçon](../45-api-contract-first.md).

**Réponse : B.** Un contrat précise schéma, erreurs, versions et signification.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 46. Dependency Inversion
**Cours :** [Ouvrir la leçon](../46-dependency-inversion.md).

**Réponse : A.** Les abstractions du métier ne dépendent pas de JDBC.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 47. Anti-Corruption Layer
**Cours :** [Ouvrir la leçon](../47-anti-corruption-layer.md).

**Réponse : B.** La traduction protège le modèle cible de l'ancien SI.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 48. Backend for Frontend
**Cours :** [Ouvrir la leçon](../48-backend-for-frontend.md).

**Réponse : B.** Le BFF adapte l'expérience au canal sans prendre les décisions financières.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 49. Unit of Work
**Cours :** [Ouvrir la leçon](../49-unit-of-work.md).

**Réponse : C.** La transaction locale couvre les mutations qui doivent rester cohérentes.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 50. Branch by Abstraction
**Cours :** [Ouvrir la leçon](../50-branch-by-abstraction.md).

**Réponse : B.** Une abstraction permet la coexistence et la bascule contrôlée.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

## Java et GoF — cours 51 à 52

### 51. Factory Method (Java GoF)
**Cours :** [Ouvrir la leçon](../51-factory-method.md).

**Réponse : B.** La méthode de création est spécialisée par polymorphisme.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 52. Abstract Factory (Java GoF)
**Cours :** [Ouvrir la leçon](../52-abstract-factory.md).

**Réponse : C.** La fabrique crée une famille de produits compatibles.

**Preuve demandée :** décrire un scénario nominal, un échec, une règle/invariant et le test qui prouve le comportement.

### 53. Builder (GoF Java)
**Cours :** [Ouvrir la leçon](../53-builder.md).

**Réponse : C.** Builder assemble un ordre progressivement et vérifie les contraintes de construction, sans remplacer le contrôle métier.

**Preuve demandée :** construire un ordre de 500 EUR, refuser un montant absent et vérifier l'immuabilité.

### 54. Prototype (GoF Java)
**Cours :** [Ouvrir la leçon](../54-prototype.md).

**Réponse : A.** Reprendre les données d'un modèle en créant une nouvelle référence et un nouvel état non exécuté.

**Preuve demandée :** isoler les champs mutables, vérifier la nouvelle référence et refaire les contrôles métier.

## Cas transverse de synthèse
Le client initie un virement SEPA fictif de 500 EUR. Présenter le processus BPMN, les fonctions, contrats, règles et états; choisir modules applicatifs, limites DDD et composants; décrire le changement technologique, la reprise après réponse perdue et l'absence de double effet métier. Séparer explicitement ordre accepté et règlement confirmé.

[Retour à la formation](../README.md).
