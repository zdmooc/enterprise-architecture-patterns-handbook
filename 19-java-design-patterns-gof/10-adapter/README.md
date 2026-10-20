# Adapter

## Problème

Réutiliser une interface de moteur de règles ou d'application legacy à travers un contrat moderne.

## Diagramme de structure

```mermaid
flowchart LR
 A["Contrat métier"] --> B["Adapter javax/JMS/REST"] --> C["Runtime legacy"]
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

- **Invariant :** Ne pas faire sortir un code erreur de l'éditeur comme décision métier sans traduction.
- **Test négatif :** Erreur legacy inconnue : résultat non confirmé, pas une approbation implicite.
- **Limite :** Adapter GoF est local; une ACL requiert aussi gouvernance sémantique et processus.
- Évaluer explicitement l'alternative simple, les coûts de maintenance, le comportement concurrent et les tests de contrat.

Ce pattern Java local ne dispense pas de politiques de sécurité ou de reprise d'un système distribué.

[Catalogue](../README.md)
