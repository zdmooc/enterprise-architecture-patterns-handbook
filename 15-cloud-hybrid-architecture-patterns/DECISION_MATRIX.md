# Matrice de sélection et ADR — Architecture cloud hybride et multienvironnement

## Choisir à partir d'une contrainte, pas d'un outil

| Question / contrainte | Pattern ou décision candidate | Preuve minimale |
|---|---|---|
| Landing zone minimum avant workload ? | [Landing zone](01-landing-zone/README.md) | Contrat, risque et test de scénario P0 |
| Residency et IAM avant placement ? | [Hub spoke](02-hub-spoke/README.md) | Contrat, risque et test de scénario P0 |
| Lien privé avec plan de dégradation ? | [Transit connectivity](03-transit-connectivity/README.md) | Contrat, risque et test de scénario P0 |
| Portabilité testée selon exigences réelles ? | [Private connectivity](04-private-connectivity/README.md) | Contrat, risque et test de scénario P0 |

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
