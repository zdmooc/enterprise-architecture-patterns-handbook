# CRM omnicanal : données clients, réservations et documents

**Cas d'architecture original et synthétique pour préparer des missions futures.** Pas un état client réellement déployé.

## 1. Décision à instruire

Plusieurs applications transportent une identité client, des réservations et des documents. La synchronisation batch et API peut produire des doublons, retards et conflits.

## 2. Architecture de principe

```mermaid
flowchart LR
 A["Entrée et identité"] --> B["Façade / contrat"] --> C["Domaine et adaptateurs"] --> D["Persistance et preuve"]
```

Flux métier envisagé : **Source commande --> ACL et Outbox --> Transport --> Inbox + Customer 360 --> Portail autorisé**. Chaque flèche doit porter un propriétaire, un contrat, une politique de sécurité et un comportement en timeout.

## 3. Patterns sélectionnés

- [12 data architecture patterns](../../12-data-architecture-patterns/01-data-ownership/README.md)
- [12 data architecture patterns](../../12-data-architecture-patterns/11-master-data-management/README.md)
- [11 application software patterns](../../11-application-software-patterns/02-hexagonal-ports-adapters/README.md)
- [18 enterprise integration patterns](../../18-enterprise-integration-patterns/01-transactional-outbox/README.md)
- [18 enterprise integration patterns](../../18-enterprise-integration-patterns/02-transactional-inbox/README.md)
- [14 security zero trust patterns](../../14-security-zero-trust-patterns/06-rbac-abac/README.md)

## 4. Exécution de la démarche

1. **AS-IS et ownership** : Un propriétaire par attribut, un mapping versionné et aucun écrasement silencieux de consentement.
2. **Architecture de transition** : Distinguer identifiant maître client et projection CRM, gérer fusion ambiguë par revue humaine.
3. **Critère de validation** : Exécuter livraison initiale puis deux deltas ; rejouer les mêmes octets : zéro doublon durable.
4. **Failure engineering** : Envoi hors ordre, document orphelin, client homonyme et accès hors périmètre doivent être rejetés.
5. **Décision et limites** : PII et données clients réelles proscrites; démonstration sur fixtures entièrement fictives.

## 5. Livrables d'architecture demandés

- Contexte, hypothèses, diagramme d'interactions, contrats versionnés et NFR non inventés.
- ADR avec minimum deux options comparées : statu quo, progression ciblée et refonte si pertinente.
- Matrice de tests : nominal, duplicata, réponse perdue, panne partielle, droits objet et retour arrière.
- Verdict `GO`, `GO_CONDITIONNEL` ou `NO_GO` selon preuves, licences, sécurité et coûts.
- Rapport de test horodaté avec commande, environnement et limite de preuve; une fiche de conception n'est pas une preuve runtime.

[Recueil des cas transversaux](../README.md)
