# Cours 18 — Business Events Architecture

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 18.**

## Objectif et question d'architecte
Quels faits métier méritent un événement distinct ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Pour le virement de 500 EUR, l'ordre est reçu, puis accepté au contrôle, puis éventuellement réglé.

## 2. Notion et vocabulaire
Un événement métier est un fait passé et nommé au passé : OrdreReçu, OrdreAccepté, OrdreRejeté, RèglementConfirmé. Il décrit un fait; une commande exprime une intention.

## 3. Mise en pratique sur le paiement SEPA
Préciser déclencheur, producteur, référence, horodatage, version et signification de chaque événement. Les consommateurs doivent savoir si un événement signifie décision interne, transmission ou confirmation externe.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Un événement publié correspond à un fait réellement constaté; les abonnés tolèrent les doublons; une publication ne doit pas anticiper la validation de l'état.

**Piège à éviter :** Nommer « PaiementEffectué » un simple OrdreReçu, ou faire dépendre la transaction métier d'une notification non essentielle.

## 5. Vérification et recette
Rejouer deux fois OrdreAccepté sans double effet financier; vérifier l'absence d'un RèglementConfirmé tant que la preuve n'existe pas.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Quel événement indique un fait constaté ?

- **A.** « OrdreAccepté » après validation effective.
- **B.** « RéglerPaiement » avant exécution.
- **C.** « PaiementRéglé » dès réception HTTP.

**Réponse attendue : A.** Un événement métier est un fait passé et nommé au passé : OrdreReçu, OrdreAccepté, OrdreRejeté, RèglementConfirmé. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
