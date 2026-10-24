# Cours 53 — Builder (GoF Java)

> Formation architecture bancaire. Cas fictif : virement SEPA de 500 EUR. **Cours validé : C.**

## Problème
Un ordre de paiement contient compte débiteur, bénéficiaire, montant, devise, référence et date éventuelle. Un constructeur Java à de nombreux paramètres devient difficile à lire.

## Principe
Builder est un pattern de création GoF. Il permet de renseigner progressivement les champs d'un objet, puis de produire un objet cohérent avec `build()`. Il est utile pour les objets complexes, avec champs obligatoires et optionnels.

## Exemple Java
~~~java
PaymentOrder order = PaymentOrder.builder()
    .debtorAccount("FR76...")
    .creditorAccount("FR14...")
    .amount(new BigDecimal("500.00"))
    .currency("EUR")
    .reference("PAY-001")
    .build();
~~~

Les types et coordonnées sont fictifs. Le Builder vérifie que les champs de construction sont présents et cohérents. **Il ne décide pas** si le virement est autorisé, ni si les fonds ou le plafond permettent de l'exécuter : ces règles restent dans les services métier.

## Architecture
~~~mermaid
flowchart LR
    A["Cas d'utilisation"] --> B["PaymentOrder.Builder"]
    B --> C["Validation des champs requis"]
    C --> D["PaymentOrder immuable"]
    D --> E["Contrôles de paiement"]
~~~

## Différences avec les autres patterns de création
- **Factory Method** : une méthode polymorphe délègue le choix d'un produit concret.
- **Abstract Factory** : fabrique plusieurs produits compatibles d'une même famille.
- **Builder** : construit progressivement un objet complexe.

## Avantages et compromis
- Lisibilité des appels et réduction des longues listes de paramètres.
- Gestion des propriétés optionnelles et vérification de la construction.
- Objet final potentiellement immuable.
- Coût de code supplémentaire : un constructeur simple peut suffire pour un objet simple.
- Aucune garantie automatique d'idempotence ni d'absence de double débit.

## Validation
1. Construire un ordre complet valide de 500 EUR.
2. Rejeter un ordre sans montant ou sans devise.
3. Gérer les options absentes conformément au contrat.
4. Vérifier qu'un montant ne peut être modifié arbitrairement après construction.
5. Garder les contrôles de plafond et de disponibilité des fonds hors du Builder.

## Exercice corrigé
**Comment construire un ordre avec de nombreux champs obligatoires et optionnels ?**

A. Singleton : un ordre partagé entre tous les clients.

B. Observer : écouter les notifications.

C. Builder : assembler chaque ordre étape par étape et valider sa construction.

**Bonne réponse : C.** Builder rend la construction explicite; il ne remplace pas les règles métier.

## Question d'entretien
**Quand éviter Builder ?** Lorsque le modèle est simple et que l'abstraction ajouterait une complexité inutile.

[Retour au programme](README.md)
