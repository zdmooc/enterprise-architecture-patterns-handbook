# Formation — Architecture d'entreprise appliquée aux paiements bancaires

**Parcours 01 à 10 — 10 cours détaillés et exercices corrigés.**  
Référentiel : [famille des 12 patterns d'architecture d'entreprise](../README.md) | [Handbook (180 patterns)](../../README.md).

> **Pédagogie et anonymisation.** Cas fictif d'une banque traitant des virements SEPA et instantanés de 500 EUR ; aucun SI client, dessin confidentiel ni performance de production n'est reproduit. Les produits Java, IBM MQ, Kafka, PostgreSQL et OpenShift sont des exemples techniques, pas une déclaration de technologie chez un établissement. La conformité aux règles de paiement doit être examinée sur les textes applicables.

## Objectif du parcours
Savoir partir de la stratégie et des capacités métier, expliquer le parcours de valeur, attribuer des responsabilités, cartographier les applications et les flux, puis préparer une modernisation progressive avec une architecture cible argumentée, un plan de transition, une roadmap et un catalogue ABB/SBB.

## Index — cours détaillés
| N° | Leçon | Question de l'architecte | Fiche source | Validation pédagogique |
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

**Précision :** « validé » signifie ici qu'un QCM de formation a été corrigé dans la conversation pédagogique ; **ce n'est ni une certification ni une validation de production**.

## Ressources complémentaires
- [10 exercices et corrigés + étude transverse](exercices-et-corriges/README.md) — décisions, justifications, pièges et réponses attendues.
- [Schéma central des paiements et cartographie des flux](schemas/architecture-de-reference.md) — vues métier/applicative/technique.
- [Séquences de reprise, coexistence et cutover](schemas/cutover-et-incidents.md) — gestion d'incidents et invariants.
- [Étude bancaire transversale canonique du dépôt](../../07-case-studies/banking-payments-reference/README.md).
- [Playbook de migration Java/JEE vers OpenShift](../../09-containerization-kubernetes-openshift-patterns/09-case-study-java-jee-openshift/migration-playbook.md).

## Approche de lecture
1. Étudier l'objectif et le cas concret.
2. Reproduire le schéma de mémoire en nommant capacités, autorités, interfaces.
3. Expliquer les compromis au lieu de citer automatiquement une technologie.
4. Répondre à l'exercice sans regarder le corrigé, puis examiner les preuves attendues.
5. Compléter un livrable de mission : carte, matrice, ADR, risques ou plan de validation.

## Prochaines leçons dans l'ordre de la famille existante
- **11 — [Architecture Governance / ADR](../11-architecture-governance-adr/README.md)** : le cours conversationnel est entamé ; à finaliser puis documenter séparément.
- **12 — [Architecture Compliance / NFR](../12-architecture-compliance-nfr/README.md)** : prochaine leçon.
- **Extensions métier à développer** : BPMN/processus détaillé, RACI, règles métier, modèle d'information, états et événements bancaires. Ces sujets ne sont pas considérés comme couverts intégralement par les dix fiches ci-dessus.

## Glossaire minimum
- **ABB / SBB** : responsabilité d'architecture / réalisation technique.
- **AS-IS / TO-BE** : existant constaté / cible proposée.
- **ADR** : document de décision architecturale motivée.
- **Source autoritative** : système compétent pour attester l'état métier concerné.
- **Idempotence** : répétition du même ordre sans répétition de l'effet métier.
- **Outbox** : intention d'échange enregistrée durablement dans la transaction locale pour publication ultérieure.
- **GO / NO-GO** : autorisation ou refus motivé de franchir un jalon.
- **P0** : dépendance ou exigence bloquante selon la classification du programme.

**Copyright © 2026 Zidane Djamal — matériel original pédagogique.** Les noms de produits restent la propriété de leurs titulaires ; aucune licence des tiers n'est modifiée.
