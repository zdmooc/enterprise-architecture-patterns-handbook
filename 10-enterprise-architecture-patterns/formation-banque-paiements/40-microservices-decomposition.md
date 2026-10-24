# Cours 40 — Microservices Decomposition

> Formation architecture bancaire · Cas fictif SEPA de 500 EUR · Pattern et exercice corrigé.

## Objectif et définition
Le découpage par capacités métier facilite l'autonomie quand le besoin le justifie.

## 1. Contexte concret
Les notifications de virements SEPA évoluent indépendamment du traitement financier et peuvent devenir un service séparé.

## 2. Conception proposée
Comparer monolithe modulaire et microservices; isoler la capacité Notification, définir son contrat événementiel et la gestion de ses propres données. Ne pas déplacer automatiquement la tenue de compte.

### Méthode de l'architecte
1. Préciser la capacité métier et l'invariant de paiement à protéger.
2. Délimiter responsabilités, interfaces, données et frontières transactionnelles.
3. Définir le scénario nominal et le statut attesté à chaque étape.
4. Décrire refus, réponse perdue, doublon, concurrence et reprise.
5. Démontrer le bénéfice par comparaison avec une solution plus simple.

## 3. Limites et compromis
Chaque service distribué ajoute latence, incidents possibles, besoin de traçage et de reprise; ne pas créer un microservice par classe.

Ne jamais confondre prise en charge d'un ordre et règlement bancaire confirmé. L'acceptation technique, le transport et la preuve financière sont des événements différents.

## 4. Validation et preuves
Tester arrêt des notifications, événements rejoués et ordre toujours accepté/traité sans dépendance bloquante sur la notification.

**Critères de sortie :** tests positifs et négatifs, contrat documenté, propriété des données validée, traçabilité et décision d'architecture argumentée.

## 5. Exercice de consolidation corrigé
**Quelle option est conforme au pattern ?**

- A. Créer un microservice par classe.
- B. Extraire les notifications de façon progressive avec contrats et résilience.
- C. Interdire tout microservice.

**Bonne réponse : B.** Le découpage par capacités métier facilite l'autonomie quand le besoin le justifie.

## 6. Question d'architecte senior
Expliquer quand éviter ce pattern : si sa complexité dépasse le besoin réel, un monolithe simple ou un module bien isolé peut être préférable. Donner le critère de décision, pas uniquement la technologie.

[Retour à l'index](README.md) · [Fiche technique](../../11-application-software-patterns/05-microservices-decomposition/README.md)
