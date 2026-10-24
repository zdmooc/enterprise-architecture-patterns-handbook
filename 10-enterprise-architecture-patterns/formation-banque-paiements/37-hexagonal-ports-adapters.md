# Cours 37 — Architecture hexagonale : Ports et Adapters

> Formation architecture bancaire · Banque fictive · Virement SEPA de 500 EUR.

## Objectif
Comprendre le pattern et le justifier sur une architecture bancaire réelle ou simulée, en séparant faits attestés et hypothèses.

## Principe
Les ports définissent ce que le cœur métier attend; les adaptateurs implémentent les communications avec le monde extérieur.

## Étude de cas
Le moteur reçoit un ordre par REST ou IBM MQ et persiste dans PostgreSQL, mais les règles bancaires restent identiques.

## Démarche détaillée
Définir les ports SoumettreOrdre et EnregistrerOrdre; implémenter adaptateurs REST, MQ et PostgreSQL. Traiter l'identifiant de paiement comme référence stable et isoler les règles du protocole.

### Étapes de revue
1. Identifier acteurs, fonctions et composants concernés.
2. Décrire entrées, sorties, contrats et sources autoritatives.
3. Attribuer chaque décision et chaque information à un responsable.
4. Préciser les cas nominaux, refus métier, délais, doublons et reprises.
5. Distinguer ordre reçu, accepté, transmis et règlement confirmé.

## Risques, compromis et limites
Un adaptateur ne doit pas porter l'essentiel des règles; ports et adaptateurs ne garantissent pas seuls l'absence de double débit.

Comparer systématiquement la solution à une approche plus simple, consigner les contraintes de disponibilité, coût, intégration, conformité et maintenabilité.

## Plan de tests et preuves
Tester substitution PostgreSQL par un double, mêmes décisions sur REST et MQ, panne après persistance et demande rejouée.

**Livrable :** scénario et preuve d'exécution, contrat, résultat vérifiable, décision documentée et condition de repli.

## Exercice corrigé
**Quelle décision convient à ce cours ?**

- A. Importer PostgreSQL dans les règles métier.
- B. Définir un port de persistance avec adaptateur remplaçable.
- C. Réécrire les règles bancaires.

**Bonne réponse : B.** Les ports définissent ce que le cœur métier attend; les adaptateurs implémentent les communications avec le monde extérieur.

## Pour aller plus loin
Vérifier les frontières transactionnelles, l'idempotence et la reprise. Une acceptation technique ne prouve jamais à elle seule le règlement bancaire.

[Retour à l'index](README.md)
