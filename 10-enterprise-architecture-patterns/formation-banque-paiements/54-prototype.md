# Cours 54 — Prototype (GoF Java)

> Banque fictive · Virement SEPA de 500 EUR · Réponse validée : **A**.

## Objectif
Prototype est un pattern de création : fabriquer un nouvel objet à partir d'un objet modèle, au lieu de reconstruire toutes ses propriétés.

## Cas bancaire
Un client conserve un modèle de virement vers un bénéficiaire, de 500 EUR. Pour préparer un nouveau virement, il copie le modèle.

Le nouveau brouillon reprend les informations pertinentes, mais reçoit une **nouvelle référence** et un **état non exécuté**. Les contrôles bancaires demeurent nécessaires avant toute soumission.

## Exemple Java conceptuel
~~~java
PaymentTemplate model = templates.load("MODEL-001");
PaymentOrder draft = model.newDraft("ORDER-002");
paymentService.validate(draft);
~~~

Ces types et méthodes sont illustratifs, et non une bibliothèque Java.

## Copie profonde et superficielle
Une copie superficielle peut partager des objets internes mutables avec le modèle. Une copie profonde les duplique. Des objets immuables peuvent être partagés lorsqu'ils sont sûrs. Choisir selon les invariants, pas systématiquement.

## Comparaison
- **Builder :** construire progressivement un objet à partir de paramètres.
- **Factory Method :** déléguer le choix de la classe concrète à une méthode de création.
- **Prototype :** créer par copie d'un modèle existant.

## Limites et risques
Ne jamais réutiliser la référence ni le statut d'un virement déjà exécuté. Copier un modèle ne confirme pas le règlement et ne dispense pas des contrôles métier. Le pattern ne garantit pas l'idempotence financière.

## Vérifications
1. Copie d'un modèle de 500 EUR : nouveau brouillon avec référence distincte.
2. Modification du brouillon sans modifier le modèle d'origine.
3. Champs imbriqués mutables isolés lorsque nécessaire.
4. Statut du brouillon jamais « réglé ».
5. Plafond et droits contrôlés avant la soumission.

## Exercice corrigé
Comment créer une demande depuis un modèle enregistré ?

**A.** Copier le modèle, générer une nouvelle référence et réinitialiser l'état.

**B.** Réutiliser le même objet et la même référence de paiement.

**C.** Partager un seul ordre via Singleton.

**Bonne réponse : A.** Prototype réutilise un modèle tout en créant un objet indépendant.

[Retour à l'index](README.md)
