# Cours 49 — Unit of Work

> Formation architecture bancaire · Virement SEPA fictif de 500 EUR · Cours avec correction. Aucun choix produit ou délai réel de règlement n'est attribué à une banque.

## 1. Objectif pédagogique
Regrouper les modifications devant être validées ou annulées ensemble dans une frontière transactionnelle locale.

## 2. Situation métier
Le moteur Java accepte un ordre de virement SEPA de 500 EUR et doit enregistrer l'état de l'ordre et son journal d'audit local de manière cohérente.

## 3. Mise en œuvre et responsabilités
Dans une transaction locale, charger l'agrégat, contrôler les invariants, modifier son état, enregistrer les modifications et valider une seule unité. Un échec avant commit entraîne rollback. Si un message doit être émis après commit, considérer le pattern Outbox transactionnelle.


### Étapes de conception
1. Identifier le besoin et la frontière de responsabilité.
2. Définir les interfaces, l'objet métier principal et la source autoritative des données.
3. Distinguer la réception d'un ordre, son acceptation interne, sa transmission et la confirmation financière.
4. Choisir un mécanisme de contrôle des mutations, doublons et opérations concurrentes.
5. Documenter les hypothèses et les conditions d'une alternative plus simple.

## 4. Compromis et anti-patterns
Unit of Work ne rend pas atomiques par magie les écritures entre plusieurs bases, IBM MQ et systèmes externes. Ne jamais assimiler commit de l'ordre à règlement interbancaire.

**Questions à trancher :** quel gain de découplage ou de maintenabilité ? Quel coût en classes et tests ? Quel comportement après panne, réponse perdue ou version incompatible ?

## 5. Tests et preuves
Panne entre écriture et commit, concurrence sur la même référence, rollback, crash après commit et avant publication d'événement; réexécution idempotente.

**Critères d'acceptation :** tests positifs et négatifs exécutables, contrats versionnés, invariants vérifiés, résultat observable, stratégie de reprise documentée et attribution des décisions.

## 6. Exercice corrigé
**Quelle option correspond à la bonne démarche ?**

- A. Valider chaque table indépendamment sans contrôle.
- B. Supposer qu'une transaction locale englobe toutes les banques.
- C. Regrouper les mutations locales cohérentes dans une unité transactionnelle.

**Bonne réponse : C.** Regrouper les modifications devant être validées ou annulées ensemble dans une frontière transactionnelle locale.

## 7. Application à la mission d'architecte
Expliquer au comité pourquoi ce pattern est pertinent ici, pourquoi une solution plus simple peut parfois suffire et quelle preuve vous exigerez avant mise en production.

[Retour à l'index](README.md) · [Fiche du pattern](../../11-application-software-patterns/14-unit-of-work/README.md)
