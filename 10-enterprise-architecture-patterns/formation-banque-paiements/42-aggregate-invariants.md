# Cours 42 — DDD : Aggregate et invariants

> Formation architecture bancaire · Cas fictif SEPA de 500 EUR · Pattern et exercice corrigé.

## Objectif et définition
L'agrégat protège les règles de cohérence et contrôle les mutations via une racine.

## 1. Contexte concret
Un OrdrePaiement de 500 EUR est accepté; un autre traitement tente de changer son montant à 900 EUR. La racine refuse la modification non autorisée.

## 2. Conception proposée
Définir la frontière de cohérence locale de l'ordre, ses transitions autorisées et l'optimistic locking; garder l'agrégat assez petit pour être transactionnel.

### Méthode de l'architecte
1. Préciser la capacité métier et l'invariant de paiement à protéger.
2. Délimiter responsabilités, interfaces, données et frontières transactionnelles.
3. Définir le scénario nominal et le statut attesté à chaque étape.
4. Décrire refus, réponse perdue, doublon, concurrence et reprise.
5. Démontrer le bénéfice par comparaison avec une solution plus simple.

## 3. Limites et compromis
Un agrégat n'assure pas l'exactly-once inter-applicatif; gérer idempotence, référence et rapprochement séparément.

Ne jamais confondre prise en charge d'un ordre et règlement bancaire confirmé. L'acceptation technique, le transport et la preuve financière sont des événements différents.

## 4. Validation et preuves
Tester changement du montant après acceptation, transition rejeté → transmis, deux modifications simultanées et reprise.

**Critères de sortie :** tests positifs et négatifs, contrat documenté, propriété des données validée, traçabilité et décision d'architecture argumentée.

## 5. Exercice de consolidation corrigé
**Quelle option est conforme au pattern ?**

- A. Modifier directement les colonnes.
- B. Autoriser toute mutation tardive.
- C. Passer par l'agrégat et vérifier les invariants.

**Bonne réponse : C.** L'agrégat protège les règles de cohérence et contrôle les mutations via une racine.

## 6. Question d'architecte senior
Expliquer quand éviter ce pattern : si sa complexité dépasse le besoin réel, un monolithe simple ou un module bien isolé peut être préférable. Donner le critère de décision, pas uniquement la technologie.

[Retour à l'index](README.md) · [Fiche technique](../../11-application-software-patterns/07-aggregate-invariants/README.md)
