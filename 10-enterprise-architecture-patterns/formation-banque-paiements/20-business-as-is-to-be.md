# Cours 20 — Business Architecture AS-IS et TO-BE

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 20.**

## Objectif et question d'architecte
Comment passer de l'existant à une cible démontrable ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Aujourd'hui, la banque saisit et suit les ordres dans plusieurs parcours dispersés; demain, elle souhaite clarifier les décisions et l'information client.

## 2. Notion et vocabulaire
AS-IS représente le fonctionnement observé avec preuves; TO-BE décrit les responsabilités et résultats visés. La trajectoire décrit les écarts, dépendances, coûts, risques et prérequis.

## 3. Mise en pratique sur le paiement SEPA
Cartographier qui réceptionne, contrôle et informe aujourd'hui; noter les contrôles manuels et les statuts ambigus. Pour la cible, définir source autoritative de l'état, règles harmonisées et information client explicite.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
La cible ne gomme pas les contraintes réglementaires; les anciennes et nouvelles voies peuvent coexister; le retour arrière doit préserver l'identité des ordres.

**Piège à éviter :** Dessiner le TO-BE sans connaître les flux réels, ou annoncer des gains sans indicateur de référence.

## 5. Vérification et recette
Comparer un cas nominal, un rejet et un état indéterminé sur les deux parcours; mesurer temps et taux d'erreur avant/après.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Quelle démarche prépare une transformation sûre ?

- **A.** Acheter une nouvelle technologie avant l'étude métier.
- **B.** Supprimer toutes les exceptions du modèle cible.
- **C.** Documenter AS-IS, écarts, TO-BE et trajectoire contrôlée.

**Réponse attendue : C.** AS-IS représente le fonctionnement observé avec preuves; TO-BE décrit les responsabilités et résultats visés. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
