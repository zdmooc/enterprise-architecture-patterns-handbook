# Cours 14 — Business Actors, Pools, Lanes et RACI

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 14.**

## Objectif et question d'architecte
Qui agit, décide et rend compte à chaque étape ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Le client déclenche le paiement; la banque donne suite à l'ordre; le mécanisme de compensation et la banque du bénéficiaire ont des responsabilités différentes.

## 2. Notion et vocabulaire
Dans BPMN, un pool est un participant autonome; une lane précise un rôle interne. RACI : Responsible exécute, Accountable répond du résultat, Consulted donne un avis, Informed est tenu informé.

## 3. Mise en pratique sur le paiement SEPA
Créer un pool Client et un pool Banque; dans le pool Banque, distinguer Front-office, Contrôle et Opérations. Définir un propriétaire métier responsable des règles d'acceptation et préciser les interfaces avec l'extérieur.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Une activité a un propriétaire explicite; le responsable final n'est pas confondu avec l'exécutant; le transfert à un tiers nécessite un échange modélisé.

**Piège à éviter :** Multiplier les rôles « A » pour une même décision, ou confondre une lane interne avec une banque externe.

## 5. Vérification et recette
Contrôler que chaque décision a une responsabilité, que le refus a un émetteur connu et qu'un acteur notifié ne devient pas automatiquement responsable.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Quelle modélisation clarifie les responsabilités ?

- **A.** Tous les acteurs dans une unique tâche anonyme.
- **B.** Pools pour les participants, lanes pour les rôles et RACI pour les responsabilités.
- **C.** Remplacer tous les rôles par le nom de l'application.

**Réponse attendue : B.** Dans BPMN, un pool est un participant autonome; une lane précise un rôle interne. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
