# Cours 45 — API Contract First

> Formation d'architecture applicative · Banque fictive · Paiement SEPA 500 EUR.

## Compétence visée
Expliquer le problème résolu, le mécanisme, la frontière de responsabilité et le coût du pattern.

## 1. Définition
Spécifier le contrat et sa sémantique avant de coder producteurs et consommateurs.

## 2. Cas d'étude métier
L'application cliente soumet un virement de 500 EUR et reçoit une référence. Le contrat distingue réception de demande, acceptation de l'ordre et confirmation éventuelle du résultat.

## 3. Conception détaillée
Définir opération, schéma de requête, référence idempotente, statuts métiers, erreurs, authN/authZ, compatibilité de versions et délais. Examiner REST/OpenAPI comme support possible, sans réduire le contrat à l'URL.

### Parcours à modéliser
1. Identifier le fait métier et la source autoritative.
2. Décrire les contrats d'entrée et de sortie et leur version.
3. Tracer le résultat nominal et sa signification exacte.
4. Prévoir refus, timeout, traitement concurrent, duplicata et reprise.
5. Vérifier que l'utilisateur ne reçoit pas une affirmation financière sans preuve.

## 4. Décisions et compromis
Un code HTTP 200/202 ne prouve pas un règlement; les changements de champs obligatoires et de sens des statuts sont des ruptures de contrat.

**Arbitrage :** comparer ce pattern à une implémentation locale et simple; documenter les bénéfices mesurables, les données possédées, le coût de migration, les risques et le chemin de retour.

## 5. Tests / preuves attendues
Contract tests : champ inconnu, version ancienne, requête répétée, erreur autorisation, résultat en attente, réponse perdue.

Les preuves associent identifiant de paiement stable, événement ou décision d'origine, statut produit et correspondance avec le scénario attendu.

## 6. Exercice corrigé
**Quelle décision est pertinente ?**

- A. Écrire d'abord tout le code et nommer les champs après.
- B. Définir et valider un contrat stable, ses erreurs et sa sémantique avant implémentation.
- C. Utiliser toujours le même statut pour accepté et réglé.

**Bonne réponse : B.** Spécifier le contrat et sa sémantique avant de coder producteurs et consommateurs.

## 7. Synthèse pour entretien
- **Problème :** L'application cliente soumet un virement de 500 EUR et reçoit une référence. Le contrat distingue réception de demande, acceptation de l'ordre et confirmation éventuelle du résultat.
- **Solution :** Définir opération, schéma de requête, référence idempotente, statuts métiers, erreurs, authN/authZ, compatibilité de versions et délais. Examiner REST/OpenAPI comme support possible, sans réduire le contrat à l'URL.
- **Limite :** Un code HTTP 200/202 ne prouve pas un règlement; les changements de champs obligatoires et de sens des statuts sont des ruptures de contrat.

[Retour au programme](README.md) · [Fiche du pattern](../../11-application-software-patterns/10-api-contract-first/README.md)
