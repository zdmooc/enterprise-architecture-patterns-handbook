# Matrice de décision — Architecture applicative

**Version corrigée :** chaque besoin renvoie au pattern portant réellement ce nom. Aucun résultat d'un POC n'est implicitement validé.

| Besoin réel | Pattern | Preuve à fournir |
|---|---|---|
| Séparer responsabilités dans une application simple | [layered architecture](01-layered-architecture/README.md) | Contrat, cas négatif, test de panne, ADR |
| Changer adaptateur sans changer le domaine | [hexagonal ports adapters](02-hexagonal-ports-adapters/README.md) | Contrat, cas négatif, test de panne, ADR |
| Protéger le métier des frameworks | [clean architecture](03-clean-architecture/README.md) | Contrat, cas négatif, test de panne, ADR |
| Isoler modules avec transactions locales | [modular monolith](04-modular-monolith/README.md) | Contrat, cas négatif, test de panne, ADR |
| Découper selon autonomie et charge prouvées | [microservices decomposition](05-microservices-decomposition/README.md) | Contrat, cas négatif, test de panne, ADR |
| Éviter l'ambiguïté des langages métier | [ddd bounded context](06-ddd-bounded-context/README.md) | Contrat, cas négatif, test de panne, ADR |
| Garantir invariants dans une transaction | [aggregate invariants](07-aggregate-invariants/README.md) | Contrat, cas négatif, test de panne, ADR |
| Adapter modèles de lecture très différents | [cqrs read write](08-cqrs-read-write/README.md) | Contrat, cas négatif, test de panne, ADR |
| Reconstituer un état depuis un journal fiable | [event sourcing](09-event-sourcing/README.md) | Contrat, cas négatif, test de panne, ADR |
| Versionner les contrats avant codage | [api contract first](10-api-contract-first/README.md) | Contrat, cas négatif, test de panne, ADR |
| Inverser les dépendances de modules | [dependency inversion](11-dependency-inversion/README.md) | Contrat, cas négatif, test de panne, ADR |
| Isoler la sémantique legacy | [anti corruption domain](12-anti-corruption-domain/README.md) | Contrat, cas négatif, test de panne, ADR |
| Distinguer besoins de chaque canal | [backend for frontend](13-backend-for-frontend/README.md) | Contrat, cas négatif, test de panne, ADR |
| Coordonner des modifications locales atomiques | [unit of work](14-unit-of-work/README.md) | Contrat, cas négatif, test de panne, ADR |
| Substituer une implémentation progressivement | [branch by abstraction](15-branch-by-abstraction/README.md) | Contrat, cas négatif, test de panne, ADR |

## Méthode

1. Définir contexte métier, propriétaire de données, NFR et contraintes de licences.
2. Comparer le minimum viable avec l'option utilisant ce pattern, risques et coûts inclus.
3. Tester nominal + anomalie + reprise ; expliciter ce qui n'est pas prouvé.
4. Formaliser décision, responsable, date de revue et conditions de retour arrière.

[Sommaire famille](README.md) · [Guide de sélection](../references/GUIDE_ARCHITECTE_151_PATTERNS.md)
