# Matrice de sélection et ADR — Architecture applicative et conception logicielle

## Choisir à partir d'une contrainte, pas d'un outil

| Question / contrainte | Pattern ou décision candidate | Preuve minimale |
|---|---|---|
| Modular monolith avant microservices non justifiés ? | [Layered architecture](01-layered-architecture/README.md) | Contrat, risque et test de scénario P0 |
| Contrats explicites et tests consumer-driven ? | [Hexagonal ports adapters](02-hexagonal-ports-adapters/README.md) | Contrat, risque et test de scénario P0 |
| CQRS seulement si lectures/écritures divergent fortement ? | [Clean architecture](03-clean-architecture/README.md) | Contrat, risque et test de scénario P0 |
| Cohérence limitée aux frontières transactionnelles ? | [Modular monolith](04-modular-monolith/README.md) | Contrat, risque et test de scénario P0 |

## Chemin d'arbitrage

~~~mermaid
flowchart TD
  A["Besoin réel et criticité"] --> B{"Invariants et NFR spécifiés ?"}
  B -->|Non| X["Cadrage, collecte de preuves"]
  B -->|Oui| C["Comparer les options et coûts"]
  C --> D{"Tests sécurité / pannes concluants ?"}
  D -->|Non| P["POC / remédiation / NO GO"]
  D -->|Oui| GO["ADR avec validation et runbook"]
~~~

## Grille de lecture

| Critère | Question à poser au comité |
|---|---|
| Métier | Quelle capacité et quel processus changent ? |
| Fonctionnel | Quels contrats et états sont impactés ? |
| Sécurité | Quelle identité et quelle frontière d'autorisation ? |
| Résilience | Que se passe-t-il entre commit et réponse perdue ? |
| Performance | p95/p99, pointe, goulots et capacité survivante mesurés ? |
| Données | Quel propriétaire et quel mode de réconciliation ? |
| Déploiement | Migration, rollback, compatibilité et propriétaires d'exploitation ? |
| Économie | Coûts/licences, alternatives et plan d'exit ? |

## À éviter

Un choix technique **ne** démontre **pas** automatiquement haute disponibilité, sécurité, conformité, cohérence financière ou portabilité. Les preuves attendues et les limites sont détaillées dans les fiches et le [cas d'étude](CASE_STUDY.md).
