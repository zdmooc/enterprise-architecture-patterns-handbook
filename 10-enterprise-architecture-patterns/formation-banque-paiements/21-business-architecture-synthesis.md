# Cours 21 — Synthèse d'architecture métier

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 21.**

## Objectif et question d'architecte
Comment défendre une vue métier bout en bout ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Le comité bancaire demande une vision commune du virement SEPA de 500 EUR avant toute sélection technologique.

## 2. Notion et vocabulaire
La synthèse relie capacités, flux de valeur, domaines, acteurs, processus, informations, règles, états, événements, indicateurs et trajectoire.

## 3. Mise en pratique sur le paiement SEPA
Présenter une page de cadrage : besoin et objectifs; valeur pour le client; rôles; parcours et exceptions; référentiel d'information; mesures de succès; risques; décisions ouvertes. Produire les hypothèses et leur propriétaire.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Chaque capacité a une responsabilité; chaque état a un sens; chaque risque a une mitigation; aucun fournisseur n'est présenté comme une obligation métier.

**Piège à éviter :** Transformer la synthèse en catalogue de logiciels et omettre les décisions ou preuves.

## 5. Vérification et recette
Faire expliquer le même scénario à un représentant métier et un architecte; relever toute divergence de vocabulaire ou responsabilité.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Quelle synthèse convient au comité métier ?

- **A.** Une vue intégrée des responsabilités, parcours, règles, états, risques et résultats.
- **B.** Une liste de bibliothèques Java.
- **C.** Une maquette de base de données seule.

**Réponse attendue : A.** La synthèse relie capacités, flux de valeur, domaines, acteurs, processus, informations, règles, états, événements, indicateurs et trajectoire. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
