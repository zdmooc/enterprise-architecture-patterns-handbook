# 01 — Request/Response : échanges synchrones

## Problème et intention
Un consommateur doit obtenir immédiatement une information ou une décision : consultation de statut de virement, vérification d'un droit, validation de données. Le modèle **Request/Response** corrèle une requête et sa réponse. Il n'est pas synonyme de REST : HTTP, gRPC, SOAP et messagerie MQ request/reply peuvent le réaliser. Une API HTTP peut également lancer un traitement **asynchrone** et retourner 202 Accepted.

## Fonctionnement
~~~mermaid
sequenceDiagram
  participant C as Canal bancaire
  participant G as API Gateway
  participant S as Payment API
  participant D as Référentiel de statut
  C->>G: GET /payments/VIR-001
  G->>S: Requête autorisée (correlation-id)
  S->>D: Lire le statut
  D-->>S: SETTLED
  S-->>G: 200 {status: SETTLED}
  G-->>C: 200 + statut
~~~

La réponse immédiate est adaptée à une **consultation**. Une réponse 200/201 sur une *création* ne doit pas être confondue avec la preuve de règlement. Une création longue peut répondre 202 + paymentId + lien de suivi ; les contraintes du schéma de paiement, notamment instantané, restent prioritaires.

## Contrat de référence (fictif)
~~~http
GET /api/v1/payments/VIR-001
Authorization: Bearer TOKEN
X-Correlation-ID: trace-001

HTTP/1.1 200 OK
Content-Type: application/json

{"paymentId":"VIR-001","status":"SETTLED"}
~~~
Statuts à préciser contractuellement : RECEIVED, VALIDATING, SUBMITTED, SETTLED, REJECTED, UNKNOWN / TO_RECONCILE. Éviter un statut ambigu « SUCCESS ».

## Arbitrages de l'architecte
- **SLA / budget de latence** : budget total de bout en bout = réseau + Gateway + service + dépendances + marge ; fixer timeout de connexion, lecture et durée totale.
- **Couplage temporel** : la requête immobilise une ressource jusqu'à la réponse ; prévoir pools et limites de concurrence.
- **Contrats** : OpenAPI, validation de schéma, codes HTTP, compatibilité ascendante et versionnement.
- **Sécurité** : TLS, jeton, scopes, contrôle d'accès objet (un client ne peut pas consulter le paiement d'un autre), filtrage des données personnelles.
- **Résilience** : Circuit Breaker, Bulkhead, cache uniquement pour données non critiques et compatibles avec la fraîcheur exigée.
- **Observabilité** : latences p50/p95/p99, taux d'erreur, saturation, correlation-id et traces distribuées expurgées.

## Scénarios d'échec
| Incident | Mesure | Risque métier |
|---|---|---|
| Lecture lente | Timeout + Circuit Breaker | Afficher « indisponible », non « paiement rejeté » |
| HTTP 503 | Retry borné pour une lecture idempotente | Tempête de requêtes si pas de backoff |
| Réponse de création perdue | Retrouver l'ordre par idempotency-key | Double ordre lors de répétition |
| Service disponible, DB indisponible | Dégradation contrôlée | Statut non vérifiable |

## Quand préférer autre chose
Préférer Queue/Event-Driven quand le traitement dépasse le budget de réponse, doit survivre à une indisponibilité ou ne nécessite pas de résultat synchrone. Un parcours peut combiner POST synchrone **d'acceptation technique** et traitement asynchrone.

## Checklist revue de conception
- Le code HTTP et le **statut métier** sont-ils distincts ?
- Quel est le budget de latence, quels timeouts par saut, que fait le client après un délai dépassé ?
- L'opération est-elle sûre à répéter ? Quels identifiants et clés d'idempotence ?
- AuthZ objet, mTLS interne si requis, audit et protection des logs ?
- Quel état est présenté si la réponse d'une création est perdue ?

## Entretien
**Q : pourquoi ne pas tout faire en REST synchrone ?** R : cela crée un couplage de disponibilité et de latence, et ne résout ni la reprise durable ni la duplication d'effets métier.

**Q : timeout = transaction annulée ?** R : non, le serveur peut avoir exécuté l'action ; il faut réconcilier.

**À relier :** 06 API Gateway, 09 Circuit Breaker, 10 Retry/Timeout/Idempotency.
