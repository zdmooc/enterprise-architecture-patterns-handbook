# Cours 51 — Factory Method (GoF Java)

> Formation architecture bancaire · Virement SEPA fictif de 500 EUR · Cours avec correction. Aucun choix produit ou délai réel de règlement n'est attribué à une banque.

## 1. Objectif pédagogique
Déléguer à une méthode polymorphe de création le choix d'un produit concret qui implémente une abstraction commune.

## 2. Situation métier
La banque possède deux processeurs pour des flux pédagogiques : StandardPaymentProcessor et InstantPaymentProcessor. Leur création varie selon le créateur utilisé; leur utilisation repose sur PaymentProcessor.

## 3. Mise en œuvre et responsabilités
Définir une abstraction PaymentCreator avec une méthode createProcessor(). StandardCreator et InstantCreator spécialisent cette méthode. Le workflow utilise le type abstrait PaymentProcessor et peut traiter l'ordre sans connaître la classe concrète.

### Exemple Java simplifié
```java
interface PaymentProcessor { void process(PaymentOrder order); }
abstract class PaymentCreator {
    protected abstract PaymentProcessor createProcessor();
    public void submit(PaymentOrder order) { createProcessor().process(order); }
}
class StandardCreator extends PaymentCreator {
    @Override protected PaymentProcessor createProcessor() {
        return new StandardPaymentProcessor();
    }
}
```

La sous-classe du créateur choisit le produit concret : c'est la caractéristique centrale du Factory Method. `PaymentOrder` et `StandardPaymentProcessor` sont des types métier d'exemple.

### Étapes de conception
1. Identifier le besoin et la frontière de responsabilité.
2. Définir les interfaces, l'objet métier principal et la source autoritative des données.
3. Distinguer la réception d'un ordre, son acceptation interne, sa transmission et la confirmation financière.
4. Choisir un mécanisme de contrôle des mutations, doublons et opérations concurrentes.
5. Documenter les hypothèses et les conditions d'une alternative plus simple.

## 4. Compromis et anti-patterns
Une méthode avec un simple `switch(type)` qui retourne plusieurs classes est souvent une Simple Factory, pas nécessairement le Factory Method GoF fondé sur l'extension polymorphe. Ne pas attribuer aux fabriques les règles de règlement elles-mêmes.

**Questions à trancher :** quel gain de découplage ou de maintenabilité ? Quel coût en classes et tests ? Quel comportement après panne, réponse perdue ou version incompatible ?

## 5. Tests et preuves
Instantiation standard et instantanée, compatibilité du contrat Processor, comportement métier identique à scénario comparable, test lors d'une nouvelle variante.

**Critères d'acceptation :** tests positifs et négatifs exécutables, contrats versionnés, invariants vérifiés, résultat observable, stratégie de reprise documentée et attribution des décisions.

## 6. Exercice corrigé
**Quelle option correspond à la bonne démarche ?**

- A. Créer partout les implémentations avec new.
- B. Déléguer la création polymorphe à des créateurs spécialisés et consommer une interface commune.
- C. Remplacer automatiquement tous les processeurs par des microservices.

**Bonne réponse : B.** Déléguer à une méthode polymorphe de création le choix d'un produit concret qui implémente une abstraction commune.

## 7. Application à la mission d'architecte
Expliquer au comité pourquoi ce pattern est pertinent ici, pourquoi une solution plus simple peut parfois suffire et quelle preuve vous exigerez avant mise en production.

[Retour à l'index](README.md) · [Fiche du pattern](../../19-java-design-patterns-gof/02-factory-method/README.md)
