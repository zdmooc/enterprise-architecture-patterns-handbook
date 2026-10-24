# Cours 48 — Backend for Frontend (BFF)

> Formation architecture bancaire · Virement SEPA fictif de 500 EUR · Cours avec correction. Aucun choix produit ou délai réel de règlement n'est attribué à une banque.

## 1. Objectif pédagogique
Créer une interface serveur adaptée aux besoins d'un canal client, sans transférer les règles financières sensibles au canal.

## 2. Situation métier
La banque propose une application mobile et un portail conseiller. Le mobile consulte un suivi compact, le conseiller a besoin de motifs et traces complémentaires selon ses droits.

## 3. Mise en œuvre et responsabilités
Créer un BFF Mobile et éventuellement un BFF Conseiller. Chacun agrège les informations autorisées provenant des services propriétaires. Les règles de plafond, le calcul des frais et l'état autoritatif restent dans les services métiers.


### Étapes de conception
1. Identifier le besoin et la frontière de responsabilité.
2. Définir les interfaces, l'objet métier principal et la source autoritative des données.
3. Distinguer la réception d'un ordre, son acceptation interne, sa transmission et la confirmation financière.
4. Choisir un mécanisme de contrôle des mutations, doublons et opérations concurrentes.
5. Documenter les hypothèses et les conditions d'une alternative plus simple.

## 4. Compromis et anti-patterns
Deux BFF ne doivent pas redéfinir différemment la sémantique « accepté » et « réglé ». Gérer l'autorisation fine, les erreurs partielles et la fraîcheur des données.

**Questions à trancher :** quel gain de découplage ou de maintenabilité ? Quel coût en classes et tests ? Quel comportement après panne, réponse perdue ou version incompatible ?

## 5. Tests et preuves
Client non autorisé, canal inaccessible, réponse partielle, statut de paiement obsolète, surcharge et fuite d'informations confidentielles.

**Critères d'acceptation :** tests positifs et négatifs exécutables, contrats versionnés, invariants vérifiés, résultat observable, stratégie de reprise documentée et attribution des décisions.

## 6. Exercice corrigé
**Quelle option correspond à la bonne démarche ?**

- A. Copier les règles de plafond dans chaque écran.
- B. Adapter les vues par canal via un BFF en conservant les décisions métier dans les services autoritatifs.
- C. Autoriser le BFF à modifier directement les écritures comptables.

**Bonne réponse : B.** Créer une interface serveur adaptée aux besoins d'un canal client, sans transférer les règles financières sensibles au canal.

## 7. Application à la mission d'architecte
Expliquer au comité pourquoi ce pattern est pertinent ici, pourquoi une solution plus simple peut parfois suffire et quelle preuve vous exigerez avant mise en production.

[Retour à l'index](README.md) · [Fiche du pattern](../../11-application-software-patterns/13-backend-for-frontend/README.md)
