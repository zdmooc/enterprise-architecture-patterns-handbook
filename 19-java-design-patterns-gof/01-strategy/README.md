# Strategy — GoF / Java 17

**Catégorie : design pattern logiciel, pas une architecture distribuée complète.**

## Problème

Choisir une politique de décision selon le contexte sans modifier le service d'appel.

## Structure

```mermaid
flowchart LR
 A["Policy.evaluate(Request)"] --> B["LimitPolicy / RiskPolicy"] --> C["DecisionService"]
```

## Contrat Java (simplifié)

```java
`interface Policy { Decision evaluate(Request r); }`
```

## Séquence

```mermaid
sequenceDiagram
 participant A as Appelant
 participant P as Abstraction
 participant I as Implémentation
 A->>P: opération métier
 P->>I: déléguer selon contrat
 I-->>P: résultat explicite
 P-->>A: décision + version
```

## Invariant et tests

**Invariant :** Changer politique par configuration versionnée plutôt que par if métiers dispersés.

1. Tester choix nominal et deux variantes de stratégie/produit/commande.
2. Tester absence de configuration et fail-closed : Sélection profil inconnu refusée ; aucun profil par défaut permissif.
3. Tester latence et erreurs : la classe appelante ne doit pas dépendre d'une implémentation spécifique.

## Compromis

Une stratégie modifie le résultat : journaliser règle/version et tests Golden Master. Ne pas introduire d'abstraction si une seule implémentation restera durablement suffisante.

[Catalogue GoF](../README.md) · [Lab JDK 17](../../labs/java-gof/README.md)
