# Cours 22 — Introduction à l'architecture fonctionnelle

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 22.**

## Objectif et question d'architecte
Comment transformer le besoin métier en fonctions du SI ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Le processus métier « effectuer un virement » nécessite des fonctions de réception, contrôle, exécution et suivi.

## 2. Notion et vocabulaire
L'architecture métier explique pourquoi et par qui; l'architecture fonctionnelle décrit ce que le SI doit assurer, indépendamment du découpage applicatif.

## 3. Mise en pratique sur le paiement SEPA
Définir RéceptionnerOrdre, ContrôlerÉligibilité, ContrôlerPlafond, PiloterTraitement, ConsulterStatut, GérerRejet et RapprocherRésultat. À chaque fonction associer entrée, sortie, règle, propriétaire et exception.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Une fonction ne préjuge pas du nombre d'applications; la décision d'acceptation reste distincte de la preuve de règlement; une fonction a un contrat métier explicite.

**Piège à éviter :** Passer directement du besoin à un microservice par fonction ou confondre métier et application.

## 5. Vérification et recette
Tester traçabilité besoin → fonction; ordre de 500 EUR nominal; refus de plafond; statut non confirmé.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Que décrit la vue fonctionnelle ?

- **A.** Les serveurs et clusters OpenShift.
- **B.** Les fonctions attendues du SI et leurs échanges, sans imposer les logiciels.
- **C.** Un organigramme de l'entreprise.

**Réponse attendue : B.** L'architecture métier explique pourquoi et par qui; l'architecture fonctionnelle décrit ce que le SI doit assurer, indépendamment du découpage applicatif. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
