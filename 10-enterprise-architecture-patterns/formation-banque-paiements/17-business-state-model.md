# Cours 17 — Business State Model

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 17.**

## Objectif et question d'architecte
Quels états métier un paiement peut-il traverser ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Le client saisit un ordre SEPA de 500 EUR. Son chemin métier ne se résume pas à un indicateur booléen « succès ».

## 2. Notion et vocabulaire
Un modèle d'états définit états, transitions autorisées, événements déclencheurs et responsabilités. Les états doivent être sémantiquement vérifiables.

## 3. Mise en pratique sur le paiement SEPA
Chaîne illustrative : Reçu → En contrôle → Accepté → Transmis → Résultat confirmé. Branches possibles : Rejeté lors des contrôles; À investiguer si le résultat externe est indéterminé. « Résultat confirmé » doit préciser sa nature.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Toute transition a un événement probant; une confirmation technique de réception ne vaut pas règlement; une transition terminale ne se renverse pas arbitrairement.

**Piège à éviter :** Inventer un statut « payé » sur simple HTTP 200 ou ignorer les transitions lors des reprises après panne.

## 5. Vérification et recette
Tester transitions nominales, rejet, réponse perdue, événement dupliqué, événement hors ordre et état inconnu.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Quel suivi est fiable ?

- **A.** Un unique état « succès » dès la saisie.
- **B.** Des transitions libres sans événement.
- **C.** Des états et transitions explicites reliés à des preuves métier.

**Réponse attendue : C.** Un modèle d'états définit états, transitions autorisées, événements déclencheurs et responsabilités. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
