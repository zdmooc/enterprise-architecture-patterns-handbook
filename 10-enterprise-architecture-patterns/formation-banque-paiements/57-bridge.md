# Cours 57 — Bridge (GoF Java)

> Formation architecture bancaire · Cas fictif : virement SEPA de 500 EUR · **Cours validé : B**.

## Objectif
**Bridge** est un design pattern structurel qui sépare une **abstraction** de son **implémentation**, pour que les deux axes d'évolution puissent varier indépendamment sans créer une classe pour chaque combinaison.

## Problème métier et technique
Notre banque doit traiter deux catégories de virements : SEPA classique et SEPA instantané. Elle dispose aussi de plusieurs mécanismes techniques de communication : API REST et IBM MQ.

Une conception naïve crée des classes `StandardRestPayment`, `StandardMqPayment`, `InstantRestPayment`, `InstantMqPayment`, puis multiplie les variantes.

Attention : cet exemple est **conceptuel**. Toutes les combinaisons rail/transport ne sont pas nécessairement autorisées ou conformes en production. Le contrat du système externe, les délais et les garanties déterminent les associations réellement valides.

## Principe et rôles
- **Abstraction :** `PaymentService`, point d'entrée du traitement.
- **Abstractions raffinées :** `StandardPaymentService` et `InstantPaymentService`, chacune portant ou appelant les règles de son rail.
- **Implementor :** `PaymentTransport`, contrat de transmission.
- **ConcreteImplementors :** `RestPaymentTransport` et `MqPaymentTransport`.

L'abstraction **contient une référence** à l'interface d'implémentation. Ce lien par composition évite de combiner les variantes par héritage.

## Exemple Java simplifié
~~~java
interface PaymentTransport {
    TransmissionReceipt send(PaymentInstruction instruction);
}

abstract class PaymentService {
    protected final PaymentTransport transport;

    protected PaymentService(PaymentTransport transport) {
        this.transport = transport;
    }

    abstract TransmissionReceipt submit(PaymentInstruction instruction);
}

final class StandardPaymentService extends PaymentService {
    StandardPaymentService(PaymentTransport transport) {
        super(transport);
    }

    @Override
    TransmissionReceipt submit(PaymentInstruction instruction) {
        // Les contrôles métier sont faits par les services compétents.
        return transport.send(instruction);
    }
}

// Assemblage, si cette combinaison est autorisée :
PaymentService service = new StandardPaymentService(
    new MqPaymentTransport()
);
~~~

Les types `PaymentInstruction`, `TransmissionReceipt` et `MqPaymentTransport` sont des exemples à implémenter.

## Diagramme logique
~~~mermaid
flowchart LR
    A["StandardPaymentService"] --> P["PaymentTransport"]
    B["InstantPaymentService"] --> P
    P --> R["RestPaymentTransport"]
    P --> M["MqPaymentTransport"]
~~~

Ce diagramme décrit les **dépendances de type**; il ne suggère pas d'appeler les deux transports pour un même ordre.

## Différence avec Adapter
- **Adapter :** rend compatibles deux interfaces qui existent déjà, par traduction.
- **Bridge :** sépare intentionnellement, dès la conception, deux dimensions destinées à évoluer indépendamment.
- **Strategy :** choisit un comportement ou algorithme interchangeable; Bridge structure plus largement une abstraction et une hiérarchie d'implémentations indépendantes. Les mécanismes peuvent se ressembler techniquement.

## Limites et invariants
1. Le transport n'est pas propriétaire des règles de paiement ni des statuts financiers.
2. Un accusé de transport ne prouve **ni acceptation métier ni règlement**.
3. En cas de timeout après envoi, rechercher le résultat via la référence stable avant toute répétition potentiellement dangereuse.
4. Assurer compatibilité des rails et transports via une matrice de combinaisons autorisées.
5. La séparation introduit des abstractions supplémentaires : elle n'est justifiée que si les deux axes évoluent réellement.

## Tests et preuves
- Standard + MQ, si ce couple est pris en charge : émission nominale et contrat.
- Standard + REST, si pris en charge : même sens fonctionnel des statuts.
- Instantané + transport autorisé : respect des exigences spécifiques du rail.
- Association non autorisée : rejet explicite à la configuration.
- Panne de transport après envoi : référence stable, recherche de statut et absence de double exécution.
- Remplacer un transport sans modifier la logique du rail.

## Exercice corrigé
**La banque souhaite gérer plusieurs types de paiements et plusieurs transports sans multiplier les classes.**

- **A.** Créer une classe concrète pour chaque combinaison.
- **B.** Utiliser Bridge pour séparer le type de paiement de l'implémentation de communication.
- **C.** Imposer un seul transport mondial au moyen de Singleton.

**Bonne réponse : B.** Bridge fait évoluer les deux dimensions indépendamment, tout en conservant les règles d'association et les garanties bancaires.

[Retour à l'index](README.md) · [Cahier de révision](exercices-et-corriges/cours-13-57.md)
