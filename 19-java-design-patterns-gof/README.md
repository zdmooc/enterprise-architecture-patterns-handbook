# Java/JEE — 11 design patterns GoF utiles à l'architecte

Les patterns GoF concernent la conception **dans un processus** : ne pas les confondre avec Saga, Outbox, Kafka, GitOps ou la résilience multi-réplicas.

| Design pattern | Situation utile |
|---|---|
| [Strategy — sélection de politique](01-strategy/README.md) | Exemple, invariant, test négatif |
| [Factory Method — création d'implémentation](02-factory-method/README.md) | Exemple, invariant, test négatif |
| [Abstract Factory — familles compatibles](03-abstract-factory/README.md) | Exemple, invariant, test négatif |
| [Command — intention encapsulée](04-command/README.md) | Exemple, invariant, test négatif |
| [Decorator — enrichissement transparent](05-decorator/README.md) | Exemple, invariant, test négatif |
| [Proxy — autorisation locale](06-proxy/README.md) | Exemple, invariant, test négatif |
| [Template Method — enchaînement contrôlé](07-template-method/README.md) | Exemple, invariant, test négatif |
| [Observer — notifications in-process](08-observer/README.md) | Exemple, invariant, test négatif |
| [State — transitions explicites](09-state/README.md) | Exemple, invariant, test négatif |
| [Adapter — contrats legacy](10-adapter/README.md) | Exemple, invariant, test négatif |
| [Singleton — unicité par JVM seulement](11-singleton/README.md) | Exemple, invariant, test négatif |

## Formation / tests

Un [laboratoire JDK 17](../labs/java-gof/README.md) compile Strategy, Factory, Command, Decorator, Proxy, Template Method et Observer sans dépendance éditeur. Les autres fiches contiennent des exercices conceptuels; ils ne sont pas présentés comme exécutés.

## Parcours complet des 23 patterns GoF — cours 51 à 73

Le **catalogue ci-dessus contient 11 fiches de référence déjà présentes dans les 180 patterns du handbook** ; il ne faut pas confondre ce sous-ensemble avec le parcours pédagogique, qui couvre désormais les **23 GoF classiques** en 23 leçons numérotées, sans changer le total de 180 fiches du catalogue.

- [Index de la formation bancaire, cours 51–73](../10-enterprise-architecture-patterns/formation-banque-paiements/README.md).
- [Les onze cours comportementaux 63–73 et exercices corrigés](../10-enterprise-architecture-patterns/formation-banque-paiements/exercices-et-corriges/cours-63-73.md).

