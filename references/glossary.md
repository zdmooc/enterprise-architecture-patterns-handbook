# Glossaire d'architecture d'intégration

| Terme | Sens précis dans ce référentiel |
|---|---|
| ACL | Anti-Corruption Layer : couche de traduction et de protection du modèle métier |
| Adapter | Composant de conversion de protocoles, schémas ou interfaces |
| API Management | Gouvernance et cycle de vie des APIs |
| API Gateway | Point de contrôle et de routage des appels API |
| At-least-once | Livraison éventuellement répétée, à dédupliquer |
| Backoff / Jitter | Espacement progressif et variable des retries |
| BOQ / Backout Queue | File applicative de quarantaine pour échecs récurrents |
| Bulkhead | Isolation de ressources/concurrence pour limiter la propagation de pannes |
| Circuit Breaker | Coupe temporairement des appels vers une dépendance malade |
| Correlation ID | Identifiant reliant les traces et échanges d'une opération |
| Dead Letter Queue | File pour messages que le middleware ne peut acheminer selon le cas |
| EDA | Event-Driven Architecture : organisation autour des événements |
| Event ID | Identifiant d'occurrence événementielle, pour déduplication |
| Event Sourcing | Reconstruire un état à partir d'un journal d'événements, non requis en EDA |
| Event Streaming | Publication/consommation et traitement continus de journaux d'événements |
| Idempotence | Même intention répétée sans nouvel effet métier indésirable |
| Idempotency-Key | Clé stable d'une intention, généralement scindée par client/contexte |
| Kafka Offset | Position d'un record dans une partition |
| MQ Syncpoint | Unité de travail MQ validée ou annulée |
| Outbox | Enregistrement local durable des messages à publier avec les données métier |
| PaymentId | Référence stable de l'ordre de paiement dans un domaine |
| Pivot Transaction | Étape après laquelle l'effet ne se compense plus simplement |
| Pub/Sub | Publication à plusieurs abonnements logiques |
| Reconciliation | Vérifier et aligner les états sur la source autoritative |
| Saga | Coordination de transactions locales, avec compensations possibles |
| SCT Inst | Schéma SEPA Instant Credit Transfer |
| Settled | Réglé selon preuve du système autoritatif |
| Timeout | Limite d'attente technique, pas conclusion métier |
| TO_RECONCILE | État opérationnel fictif signalant une issue à rapprocher |
| Transactional Outbox | Pattern reliant transaction locale et publication ultérieure fiable |
| SCA | Strong Customer Authentication, authentification forte du client |
| RTO / RPO | Temps de reprise / point de reprise visés |
| SLO | Objectif mesurable de niveau de service |
| DLQ/parking | Quarantaine à traiter sous contrôle humain/automatique |
