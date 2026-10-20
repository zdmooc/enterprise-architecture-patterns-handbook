# Singleton — portée et dangers

## Problème

Un service veut partager une ressource coûteuse dans un seul processus.

## Diagramme de structure

```mermaid
flowchart LR
 A["Processus JVM"] --> B["Singleton thread-safe"] --> C["Pool de ressources"]
```

## Exemple d'appel

```mermaid
sequenceDiagram
 participant C as Client
 participant A as Abstraction
 participant I as Implémentation
 C->>A: opération + contexte
 A->>I: exécution contrôlée
 I-->>A: résultat ou échec
 A-->>C: statut attesté
```

## Invariant et preuve

- **Invariant :** Un singleton contrôle au plus un état par JVM, jamais une ressource unique entre réplicas Kubernetes.
- **Test négatif :** Tester concurrence, initialisation unique locale et comportement avec 2 processus séparés.
- **Limite :** Pour les pools JDBC utiliser gestion du conteneur et bornage global ; un singleton ne corrige pas une fuite de connexions.
- Évaluer explicitement l'alternative simple, les coûts de maintenance, le comportement concurrent et les tests de contrat.

Ce pattern Java local ne dispense pas de politiques de sécurité ou de reprise d'un système distribué.

[Catalogue](../README.md)
