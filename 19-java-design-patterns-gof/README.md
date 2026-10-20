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
