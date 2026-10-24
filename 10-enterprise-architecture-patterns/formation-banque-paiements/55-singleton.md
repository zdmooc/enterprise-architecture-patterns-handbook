# Cours 55 — Singleton (GoF Java)

> Formation architecture bancaire · Banque fictive · Exemple de virement SEPA de 500 EUR · **Cours validé : réponse B.**

## 1. Objectif
Le pattern **Singleton** offre un point d'accès commun à une instance unique **dans un périmètre d'exécution défini**. Ce périmètre ne couvre pas automatiquement plusieurs JVM, chargeurs de classes ou pods OpenShift.

## 2. Exemple bancaire
Un moteur Java traite de nombreux ordres de paiement. Un composant sans état formate les références des virements pour l'affichage. Il peut être partagé entre les traitements d'une même application, plutôt que reconstruit à chaque demande.

Le formatage de la référence est distinct de la génération de sa valeur unique et du traitement financier. Aucun état de client, montant modifiable ni ordre en cours ne doit être conservé dans cette instance partagée.

## 3. Implémentation Java pédagogique
~~~java
public enum PaymentReferenceFormatter {
    INSTANCE;

    public String display(String reference) {
        return "Virement : " + reference;
    }
}

// Utilisation :
String label = PaymentReferenceFormatter.INSTANCE.display("PAY-001");
~~~

Un `enum` avec un élément constitue une manière simple d'implémenter un Singleton dans une JVM avec ses garanties de chargement propres. Pour un projet Spring, un bean à portée singleton fourni par l'injection de dépendances répond souvent mieux aux besoins de testabilité; sa portée est liée au contexte Spring.

## 4. Périmètre et concurrence
- Une application avec plusieurs JVM ou plusieurs pods OpenShift possède en général **plusieurs instances** de ce composant.
- Le code partagé doit être sûr en concurrence : idéalement **sans état mutable**.
- Un Singleton ne garantit pas l'unicité distribuée d'un ordre, d'un numéro de référence ou d'un traitement de paiement.
- Le verrouillage distribué, le leader election ou l'idempotence relèvent de solutions distinctes à choisir selon l'invariant métier.

## 5. Compromis et anti-patterns
**Atouts :** objet partagé, accès cohérent, absence de créations répétées inutiles pour certains composants.

**Limites :** dépendance globale difficile à remplacer dans les tests, risque d'état mutable transversal, hypothèse erronée d'unicité entre déploiements.

**Anti-pattern :** stocker les paiements de tous les clients ou les données d'une transaction courante dans un Singleton global.

## 6. Plan de tests
1. Dans le périmètre défini, les accès obtiennent la même instance.
2. Des appels concurrents produisent le même format pour une même entrée.
3. Aucun champ mutable ne conserve des informations appartenant à un client.
4. Deux pods OpenShift ne sont pas supposés partager la même instance Java.
5. La prévention du double traitement est assurée par les identifiants et contrôles métier, indépendamment du Singleton.

## 7. Exercice corrigé
**Quel usage est correct dans notre banque ?**

- **A.** Conserver tous les virements des clients dans un Singleton.
- **B.** Partager un composant sans état en respectant le périmètre d'unicité et la sûreté des accès concurrents.
- **C.** Supposer qu'un Singleton Java est unique dans tout le cluster OpenShift.

**Bonne réponse : B.** L'unicité vaut pour le périmètre d'exécution de l'implémentation; elle n'est pas une garantie d'unicité métier distribuée.

## 8. Question d'entretien
**Un Singleton garantit-il une seule instance dans un cluster de cinq pods ?**

Non. Chaque JVM ou contexte applicatif peut posséder sa propre instance. Il faut une stratégie distribuée distincte lorsque l'unicité globale est réellement nécessaire.

[Retour au programme](README.md) · [Cahier de révision](exercices-et-corriges/cours-13-55.md)
