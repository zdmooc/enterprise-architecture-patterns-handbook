# Cours 38 — Clean Architecture

> Formation architecture bancaire · Cas fictif SEPA de 500 EUR · Pattern et exercice corrigé.

## Objectif et définition
Les dépendances du code doivent pointer vers les règles métier, pas vers le framework.

## 1. Contexte concret
Un ordre SEPA de 500 EUR est reçu via un contrôleur Spring Boot; le cas d'usage SoumettreVirement appelle le domaine qui contrôle le plafond sans importer Spring.

## 2. Conception proposée
Identifier entités, cas d'usage, ports d'interface et adaptateurs; isoler règles et invariants; gérer transactions et DTO hors du cœur.

### Méthode de l'architecte
1. Préciser la capacité métier et l'invariant de paiement à protéger.
2. Délimiter responsabilités, interfaces, données et frontières transactionnelles.
3. Définir le scénario nominal et le statut attesté à chaque étape.
4. Décrire refus, réponse perdue, doublon, concurrence et reprise.
5. Démontrer le bénéfice par comparaison avec une solution plus simple.

## 3. Limites et compromis
Trop de couches, classes et mappings peut masquer le flux métier; ne pas importer le framework dans le domaine.

Ne jamais confondre prise en charge d'un ordre et règlement bancaire confirmé. L'acceptation technique, le transport et la preuve financière sont des événements différents.

## 4. Validation et preuves
Tester domaine sans framework; échec de stockage; refonte de l'interface HTTP sans modification des règles.

**Critères de sortie :** tests positifs et négatifs, contrat documenté, propriété des données validée, traçabilité et décision d'architecture argumentée.

## 5. Exercice de consolidation corrigé
**Quelle option est conforme au pattern ?**

- A. Faire dépendre le domaine de Spring.
- B. Faire dépendre les composants techniques des abstractions métier.
- C. Créer un microservice par règle.

**Bonne réponse : B.** Les dépendances du code doivent pointer vers les règles métier, pas vers le framework.

## 6. Question d'architecte senior
Expliquer quand éviter ce pattern : si sa complexité dépasse le besoin réel, un monolithe simple ou un module bien isolé peut être préférable. Donner le critère de décision, pas uniquement la technologie.

[Retour à l'index](README.md) · [Fiche technique](../../11-application-software-patterns/03-clean-architecture/README.md)
