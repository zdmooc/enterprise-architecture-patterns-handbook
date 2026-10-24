# Cours 46 — Dependency Inversion Principle

> Formation d'architecture applicative · Banque fictive · Paiement SEPA 500 EUR.

## Compétence visée
Expliquer le problème résolu, le mécanisme, la frontière de responsabilité et le coût du pattern.

## 1. Définition
Les composants de haut niveau ne doivent pas dépendre des détails de bas niveau; tous dépendent d'abstractions adaptées.

## 2. Cas d'étude métier
Le domaine de paiements calcule une décision à partir d'un plafond. Il ne doit pas connaître les classes JDBC utilisées pour charger ce plafond.

## 3. Conception détaillée
Définir une interface PlafondRepository dans la couche interne; l'infrastructure fournit JdbcPlafondRepository. Injecter la dépendance. Distinguer DIP de l'injection de dépendances : l'injection est un mécanisme, DIP une règle de conception.

### Parcours à modéliser
1. Identifier le fait métier et la source autoritative.
2. Décrire les contrats d'entrée et de sortie et leur version.
3. Tracer le résultat nominal et sa signification exacte.
4. Prévoir refus, timeout, traitement concurrent, duplicata et reprise.
5. Vérifier que l'utilisateur ne reçoit pas une affirmation financière sans preuve.

## 4. Décisions et compromis
Une interface qui reproduit directement toutes les méthodes d'un framework laisse persister le couplage. Trop d'interfaces sans variabilité ajoutent du bruit.

**Arbitrage :** comparer ce pattern à une implémentation locale et simple; documenter les bénéfices mesurables, les données possédées, le coût de migration, les risques et le chemin de retour.

## 5. Tests / preuves attendues
Compiler le domaine sans bibliothèques SQL; tester un repository mémoire; changer l'adaptateur réel; vérifier erreurs de lecture.

Les preuves associent identifiant de paiement stable, événement ou décision d'origine, statut produit et correspondance avec le scénario attendu.

## 6. Exercice corrigé
**Quelle décision est pertinente ?**

- A. Définir une abstraction métier interne et lui faire implémenter l'accès technique.
- B. Faire importer JDBC dans toutes les règles de plafond.
- C. Coupler le domaine au serveur HTTP.

**Bonne réponse : A.** Les composants de haut niveau ne doivent pas dépendre des détails de bas niveau; tous dépendent d'abstractions adaptées.

## 7. Synthèse pour entretien
- **Problème :** Le domaine de paiements calcule une décision à partir d'un plafond. Il ne doit pas connaître les classes JDBC utilisées pour charger ce plafond.
- **Solution :** Définir une interface PlafondRepository dans la couche interne; l'infrastructure fournit JdbcPlafondRepository. Injecter la dépendance. Distinguer DIP de l'injection de dépendances : l'injection est un mécanisme, DIP une règle de conception.
- **Limite :** Une interface qui reproduit directement toutes les méthodes d'un framework laisse persister le couplage. Trop d'interfaces sans variabilité ajoutent du bruit.

[Retour au programme](README.md) · [Fiche du pattern](../../11-application-software-patterns/11-dependency-inversion/README.md)
