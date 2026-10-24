# Cours 13 — Business Process Architecture et BPMN

> **Formation architecture bancaire** · Cas fictif : virement SEPA de 500 EUR. Ce support pédagogique ne décrit aucun SI réel. **Progression conversationnelle : cours 13.**

## Objectif et question d'architecte
Comment décrire un processus métier indépendamment du logiciel ?

**À savoir expliquer à l'oral :** le principe, les responsabilités, un cas nominal, un échec et une preuve de validation.

## 1. Situation métier
Pour un virement SEPA fictif de 500 EUR, le client saisit l'ordre, la banque contrôle sa recevabilité, puis transmet l'instruction et suit son résultat.

## 2. Notion et vocabulaire
BPMN distingue tâches, événements, passerelles et flux de séquence. Les couloirs représentent les responsabilités; un événement de fin « ordre transmis » ne prouve pas un règlement financier.

## 3. Mise en pratique sur le paiement SEPA
Décrire le départ (demande reçue), les tâches (identifier, vérifier plafond, contrôler bénéficiaire), une passerelle (valide ou refusé), les issues (rejet motivé ou ordre transmis), puis la réception d'une confirmation indépendante.

### Déroulement à restituer
1. Identifier le besoin, l'acteur et l'information d'entrée.
2. Nommer la décision et le propriétaire de la responsabilité.
3. Décrire le résultat métier sans confondre acceptation, émission, compensation et règlement.
4. Traiter le refus ou le résultat indéterminé, puis produire une preuve vérifiable.

## 4. Invariants et limites
Un rejet doit avoir une fin explicite; les exceptions ne disparaissent pas du diagramme; les échanges entre participants restent identifiables.

**Piège à éviter :** Confondre ordre accepté, transmis et réglé, ou représenter une décision métier comme un simple appel technique.

## 5. Vérification et recette
Le parcours de 500 EUR conforme atteint la transmission sans affirmation de règlement; un plafond dépassé aboutit à un rejet traçable; une confirmation absente laisse un état non confirmé.

**Livrable attendu :** une vue ou une règle lisible par le métier, les hypothèses, les scénarios nominatifs et les critères d'acceptation. Le dossier doit être traçable, versionné et cohérent avec la source autoritative.

## 6. Exercice de consolidation corrigé
**Question :** Quel modèle est correct ?

- **A.** Un seul rectangle « paiement réalisé ».
- **B.** Un schéma uniquement basé sur les serveurs.
- **C.** Un BPMN avec activités, décisions, participants et issues distinctes.

**Réponse attendue : C.** BPMN distingue tâches, événements, passerelles et flux de séquence. Les autres choix ignorent une responsabilité ou une garantie essentielle.

## 7. Repères pour l'architecte senior
- Distinguer besoin, règle, décision, résultat observé et résultat financier établi.
- Attribuer chaque décision à un propriétaire métier et chaque information à sa source autoritative.
- Documenter nominal, rejet, délai, doublon et reprise sans présumer d'un « exactly-once » bancaire.
- N'affirmer aucune durée, conformité ou technologie réellement utilisée par une banque sans preuve.

[Retour à l'index de formation](README.md) · [Cas bancaire transverse](../../07-case-studies/banking-payments-reference/README.md)
