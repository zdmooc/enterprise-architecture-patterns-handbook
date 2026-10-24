# Cours 50 — Branch by Abstraction

> Formation architecture bancaire · Virement SEPA fictif de 500 EUR · Cours avec correction. Aucun choix produit ou délai réel de règlement n'est attribué à une banque.

## 1. Objectif pédagogique
Moderniser une implémentation sans bascule brutale, en conservant une abstraction stable utilisée par le code appelant.

## 2. Situation métier
La banque migre progressivement une fonctionnalité d'un ancien moteur Java/J2EE vers Spring Boot, tout en préservant le service aux clients.

## 3. Mise en œuvre et responsabilités
Définir une interface PaymentExecutionGateway. Conserver OldExecutionAdapter et développer NewExecutionAdapter derrière la même interface. Diriger progressivement des catégories de traitement éligibles vers la nouvelle implémentation, observer les écarts et garder une voie de repli explicitement limitée.


### Étapes de conception
1. Identifier le besoin et la frontière de responsabilité.
2. Définir les interfaces, l'objet métier principal et la source autoritative des données.
3. Distinguer la réception d'un ordre, son acceptation interne, sa transmission et la confirmation financière.
4. Choisir un mécanisme de contrôle des mutations, doublons et opérations concurrentes.
5. Documenter les hypothèses et les conditions d'une alternative plus simple.

## 4. Compromis et anti-patterns
Ne pas envoyer le même ordre financièrement exécutif aux deux implémentations. Un shadow test peut comparer des décisions sans provoquer deux effets métiers. Le rollback doit respecter les états déjà engagés, leur propriétaire et la compatibilité des données.

**Questions à trancher :** quel gain de découplage ou de maintenabilité ? Quel coût en classes et tests ? Quel comportement après panne, réponse perdue ou version incompatible ?

## 5. Tests et preuves
Bascule progressive, compatibilité de contrats, contrôle des références et idempotence, panne de nouvelle voie, rollback sans double traitement et cohabitation de versions.

**Critères d'acceptation :** tests positifs et négatifs exécutables, contrats versionnés, invariants vérifiés, résultat observable, stratégie de reprise documentée et attribution des décisions.

## 6. Exercice corrigé
**Quelle option correspond à la bonne démarche ?**

- A. Supprimer le moteur dès le premier déploiement.
- B. Introduire une abstraction, faire coexister les deux implémentations, migrer avec contrôle et repli.
- C. Conserver éternellement le legacy sans arbitrage.

**Bonne réponse : B.** Moderniser une implémentation sans bascule brutale, en conservant une abstraction stable utilisée par le code appelant.

## 7. Application à la mission d'architecte
Expliquer au comité pourquoi ce pattern est pertinent ici, pourquoi une solution plus simple peut parfois suffire et quelle preuve vous exigerez avant mise en production.

[Retour à l'index](README.md) · [Fiche du pattern](../../11-application-software-patterns/15-branch-by-abstraction/README.md)
