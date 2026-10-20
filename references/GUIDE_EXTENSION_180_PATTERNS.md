# Guide de sélection — Extension V4 de 151 à 180 patterns

Date : 20 octobre 2026. Les 151 fiches V3 restent intactes ; 29 nouvelles fiches sont regroupées en quatre familles. Le critère est le **problème métier**, non le framework.

| Situation observée | Première décision | Pattern | Test d'échec / condition GO |
|---|---|---|---|
| Publication perdue entre DB et broker | Conserver événement dans transaction SQL | [Outbox](../18-enterprise-integration-patterns/01-transactional-outbox/README.md) | Crash après COMMIT, reprise du relay |
| Redélivraisons et commandes dupliquées | Dédupliquer dans la transaction de l'effet | [Inbox](../18-enterprise-integration-patterns/02-transactional-inbox/README.md) | Deux consommateurs concurrents, un effet |
| Routage de messages sur critères vérifiables | Valider schéma et table explicite | [Router](../18-enterprise-integration-patterns/03-content-based-router/README.md) | Type inconnu rejeté |
| Différence moteur de règles entre deux versions | Comparer sans double décision métier | [Shadow Decision](../20-decision-management-patterns/04-shadow-decision-evaluation/README.md) | Zéro effet externe shadow |
| API métier couplée à l'éditeur | Contrat de domaine stable | [Rule Engine Adapter](../20-decision-management-patterns/02-rule-engine-adapter/README.md) | Bascule adapter sans changement contrat |
| Plusieurs tenants sur OpenShift | Protéger droits, réseaux et ressources | [Tenant Isolation](../21-platform-engineering-patterns/03-multi-tenant-isolation/README.md) | Accès croisé refusé |
| Trop de variations de runtime entre équipes | Fournir un chemin sûr par défaut | [Golden Path](../21-platform-engineering-patterns/02-golden-path/README.md) | Build non conforme rejeté |
| Application Java change d'algorithme | Injecter la politique métier | [Strategy](../19-java-design-patterns-gof/01-strategy/README.md) | Profiles strict et normal distincts |
| Une JVM réutilise des ressources coûteuses | Limiter pool/concurrence, éviter état global | [Singleton](../19-java-design-patterns-gof/11-singleton/README.md) | Deux réplicas ne partagent pas singleton |

## Processus de décision senior

1. Relever les capacités, l'invariant métier, les données autoritatives et les impacts inter-SI.
2. Énumérer l'alternative minimale et le coût de complexité du pattern.
3. Établir un contrat versionné, des seuils et une gouvernance ADR.
4. Mettre en place un test nominal, un test négatif, une injection de panne et une limite d'extrapolation.
5. Classer preuve : `REFERENCE`, `STATIC_VALIDATED`, `CI_RUNTIME_PROVEN`, `CRC_RUNTIME_PROVEN` ou `CLIENT_PRODUCTION` **uniquement si attestée**.

## Exemples transversaux

- [Java/JEE → OpenShift](../22-pattern-applications/01-javajee-progressive-modernization/README.md)
- [CRM Customer 360](../22-pattern-applications/02-customer360-integration/README.md)
- [Decision Platform](../22-pattern-applications/03-governed-decision-platform/README.md)

## Conventions

Aucune architecture interne de client ni donnée personnelle. Les patterns GoF sont intra-processus; les EIP traitent les échanges et effets distribués. Les schémas et tests de référence ne constituent pas de certification de support éditeur.
