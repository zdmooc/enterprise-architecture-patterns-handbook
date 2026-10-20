# Architecture décisionnelle : 5 patterns transversaux

Ce chapitre complète les patterns applicatifs GoF et les patterns IA sans revendiquer un moteur propriétaire ou une mise en production client.

| Pattern | Risque maîtrisé |
|---|---|
| [Decision Service Boundary](01-decision-service-boundary/README.md) | Plusieurs consommateurs invoquent des décisions sans contrat stable. |
| [Rule Engine Adapter](02-rule-engine-adapter/README.md) | Remplacer une implémentation de moteur sans modifier les cas d'usage métier. |
| [Rule Version Pinning / Promotion](03-rule-version-pinning/README.md) | Deux environnements exécutent des versions divergentes de règles et rendent l'audit ambigu. |
| [Shadow Decision Evaluation](04-shadow-decision-evaluation/README.md) | Une version candidate doit être évaluée sur les mêmes dossiers avant bascule. |
| [Decision Audit & Human Review](05-decision-audit-human-review/README.md) | Une décision sensible exige justification, provenance et éventuelle validation humaine. |

## Parcours architecte

**Besoin** → contrat stable → moteur interchangeable → version immuable → exécution shadow sans effet → journal et approbation. Les preuves distinguent code/tests, runtime générique, produit éditeur sous licence et exploitation client. Aucune approbation ML/IA ne remplace le point d'autorisation métier.
