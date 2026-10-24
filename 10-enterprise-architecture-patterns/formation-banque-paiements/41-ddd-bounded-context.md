# Cours 41 — DDD : Bounded Context

> Formation architecture bancaire · Cas fictif SEPA de 500 EUR · Pattern et exercice corrigé.

## Objectif et définition
Un Bounded Context délimite vocabulaire, règles, modèle et responsabilités d'un domaine.

## 1. Contexte concret
Le contexte OrdresPaiement dit « accepté » après validation interne, mais le contexte Rapprochement ne dit « réglé » qu'après preuve externe.

## 2. Conception proposée
Définir glossaire propre à chaque contexte; attribuer la source autoritative; traduire statuts et événements via contrats explicites. Plusieurs contextes peuvent exister dans un monolithe.

### Méthode de l'architecte
1. Préciser la capacité métier et l'invariant de paiement à protéger.
2. Délimiter responsabilités, interfaces, données et frontières transactionnelles.
3. Définir le scénario nominal et le statut attesté à chaque étape.
4. Décrire refus, réponse perdue, doublon, concurrence et reprise.
5. Démontrer le bénéfice par comparaison avec une solution plus simple.

## 3. Limites et compromis
Un modèle de statut universel peut fusionner des notions bancaires incompatibles; un contexte n'est pas synonyme de microservice.

Ne jamais confondre prise en charge d'un ordre et règlement bancaire confirmé. L'acceptation technique, le transport et la preuve financière sont des événements différents.

## 4. Validation et preuves
Tester conversion d'états, copie obsolète, confirmation tardive et impossibilité de passer d'accepté à réglé sans preuve.

**Critères de sortie :** tests positifs et négatifs, contrat documenté, propriété des données validée, traçabilité et décision d'architecture argumentée.

## 5. Exercice de consolidation corrigé
**Quelle option est conforme au pattern ?**

- A. Considérer accepté et réglé comme synonymes.
- B. Séparer modèles et contrats explicites entre contextes.
- C. Partager un statut sans définition.

**Bonne réponse : B.** Un Bounded Context délimite vocabulaire, règles, modèle et responsabilités d'un domaine.

## 6. Question d'architecte senior
Expliquer quand éviter ce pattern : si sa complexité dépasse le besoin réel, un monolithe simple ou un module bien isolé peut être préférable. Donner le critère de décision, pas uniquement la technologie.

[Retour à l'index](README.md) · [Fiche technique](../../11-application-software-patterns/06-ddd-bounded-context/README.md)
