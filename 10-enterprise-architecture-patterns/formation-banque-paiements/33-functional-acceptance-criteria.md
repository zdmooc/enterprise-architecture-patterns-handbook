# Cours 33 — Critères d'acceptation fonctionnelle

> Formation architecture bancaire · Banque fictive · Virement SEPA de 500 EUR.

## Objectif
Comprendre le pattern et le justifier sur une architecture bancaire réelle ou simulée, en séparant faits attestés et hypothèses.

## Principe
Un critère d'acceptation exprime un comportement observable, vérifiable et validé par le métier.

## Étude de cas
Pour le virement SEPA fictif de 500 EUR, l'écran doit afficher « réglé » seulement si une preuve de règlement existe. Si la confirmation manque, l'état doit rester non confirmé. En cas de plafond dépassé, le client reçoit le motif adéquat.

## Démarche détaillée
Définir scénario, données d'entrée, résultat attendu et preuve mesurable. Valider avec le métier avant développement.

### Étapes de revue
1. Identifier acteurs, fonctions et composants concernés.
2. Décrire entrées, sorties, contrats et sources autoritatives.
3. Attribuer chaque décision et chaque information à un responsable.
4. Préciser les cas nominaux, refus métier, délais, doublons et reprises.
5. Distinguer ordre reçu, accepté, transmis et règlement confirmé.

## Risques, compromis et limites
Le critère « l'écran est convivial » est imprécis; spécifier le parcours et le résultat concret.

Comparer systématiquement la solution à une approche plus simple, consigner les contraintes de disponibilité, coût, intégration, conformité et maintenabilité.

## Plan de tests et preuves
Tester refus de plafond, ordre simplement accepté, confirmation externe tardive, réponse externe perdue et restitution client.

**Livrable :** scénario et preuve d'exécution, contrat, résultat vérifiable, décision documentée et condition de repli.

## Exercice corrigé
**Quelle décision convient à ce cours ?**

- A. Vérifier seulement l'affichage.
- B. Tester les scénarios métier et les critères validés.
- C. Valider dès que le code compile.

**Bonne réponse : B.** Un critère d'acceptation exprime un comportement observable, vérifiable et validé par le métier.

## Pour aller plus loin
Vérifier les frontières transactionnelles, l'idempotence et la reprise. Une acceptation technique ne prouve jamais à elle seule le règlement bancaire.

[Retour à l'index](README.md)
