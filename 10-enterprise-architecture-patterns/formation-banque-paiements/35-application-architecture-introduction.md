# Cours 35 — Introduction à l'architecture applicative

> Formation architecture bancaire · Banque fictive · Virement SEPA de 500 EUR.

## Objectif
Comprendre le pattern et le justifier sur une architecture bancaire réelle ou simulée, en séparant faits attestés et hypothèses.

## Principe
L'architecture applicative traduit les fonctions en applications et composants, avec interfaces, dépendances et ownership.

## Étude de cas
Le moteur Java existant réalise plusieurs fonctions : contrôle, traitement et suivi de paiement. Une fonction ne correspond pas automatiquement à une application distincte.

## Démarche détaillée
Inventorier les composants, interactions, contrats, données et points de panne. Définir la cible et ses étapes sans imposer les microservices.

### Étapes de revue
1. Identifier acteurs, fonctions et composants concernés.
2. Décrire entrées, sorties, contrats et sources autoritatives.
3. Attribuer chaque décision et chaque information à un responsable.
4. Préciser les cas nominaux, refus métier, délais, doublons et reprises.
5. Distinguer ordre reçu, accepté, transmis et règlement confirmé.

## Risques, compromis et limites
Découper une classe Java par service ou choisir OpenShift avant de connaître les besoins augmente les risques.

Comparer systématiquement la solution à une approche plus simple, consigner les contraintes de disponibilité, coût, intégration, conformité et maintenabilité.

## Plan de tests et preuves
Tester les flux critiques, statuts ambigus, reprises, latence et une indisponibilité de composant.

**Livrable :** scénario et preuve d'exécution, contrat, résultat vérifiable, décision documentée et condition de repli.

## Exercice corrigé
**Quelle décision convient à ce cours ?**

- A. Découper immédiatement les fonctions en services.
- B. Étudier composants, fonctions et dépendances avant de choisir.
- C. Retirer l'ancien moteur sans analyse.

**Bonne réponse : B.** L'architecture applicative traduit les fonctions en applications et composants, avec interfaces, dépendances et ownership.

## Pour aller plus loin
Vérifier les frontières transactionnelles, l'idempotence et la reprise. Une acceptation technique ne prouve jamais à elle seule le règlement bancaire.

[Retour à l'index](README.md)
