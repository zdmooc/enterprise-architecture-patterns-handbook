# Matrice de décision : quel pattern pour quel besoin ?

| Besoin principal | Pattern privilégié | Compléments / pièges |
|---|---|---|
| Consulter immédiatement un statut | Request/Response | Timeout, autorisation objet, Circuit Breaker |
| Encaisser une commande alors que le destinataire peut être arrêté | Messaging/Queue | Persistant, backout, idempotence métier |
| Informer 3 applications d'un paiement réglé | Pub/Sub | Contrat événement, subscribers durables |
| Organiser réactions à un paiement demandé/autorisé/réglé | EDA | Saga/owner d'état, transitions et observabilité |
| Analyser à grande échelle des transactions et rejouer historique | Event Streaming | Kafka retention, partition, offsets, lag |
| Exposer des APIs bancaires sécurisées | API Gateway | API Management, AuthZ objet métier |
| Moderniser COBOL/CICS sans polluer Java | ACL + Adapter | Strangler Fig, traduction sémantique |
| Coordonner réservation, contrôle, soumission, compensation | Saga | Point irréversible et états durables |
| Dépendance aval saturée | Circuit Breaker + Bulkhead | Timeout et baisse de charge |
| Échec temporaire potentiellement récupérable | Retry | Backoff/jitter, deadline, idempotence |
| Appel ou message répété | Idempotency | DB UNIQUE + référence stable **au cœur** |
| BD locale modifiée puis publication message | Transactional Outbox | Relais republie parfois |
| Événement/message redélivré | Idempotent Consumer | Déduplication atomique |
| Traitement au statut inconnu | Reconciliation | Ne pas interpréter timeout comme échec |

## Arbre de décision rapide
~~~mermaid
flowchart TD
  N{"Ai-je besoin d'une réponse immédiate ?"}
  N -->|Oui| REQ["Request/Response avec budget timeout"]
  N -->|Non| A{"Travail pour un seul responsable ?"}
  A -->|Oui| Q["Queue / Messaging"]
  A -->|Non| B{"Diffusion de faits à plusieurs abonnés ?"}
  B -->|Oui| PS["Pub/Sub"]
  B -->|Flux volumineux + replay| ES["Event Streaming"]
  REQ --> R["Sécurité + Circuit Breaker + idempotence si effet"]
  Q --> R
  PS --> R
  ES --> R
~~~
Cet arbre aide à démarrer ; une architecture réelle peut combiner plusieurs patterns et ajouter Saga, EDA, Outbox, ACL selon ses invariants.

## Trois erreurs classiques
1. Confondre API Gateway et API Management.
2. Confondre la réception MQ / la publication Kafka et l'exécution d'un paiement.
3. Affirmer que la compensation Saga peut inverser un règlement déjà irrévocable.
