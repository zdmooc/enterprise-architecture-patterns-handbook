# Cours 47 — Anti-Corruption Layer (ACL)

> Formation d'architecture applicative · Banque fictive · Paiement SEPA 500 EUR.

## Compétence visée
Expliquer le problème résolu, le mécanisme, la frontière de responsabilité et le coût du pattern.

## 1. Définition
Protéger le modèle cible du vocabulaire et des comportements d'un système historique.

## 2. Cas d'étude métier
Un moteur legacy Java/J2EE expose le statut TECH_OK après remise d'une demande au système historique, alors que notre modèle cible distingue Accepté et Réglé.

## 3. Conception détaillée
Placer une couche de traduction : normalisation des identifiants et formats, correspondance explicite des statuts, validation, politique d'erreur et traçabilité. TECH_OK devient par exemple Transmis si le contrat legacy le prouve, jamais Réglé sans preuve distincte.

### Parcours à modéliser
1. Identifier le fait métier et la source autoritative.
2. Décrire les contrats d'entrée et de sortie et leur version.
3. Tracer le résultat nominal et sa signification exacte.
4. Prévoir refus, timeout, traitement concurrent, duplicata et reprise.
5. Vérifier que l'utilisateur ne reçoit pas une affirmation financière sans preuve.

## 4. Décisions et compromis
L'ACL n'est pas un simple renommage de DTO. Elle exige des règles vérifiées et peut introduire latence et défauts de traduction.

**Arbitrage :** comparer ce pattern à une implémentation locale et simple; documenter les bénéfices mesurables, les données possédées, le coût de migration, les risques et le chemin de retour.

## 5. Tests / preuves attendues
Tester statut legacy inconnu, format ambigu, doublon, timeout et changement de contrat historique. Refuser une conversion non justifiable.

Les preuves associent identifiant de paiement stable, événement ou décision d'origine, statut produit et correspondance avec le scénario attendu.

## 6. Exercice corrigé
**Quelle décision est pertinente ?**

- A. Propager TECH_OK comme règlement bancaire.
- B. Traduire et valider la sémantique du legacy à la frontière du domaine cible.
- C. Imposer tous les termes legacy à la nouvelle application.

**Bonne réponse : B.** Protéger le modèle cible du vocabulaire et des comportements d'un système historique.

## 7. Synthèse pour entretien
- **Problème :** Un moteur legacy Java/J2EE expose le statut TECH_OK après remise d'une demande au système historique, alors que notre modèle cible distingue Accepté et Réglé.
- **Solution :** Placer une couche de traduction : normalisation des identifiants et formats, correspondance explicite des statuts, validation, politique d'erreur et traçabilité. TECH_OK devient par exemple Transmis si le contrat legacy le prouve, jamais Réglé sans preuve distincte.
- **Limite :** L'ACL n'est pas un simple renommage de DTO. Elle exige des règles vérifiées et peut introduire latence et défauts de traduction.

[Retour au programme](README.md) · [Fiche du pattern](../../11-application-software-patterns/12-anti-corruption-domain/README.md)
