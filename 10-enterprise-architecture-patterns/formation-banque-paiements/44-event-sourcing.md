# Cours 44 — Event Sourcing

> Formation d'architecture applicative · Banque fictive · Paiement SEPA 500 EUR.

## Compétence visée
Expliquer le problème résolu, le mécanisme, la frontière de responsabilité et le coût du pattern.

## 1. Définition
Enregistrer les changements métier comme une suite immuable d'événements permettant de reconstruire un état.

## 2. Cas d'étude métier
L'ordre SEPA fictif reçoit successivement OrdreReçu, OrdreAccepté puis OrdreTransmis. Une confirmation financière externe est un fait séparé et ne doit pas être déduite d'OrdreTransmis.

## 3. Conception détaillée
Définir événements versionnés, identifiant d'agrégat, ordre causal, schémas, snapshots éventuels et politique de rétention. Rejouer un flux produit l'état selon les règles de version connues.

### Parcours à modéliser
1. Identifier le fait métier et la source autoritative.
2. Décrire les contrats d'entrée et de sortie et leur version.
3. Tracer le résultat nominal et sa signification exacte.
4. Prévoir refus, timeout, traitement concurrent, duplicata et reprise.
5. Vérifier que l'utilisateur ne reçoit pas une affirmation financière sans preuve.

## 4. Décisions et compromis
Event Sourcing ne remplace pas la comptabilité, n'offre pas seul exactement-une-fois et augmente la complexité de migration d'événements. Éviter si une simple journalisation auditée suffit.

**Arbitrage :** comparer ce pattern à une implémentation locale et simple; documenter les bénéfices mesurables, les données possédées, le coût de migration, les risques et le chemin de retour.

## 5. Tests / preuves attendues
Rejeu déterministe; événement dupliqué; migration de schéma; message manquant; contrôle de confidentialité et conservation.

Les preuves associent identifiant de paiement stable, événement ou décision d'origine, statut produit et correspondance avec le scénario attendu.

## 6. Exercice corrigé
**Quelle décision est pertinente ?**

- A. Écraser l'historique à chaque mise à jour.
- B. Considérer chaque message réseau comme événement financier final.
- C. Conserver les événements métier immuables et reconstruire l'état avec leurs versions.

**Bonne réponse : C.** Enregistrer les changements métier comme une suite immuable d'événements permettant de reconstruire un état.

## 7. Synthèse pour entretien
- **Problème :** L'ordre SEPA fictif reçoit successivement OrdreReçu, OrdreAccepté puis OrdreTransmis. Une confirmation financière externe est un fait séparé et ne doit pas être déduite d'OrdreTransmis.
- **Solution :** Définir événements versionnés, identifiant d'agrégat, ordre causal, schémas, snapshots éventuels et politique de rétention. Rejouer un flux produit l'état selon les règles de version connues.
- **Limite :** Event Sourcing ne remplace pas la comptabilité, n'offre pas seul exactement-une-fois et augmente la complexité de migration d'événements. Éviter si une simple journalisation auditée suffit.

[Retour au programme](README.md) · [Fiche du pattern](../../11-application-software-patterns/09-event-sourcing/README.md)
