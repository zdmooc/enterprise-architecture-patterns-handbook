# Cahier de révision — cours 59 à 62 : GoF structurels

> Cas pédagogiques bancaires fictifs · Quatre cours publiés après la série 13–58. **Questions d'auto-évaluation 59–61 non répondues individuellement en session.** L'exercice transversal sur Proxy a été répondu **A (incorrect)**, corrigé **B (Proxy)**.

## 59. Decorator
**Leçon :** [Decorator](../59-decorator.md).

**Question :** ajouter mesures et journalisation sans changer le moteur, ni modifier son contrat.

- A. Decorator
- B. Réécriture du moteur
- C. Exécution simultanée d'un deuxième moteur

**Réponse : A.** Même interface, enrichissement et délégation. **Preuve :** une invocation métier, résultat identique, erreur de métrique best effort sans masquer le résultat.

## 60. Facade
**Leçon :** [Facade](../60-facade.md).

**Question :** une application consomme trois services et souhaite un point d'entrée plus simple.

- A. Appels directs à toutes les interfaces internes
- B. Facade cohérente par cas d'usage
- C. Duplication du moteur côté canal

**Réponse : B.** La Facade simplifie l'accès au sous-système. **Preuve :** sous-services spécialisés préservés, refus de validation, timeout et sémantique financière corrects.

## 61. Flyweight
**Leçon :** [Flyweight](../61-flyweight.md).

**Question :** de nombreux ordres utilisent les mêmes métadonnées EUR immuables.

- A. Partager aussi les données de paiement des clients
- B. Recréer une métadonnée pour chaque ordre
- C. Partager seulement l'état intrinsèque de la devise

**Réponse : C.** Un objet commun pour les métadonnées, état transactionnel propre à chaque ordre. **Preuve :** identité de l'objet partagé, isolation des montants, baisse de mémoire mesurée.

## 62. Proxy
**Leçon :** [Proxy](../62-proxy.md).

**Question posée en session :** ajouter un contrôle d'accès devant un service de paiement **sans changer son interface**.

- A. Facade
- B. Proxy
- C. Flyweight

**Réponse : B.** Proxy intercepte et vérifie les droits avant la délégation. **Réponse utilisateur en session : A, corrigée en B**. **Preuve :** accès non autorisé = zéro appel au service réel, contrôle sur l'objet et protection contre le contournement.

## Mini-cas de synthèse : ne pas confondre les patterns
| Besoin | Pattern | Garantie à tester |
|---|---|---|
| Ajouter métriques sans modifier `PaymentProcessor` | **Decorator** | Résultat conservé, pas de doublon de traitement |
| Simplifier le sous-système de paiement pour le portail | **Facade** | Services responsables préservés |
| Mutualiser des métadonnées de devise immuables | **Flyweight** | Aucun état client partagé |
| Contrôler l'accès à une lecture de statut | **Proxy** | Rejet et zéro délégation en cas de refus |

## Critères de validation orale
Pour chaque pattern : citer son **intention**, son **contrat**, un **cas bancaire**, une **limite** et un **test négatif**. Ne pas assimiler ces patterns de conception Java à des garanties distribuées telles que exactly-once, consensus ou règlement financier confirmé.

[Retour au programme](../README.md) · [Cahier précédent : cours 13–58](cours-13-58.md)
