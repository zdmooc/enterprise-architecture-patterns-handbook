# Cours 15 — Business Rules Architecture

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 15.**

## Objectif et question d'architecte
Comment isoler et gouverner les règles métier ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Un ordre de 500 EUR est soumis à un plafond journalier propre au client. La banque peut aussi appliquer des contrôles de conformité et d'éligibilité.

## 2. Notion et vocabulaire
Une règle métier a un identifiant, un propriétaire, une condition, une décision, une date d'effet et des exceptions. Le catalogue de règles reste distinct du détail d'implémentation.

## 3. Mise en pratique sur le paiement SEPA
Règle fictive BR-001 : si cumul journalier + nouvel ordre > plafond applicable, refuser au titre du plafond. BR-002 : si contrôle obligatoire non concluant, ne pas autoriser la progression vers l'étape suivante. Faire valider l'ordre de priorité.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Les règles applicables sont versionnées; une dérogation doit être autorisée et auditée; la décision conserve sa justification.

**Piège à éviter :** Cacher un plafond dans l'interface web, coder la règle à deux endroits divergents ou changer la règle sans date d'effet.

## 5. Vérification et recette
Tester 1 500 EUR sur plafond 2 000 EUR avec cumul zéro; 500 EUR après cumul 1 700 EUR; changement de plafond en cours de journée selon convention précisée.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Quel est le rôle du catalogue de règles ?

- **A.** Définir des décisions métier explicites, traçables et versionnées.
- **B.** Documenter uniquement les technologies.
- **C.** Garantir qu'aucune exception métier n'existe.

**Réponse attendue : A.** Une règle métier a un identifiant, un propriétaire, une condition, une décision, une date d'effet et des exceptions. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
