# Cours 34 — Dossier d'architecture fonctionnelle (DAF)

> Formation architecture bancaire · Banque fictive · Virement SEPA de 500 EUR.

## Objectif
Comprendre le pattern et le justifier sur une architecture bancaire réelle ou simulée, en séparant faits attestés et hypothèses.

## Principe
Le DAF relie les besoins aux fonctions, flux, règles, responsabilités, informations et critères d'acceptation.

## Étude de cas
Le directeur des paiements demande une vision d'ensemble : réception des virements, contrôles, traitement, suivi, rapprochement et gestion des anomalies.

## Démarche détaillée
Structurer le dossier : contexte, périmètre, cartographie fonctionnelle, flux et contrats, sources faisant foi, règles et états, exceptions, traçabilité, décisions et recette.

### Étapes de revue
1. Identifier acteurs, fonctions et composants concernés.
2. Décrire entrées, sorties, contrats et sources autoritatives.
3. Attribuer chaque décision et chaque information à un responsable.
4. Préciser les cas nominaux, refus métier, délais, doublons et reprises.
5. Distinguer ordre reçu, accepté, transmis et règlement confirmé.

## Risques, compromis et limites
Un dossier uniquement technique ne remplace pas un DAF; il faut séparer ce que le SI fait de la façon dont les logiciels le font.

Comparer systématiquement la solution à une approche plus simple, consigner les contraintes de disponibilité, coût, intégration, conformité et maintenabilité.

## Plan de tests et preuves
Faire relire par métiers et SI. Vérifier chaque besoin et chaque exception contre une fonction et une preuve.

**Livrable :** scénario et preuve d'exécution, contrat, résultat vérifiable, décision documentée et condition de repli.

## Exercice corrigé
**Quelle décision convient à ce cours ?**

- A. Fournir les serveurs.
- B. Fournir seulement les noms d'applications.
- C. Fournir les fonctions, règles, flux, exceptions et vérifications.

**Bonne réponse : C.** Le DAF relie les besoins aux fonctions, flux, règles, responsabilités, informations et critères d'acceptation.

## Pour aller plus loin
Vérifier les frontières transactionnelles, l'idempotence et la reprise. Une acceptation technique ne prouve jamais à elle seule le règlement bancaire.

[Retour à l'index](README.md)
