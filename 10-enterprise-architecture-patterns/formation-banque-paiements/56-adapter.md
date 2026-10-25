# Cours 56 — Adapter (GoF Java)

> Formation banque fictive · Exemple virement SEPA de 500 EUR · **Cours validé : réponse C.**

## Objectif

Le **pattern structurel Adapter** fait communiquer un composant client et un service existant dont les interfaces sont incompatibles, sans imposer une refonte immédiate de l'un ou l'autre.

## Situation bancaire

La banque modernise un moteur Java/J2EE vers Spring Boot. Le nouveau composant attend une interface `PaymentGateway`, tandis que l'ancien moteur expose un contrat EJB `LegacyPaymentBean`. L'objectif est d'utiliser le service historique depuis la nouvelle application en conservant la sémantique exacte des réponses.

## Mécanisme

1. **Client** : le cas d'usage moderne appelle `PaymentGateway.submit(order)`.
2. **Target** : `PaymentGateway` définit le contrat attendu par le client.
3. **Adapter** : `LegacyPaymentAdapter` implémente `PaymentGateway`.
4. **Adaptee** : `LegacyPaymentBean` reste inchangé.
5. **Transformation** : l'adaptateur convertit les données et les erreurs entre les deux contrats.

### Exemple Java conceptuel

~~~java
interface PaymentGateway {
    SubmissionResult submit(PaymentOrder order);
}

final class LegacyPaymentAdapter implements PaymentGateway {
    private final LegacyPaymentBean legacy;

    LegacyPaymentAdapter(LegacyPaymentBean legacy) {
        this.legacy = legacy;
    }

    public SubmissionResult submit(PaymentOrder order) {
        LegacyReceipt receipt = legacy.sendPayment(
            order.reference(), order.amount()
        );
        return mapLegacyReceipt(receipt);
    }

    private SubmissionResult mapLegacyReceipt(LegacyReceipt receipt) {
        // Traduction contractuelle validée par les équipes métier.
        return new SubmissionResult(receipt.reference(), "TRANSMIS");
    }
}
~~~

Types pédagogiques à adapter au vrai contrat : ce code **ne constitue pas un exemple exécutable autonome**. La conversion en `TRANSMIS` ne serait permise que si la documentation et les preuves du système ancien lui donnent réellement ce sens.

## Garanties et limites

- La traduction doit distinguer **ordre reçu, accepté, transmis et règlement confirmé**.
- L'Adapter traite la compatibilité **d'interface**. Une **Anti-Corruption Layer** protège plus largement un modèle métier des concepts, statuts et règles d'un SI historique.
- Une réponse réseau perdue après exécution du moteur ancien peut masquer un traitement réussi. Utiliser une référence stable et rechercher le statut avant de relancer.
- Adapter ne garantit **ni idempotence ni absence de double débit**.
- Le contrat EJB et les droits d'accès doivent rester encapsulés et sécurisés.

## Tests et preuve

1. Appel nominal : un ordre fictif de 500 EUR est transmis à l'interface EJB et retourne un résultat métier conforme.
2. Refus du moteur ancien : le motif est conservé et non transformé en succès.
3. Timeout après émission : le statut demeure incertain jusqu'à vérification.
4. Appel dupliqué : aucune seconde opération financière non désirée.
5. Évolution du contrat historique : un test de contrat détecte les incompatibilités.
6. Changement d'implémentation derrière `PaymentGateway` : le client moderne demeure indépendant du détail EJB.

## Exercice corrigé

**Une application Spring Boot doit utiliser un ancien moteur EJB sans dépendre directement de son interface.**

- **A.** Modifier toutes les applications pour appeler directement EJB.
- **B.** Convertir toute réponse technique en règlement financier confirmé.
- **C.** Interposer un Adapter qui préserve la sémantique des échanges.

**Bonne réponse : C.** Adapter rend compatibles les interfaces sans modifier arbitrairement le sens des réponses.

## Question d'entretien

**Quelle différence entre Adapter, Facade et Anti-Corruption Layer ?**

Adapter assure la compatibilité de deux interfaces. Facade propose une interface simplifiée devant plusieurs composants. L'Anti-Corruption Layer isole et traduit également les **concepts métier** d'un domaine historique.

[Retour aux cours](README.md) · [Révisions](exercices-et-corriges/cours-13-56.md)
