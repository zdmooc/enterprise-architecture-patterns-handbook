# Cours 43 — CQRS : séparation lecture et écriture

> Formation d'architecture applicative · Banque fictive · Paiement SEPA 500 EUR.

## Compétence visée
Expliquer le problème résolu, le mécanisme, la frontière de responsabilité et le coût du pattern.

## 1. Définition
Séparer le modèle de commandes (décisions et modifications) des modèles de consultation lorsque les besoins divergent.

## 2. Cas d'étude métier
Le moteur accepte ou rejette un ordre SEPA de 500 EUR. Le client consulte l'historique via un modèle de lecture optimisé sans pouvoir modifier les décisions.

## 3. Conception détaillée
Définir l'autorité d'écriture du paiement. Les événements ou projections alimentent la vue de consultation; préciser version, fraîcheur, retard et rapprochement. Les statuts affichés ne doivent pas surinterpréter une copie ancienne.

### Parcours à modéliser
1. Identifier le fait métier et la source autoritative.
2. Décrire les contrats d'entrée et de sortie et leur version.
3. Tracer le résultat nominal et sa signification exacte.
4. Prévoir refus, timeout, traitement concurrent, duplicata et reprise.
5. Vérifier que l'utilisateur ne reçoit pas une affirmation financière sans preuve.

## 4. Décisions et compromis
CQRS n'impose ni microservices ni event sourcing. Les projections peuvent être en retard; le domaine critique doit consulter l'autorité à l'instant requis.

**Arbitrage :** comparer ce pattern à une implémentation locale et simple; documenter les bénéfices mesurables, les données possédées, le coût de migration, les risques et le chemin de retour.

## 5. Tests / preuves attendues
Tester retard de projection, double événement, reconstruction d'une vue et consultation pendant panne.

Les preuves associent identifiant de paiement stable, événement ou décision d'origine, statut produit et correspondance avec le scénario attendu.

## 6. Exercice corrigé
**Quelle décision est pertinente ?**

- A. Laisser la vue lecture modifier directement les écritures financières.
- B. Distinguer commandes autoritatives et projections de consultation.
- C. Imposer un broker Kafka même pour un simple monolithe.

**Bonne réponse : B.** Séparer le modèle de commandes (décisions et modifications) des modèles de consultation lorsque les besoins divergent.

## 7. Synthèse pour entretien
- **Problème :** Le moteur accepte ou rejette un ordre SEPA de 500 EUR. Le client consulte l'historique via un modèle de lecture optimisé sans pouvoir modifier les décisions.
- **Solution :** Définir l'autorité d'écriture du paiement. Les événements ou projections alimentent la vue de consultation; préciser version, fraîcheur, retard et rapprochement. Les statuts affichés ne doivent pas surinterpréter une copie ancienne.
- **Limite :** CQRS n'impose ni microservices ni event sourcing. Les projections peuvent être en retard; le domaine critique doit consulter l'autorité à l'instant requis.

[Retour au programme](README.md) · [Fiche du pattern](../../11-application-software-patterns/08-cqrs-read-write/README.md)
