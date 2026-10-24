# Cours 39 — Modular Monolith

> Formation architecture bancaire · Cas fictif SEPA de 500 EUR · Pattern et exercice corrigé.

## Objectif et définition
Un monolithe modulaire est déployé comme une seule application mais respecte des frontières internes fortes.

## 1. Contexte concret
Dans le moteur bancaire Java, les modules Contrôle, Traitement et Suivi possèdent des API internes et ne manipulent pas les tables privées des autres.

## 2. Conception proposée
Définir module owner, entrées, sorties et tables privées; contrôler imports; conserver une transaction locale lorsque justifiée, sans exposer les données internes.

### Méthode de l'architecte
1. Préciser la capacité métier et l'invariant de paiement à protéger.
2. Délimiter responsabilités, interfaces, données et frontières transactionnelles.
3. Définir le scénario nominal et le statut attesté à chaque étape.
4. Décrire refus, réponse perdue, doublon, concurrence et reprise.
5. Démontrer le bénéfice par comparaison avec une solution plus simple.

## 3. Limites et compromis
Des appels directs aux tables d'un autre module transforment le monolithe modulaire en monolithe couplé.

Ne jamais confondre prise en charge d'un ordre et règlement bancaire confirmé. L'acceptation technique, le transport et la preuve financière sont des événements différents.

## 4. Validation et preuves
Tester indépendance des modules, contrôle de dépendances, absence de tables transverses et reprise après panne.

**Critères de sortie :** tests positifs et négatifs, contrat documenté, propriété des données validée, traçabilité et décision d'architecture argumentée.

## 5. Exercice de consolidation corrigé
**Quelle option est conforme au pattern ?**

- A. Transformer chaque classe en service.
- B. Mélanger toutes les règles.
- C. Isoler les modules derrière leurs interfaces et déployer ensemble.

**Bonne réponse : C.** Un monolithe modulaire est déployé comme une seule application mais respecte des frontières internes fortes.

## 6. Question d'architecte senior
Expliquer quand éviter ce pattern : si sa complexité dépasse le besoin réel, un monolithe simple ou un module bien isolé peut être préférable. Donner le critère de décision, pas uniquement la technologie.

[Retour à l'index](README.md) · [Fiche technique](../../11-application-software-patterns/04-modular-monolith/README.md)
