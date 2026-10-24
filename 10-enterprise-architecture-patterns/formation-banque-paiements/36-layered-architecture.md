# Cours 36 — Layered Architecture

> Formation architecture bancaire · Banque fictive · Virement SEPA de 500 EUR.

## Objectif
Comprendre le pattern et le justifier sur une architecture bancaire réelle ou simulée, en séparant faits attestés et hypothèses.

## Principe
Une application en couches sépare présentation, orchestration applicative, domaine métier et infrastructure.

## Étude de cas
L'écran reçoit l'ordre SEPA de 500 EUR. Le service applicatif organise le traitement. Le domaine applique les règles de plafond. L'infrastructure fournit stockage et communications.

## Démarche détaillée
Définir les dépendances permises, placer les règles stables dans le domaine et maintenir la couche d'infrastructure remplaçable. Les couches peuvent être dans un même déploiement.

### Étapes de revue
1. Identifier acteurs, fonctions et composants concernés.
2. Décrire entrées, sorties, contrats et sources autoritatives.
3. Attribuer chaque décision et chaque information à un responsable.
4. Préciser les cas nominaux, refus métier, délais, doublons et reprises.
5. Distinguer ordre reçu, accepté, transmis et règlement confirmé.

## Risques, compromis et limites
Une séparation de packages sans contrôle des dépendances ne suffit pas; éviter des couches créées artificiellement.

Comparer systématiquement la solution à une approche plus simple, consigner les contraintes de disponibilité, coût, intégration, conformité et maintenabilité.

## Plan de tests et preuves
Tester les règles métier sans serveur HTTP ni vraie base; tester remplacement d'une implémentation de stockage.

**Livrable :** scénario et preuve d'exécution, contrat, résultat vérifiable, décision documentée et condition de repli.

## Exercice corrigé
**Quelle décision convient à ce cours ?**

- A. Mélanger présentation et métier.
- B. Réécrire les règles à chaque migration.
- C. Isoler les règles métier des détails techniques.

**Bonne réponse : C.** Une application en couches sépare présentation, orchestration applicative, domaine métier et infrastructure.

## Pour aller plus loin
Vérifier les frontières transactionnelles, l'idempotence et la reprise. Une acceptation technique ne prouve jamais à elle seule le règlement bancaire.

[Retour à l'index](README.md)
