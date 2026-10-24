# Cours 16 — Business Information Model

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 16.**

## Objectif et question d'architecte
Quelles informations métier sont échangées et qui les possède ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Un virement SEPA de 500 EUR relie un donneur d'ordre, un bénéficiaire, un compte, un montant, une devise et une référence.

## 2. Notion et vocabulaire
Le modèle d'information métier formalise les concepts, attributs, relations et significations sans commencer par le schéma SQL. Chaque concept a une définition et une source autoritative.

## 3. Mise en pratique sur le paiement SEPA
Modèle minimal : Client donne Ordre; Ordre désigne Bénéficiaire; Ordre possède Montant, Devise, Référence et Statut; Compte porte ses propres données de tenue de compte. Définir unicité et durée de conservation des références.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Une référence stable identifie l'ordre; montant et devise forment une donnée métier cohérente; les informations sensibles sont minimisées.

**Piège à éviter :** Assimiler « accepté » à « réglé », dupliquer une source maîtresse sans contrôle de cohérence ou concevoir la table avant le sens métier.

## 5. Vérification et recette
Tester doublons de références, absence d'un bénéficiaire obligatoire, statut inconnu et différences entre date de demande et date de règlement.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Par quoi démarrer le modèle métier ?

- **A.** Par le choix des tables PostgreSQL.
- **B.** Par les concepts, leurs relations, définitions et propriétaires.
- **C.** Par le nombre de pods Kubernetes.

**Réponse attendue : B.** Le modèle d'information métier formalise les concepts, attributs, relations et significations sans commencer par le schéma SQL. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
