# Cours 52 — Abstract Factory (GoF Java)

> Formation architecture bancaire · Virement SEPA fictif de 500 EUR · Cours avec correction. Aucun choix produit ou délai réel de règlement n'est attribué à une banque.

## 1. Objectif pédagogique
Créer des familles cohérentes d'objets apparentés à travers une fabrique abstraite, sans coupler le client aux classes concrètes.

## 2. Situation métier
Deux familles de traitements pédagogiques coexistent : SEPA classique et SEPA instantané. Chacune exige un validateur et un processeur compatibles.

## 3. Mise en œuvre et responsabilités
Définir PaymentFamilyFactory avec createValidator() et createProcessor(). StandardPaymentFactory produit le couple validateur/processeur classique. InstantPaymentFactory produit le couple instantané. Le cas d'usage choisit une famille et consomme ses abstractions.

### Exemple Java simplifié
```java
interface PaymentFamilyFactory {
    PaymentValidator createValidator();
    PaymentProcessor createProcessor();
}
class InstantPaymentFactory implements PaymentFamilyFactory {
    public PaymentValidator createValidator() {
        return new InstantPaymentValidator();
    }
    public PaymentProcessor createProcessor() {
        return new InstantPaymentProcessor();
    }
}
```

La fabrique construit deux produits d'une même famille. Les classes `PaymentValidator`, `PaymentProcessor` et leurs implémentations sont des exemples, pas des bibliothèques standard Java.

### Étapes de conception
1. Identifier le besoin et la frontière de responsabilité.
2. Définir les interfaces, l'objet métier principal et la source autoritative des données.
3. Distinguer la réception d'un ordre, son acceptation interne, sa transmission et la confirmation financière.
4. Choisir un mécanisme de contrôle des mutations, doublons et opérations concurrentes.
5. Documenter les hypothèses et les conditions d'une alternative plus simple.

## 4. Compromis et anti-patterns
Une famille cohérente ne garantit pas la conformité réglementaire, les délais de règlement ou l'absence de doubles opérations. La multiplication des familles peut compliquer l'ajout d'un nouveau type de produit à toutes les fabriques.

**Questions à trancher :** quel gain de découplage ou de maintenabilité ? Quel coût en classes et tests ? Quel comportement après panne, réponse perdue ou version incompatible ?

## 5. Tests et preuves
Vérifier famille classique complète, famille instantanée complète, absence de mélange involontaire, substitution de famille en test et impact d'un nouveau produit.

**Critères d'acceptation :** tests positifs et négatifs exécutables, contrats versionnés, invariants vérifiés, résultat observable, stratégie de reprise documentée et attribution des décisions.

## 6. Exercice corrigé
**Quelle option correspond à la bonne démarche ?**

- A. Singleton, pour n'avoir qu'un objet global.
- B. Observer, pour diffuser des notifications.
- C. Abstract Factory, pour créer une famille de composants compatibles.

**Bonne réponse : C.** Créer des familles cohérentes d'objets apparentés à travers une fabrique abstraite, sans coupler le client aux classes concrètes.

## 7. Application à la mission d'architecte
Expliquer au comité pourquoi ce pattern est pertinent ici, pourquoi une solution plus simple peut parfois suffire et quelle preuve vous exigerez avant mise en production.

[Retour à l'index](README.md) · [Fiche du pattern](../../19-java-design-patterns-gof/03-abstract-factory/README.md)
