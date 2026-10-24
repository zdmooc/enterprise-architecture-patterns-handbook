# Cours 19 — Business KPI, SLA et SLO

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 19.**

## Objectif et question d'architecte
Comment mesurer une qualité de service utile au métier ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
La banque veut réduire les retards de suivi et mieux expliquer les rejets des virements SEPA.

## 2. Notion et vocabulaire
Un KPI mesure une performance métier; un SLI est un indicateur de service observé; un SLO est une cible interne; un SLA est un engagement formel selon son périmètre et ses clauses.

## 3. Mise en pratique sur le paiement SEPA
Définir taux de rejet par motif, proportion d'ordres au résultat inconnu, délai entre acceptation et information client, et disponibilité du parcours. Préciser population, fenêtre de mesure, exclusions et source de preuve.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Chaque mesure a un dénominateur, une fenêtre et un propriétaire; un délai « accepté → réglé » n'est pas confondu avec latence d'API; aucune cible de production n'est inventée.

**Piège à éviter :** Afficher « 100 % disponible » sans périmètre ni méthode; utiliser uniquement le temps de réponse réseau pour juger le règlement.

## 5. Vérification et recette
Simuler refus métier normal (qui n'est pas une panne), indisponibilité de notification, retard externe, et vérifier le classement des indicateurs.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Qu'est-ce qu'un KPI exploitable ?

- **A.** Un nombre sans définition ni période.
- **B.** Une mesure définie avec périmètre, source, période et interprétation.
- **C.** Un objectif de latence arbitraire.

**Réponse attendue : B.** Un KPI mesure une performance métier; un SLI est un indicateur de service observé; un SLO est une cible interne; un SLA est un engagement formel selon son périmètre et ses clauses. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
