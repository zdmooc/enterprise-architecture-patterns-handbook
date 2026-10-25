# Cours 58 — Composite (GoF Java)

> Formation architecture bancaire · Banque fictive · **Cours validé : réponse C**.

## 1. Problème
Une banque commercialise des services individuels (compte, carte, assurance selon le périmètre) et des offres regroupant plusieurs services. Elle veut présenter une arborescence et appliquer certaines opérations de manière uniforme aux éléments simples et aux groupes.

## 2. Principe
Le design pattern structurel **Composite** permet aux clients de manipuler uniformément un **objet simple** (Leaf) et un **objet composé** (Composite) à travers une interface commune (Component).

- **Component :** interface `BankingProduct`.
- **Leaf :** `CardProduct`, `AccountProduct` ou un service individuel.
- **Composite :** `BankingPackage`, contenant plusieurs `BankingProduct`.
- **Client :** le configurateur d'offre ou l'application de consultation.

Un objet composé peut contenir d'autres objets composés; l'ensemble forme un arbre. Des opérations de consultation peuvent être effectuées récursivement.

## 3. Exemple Java simplifié

~~~java
interface BankingProduct {
    String label();
    void collectLabels(List<String> target);
}

final class CardProduct implements BankingProduct {
    public String label() { return "Carte"; }
    public void collectLabels(List<String> target) {
        target.add(label());
    }
}

final class BankingPackage implements BankingProduct {
    private final String name;
    private final List<BankingProduct> children;

    BankingPackage(String name, List<BankingProduct> children) {
        this.name = name;
        this.children = List.copyOf(children);
    }

    public String label() { return name; }
    public void collectLabels(List<String> target) {
        for (BankingProduct child : children) {
            child.collectLabels(target);
        }
    }
}
~~~

L'exemple illustre uniquement la structure. Il suppose les imports Java habituels pour `List` et ne constitue pas une bibliothèque bancaire réelle.

## 4. Application aux frais bancaires
Le modèle permet d'énumérer les composants d'une offre puis d'appliquer des règles tarifaires appropriées. **Les frais d'une offre groupée ne sont pas nécessairement la simple somme des frais unitaires** : remises, conditions d'éligibilité, périodicité et fiscalité éventuelle doivent être traitées par un composant de tarification métier autoritatif.

## 5. Invariants et limites
- Une feuille n'est pas obligée de fournir des méthodes d'ajout ou de suppression d'enfants.
- Prévenir les références cycliques et les parcours infiniment récursifs.
- Définir à qui appartiennent les objets et leurs règles de modification.
- Ne pas confondre représentation commerciale d'un groupe de produits et écritures comptables réelles.
- Pour un ensemble toujours plat et simple, une collection ordinaire peut suffire.

## 6. Tests et preuves
1. Un produit individuel produit son libellé.
2. Une offre contenant plusieurs produits retourne une liste structurée complète.
3. Une offre imbriquée est parcourue sans perdre ni répéter involontairement de produit.
4. Toute opération modifiant la composition contrôle les cycles.
5. Le calcul des frais respecte les règles tarifaires de la banque et ne se contente pas d'une addition aveugle.

## 7. Exercice corrigé
**La banque souhaite manipuler produits individuels et offres regroupées via une interface commune.**

- **A.** Singleton, pour un seul produit bancaire partagé.
- **B.** Adapter, pour traduire une ancienne interface.
- **C.** Composite, pour représenter uniformément éléments individuels et groupes.

**Bonne réponse : C.** Composite permet de traiter feuilles et ensembles à travers une abstraction partagée.

## 8. À expliquer en entretien
Composite s'emploie quand une structure hiérarchique « partie-tout » est pertinente. Le pattern décrit la composition; les règles tarifaires et les responsabilités métier restent distinctes.

[Retour à l'index](README.md) · [Cahier de révision](exercices-et-corriges/cours-13-58.md)
