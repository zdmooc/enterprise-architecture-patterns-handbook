# Cahier de révision — cours 74 à 83 : Java/JEE et Spring

> 10 cours publiés avec corrigés théoriques, sans validation individuelle des questionnaires en session. Les réponses du cahier servent à l'auto-évaluation.

| Cours | Concept | Réponse théorique | Risque à savoir défendre |
|---:|---|:---:|---|
| 74 | [Dependency Injection](../74-dependency-injection.md) | **B** | Privilégier l'injection par constructeur : dépendances requises explicites et objet correctement initialisé. |
| 75 | [Inversion of Control (IoC)](../75-inversion-of-control.md) | **C** | IoC est le principe général ; DI est une façon de le réaliser. Dependency Inversion est un principe de direction des dépendances : les trois notions ne sont pas synonymes. |
| 76 | [Bean Scopes et Lifecycle](../76-bean-scopes-lifecycle.md) | **B** | `singleton` est une seule instance par définition de bean et par conteneur Spring, non un leader unique multi-pods. |
| 77 | [Spring AOP](../77-spring-aop.md) | **B** | En AOP par proxy, l'auto-invocation `this.autreMethode()` ne passe pas par l'advice. |
| 78 | [Spring Transactions](../78-spring-transactions.md) | **C** | `@Transactional` protège la ressource gérée ; ne promet aucune atomicité automatique DB + broker externe. |
| 79 | [Spring Data / JPA](../79-spring-data-jpa.md) | **A** | `@Version` détecte des modifications concurrentes sur une entité versionnée ; elle ne suffit pas à garantir l'idempotence globale. |
| 80 | [Spring MVC / REST](../80-spring-mvc-rest.md) | **B** | `202 Accepted` indique que la demande est acceptée pour traitement, pas un règlement confirmé ; choisir le code HTTP selon le vrai contrat. |
| 81 | [Exception Handling Spring](../81-exception-handling.md) | **C** | Un timeout externe ne prouve pas que la banque n'a rien exécuté ; permettre la recherche d'état via identifiant stable. |
| 82 | [Tests unitaires et d'intégration](../82-spring-testing.md) | **B** | Un test unitaire avec mocks ne démontre pas un comportement transactionnel JPA réel. |
| 83 | [Configuration Spring Boot](../83-spring-boot-configuration.md) | **C** | Les Secrets Kubernetes ne doivent pas être supposés suffisants sans contrôle RBAC, chiffrement approprié et processus de rotation. |

## Synthèse : distinguer IoC, DI et DIP
- **DIP** : orienter les dépendances vers des abstractions stables plutôt que vers les détails techniques.
- **DI** : donner au composant ses collaborateurs de l'extérieur, préférablement par constructeur.
- **IoC** : confier l'assemblage et parfois le cycle de vie des composants au conteneur.
- **Spring AOP** : intercepter certains appels au travers des proxies ; l'auto-invocation ne traverse généralement pas le proxy.

## Cas de synthèse — SEPA fictif 500 EUR
1. Une API REST reçoit une commande avec une clé d'idempotence.
2. Le cas d'usage injecté consulte des ports métier (contrôle, persistance).
3. Une transaction PostgreSQL atomique écrit `ORDERS` + `OUTBOX`.
4. Un worker lit l'Outbox et publie vers Kafka ou IBM MQ. Les consommateurs doivent gérer les doublons.
5. Une requête de statut consulte la source autoritative ou une projection explicitement qualifiée ; l'acceptation ne signifie jamais le règlement.
6. Les tests exercent concurrence, rollback, timeout, réponse perdue, panne broker, et redémarrage d'un pod.

## Mini-examen de catégorie (3 questions)
**Q1.** Une méthode annotée `@Transactional` est appelée par `this.method()` dans le même bean. A : transaction toujours active ; **B : l'appel interne peut contourner le proxy** ; C : le code ne compile pas. **Réponse B.**

**Q2.** Ordre et Outbox dans PostgreSQL, puis Kafka. A : transaction SQL + publication Outbox avec déduplication ; B : `@Transactional` garantit un commit Kafka atomique ; C : supprimer l'Outbox. **Réponse A.**

**Q3.** Cinq pods exécutent un bean singleton Spring. A : une seule instance dans tout le cluster ; B : aucune ; **C : en règle générale, une instance par définition de bean et par contexte de chaque pod**. **Réponse C.**

## Points de non-conformité à détecter
- Réutiliser une référence de virement sans contrôle d'idempotence du chemin complet.
- Déduire un règlement définitif d'un HTTP 200/202, d'un ACK de broker ou d'un timeout.
- Laisser des montants de clients en champs d'un singleton Spring.
- Supposer que l'AOP intercepte tous les appels internes.
- Croire qu'un test Mockito prouve les garanties d'une transaction PostgreSQL réelle.
- Placer des secrets d'environnement dans le code, l'image ou les logs.

[Retour au programme](../README.md) · [Schéma de synthèse](../schemas/spring-paiement-74-83.md)
