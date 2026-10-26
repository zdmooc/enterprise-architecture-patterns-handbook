# Architecture de synthèse — Java/Spring : initiation SEPA fictive 500 EUR

> Cas pédagogique, non représentatif d'un établissement. Les composants financiers et les statuts demeurent sous l'autorité des systèmes habilités.

## Structure
```mermaid
flowchart LR
    UI["Mobile ou portail"] --> API["Spring MVC / Validation / Advice"]
    API --> UC["Use Case / DI / IoC"]
    UC --> FRAUD["Port FraudChecker"]
    UC --> TX["@Transactional SQL"]
    TX --> ORDERS[("ORDERS + version + clé idem")]
    TX --> OUTBOX[("OUTBOX")]
    OUTBOX --> WORKER["Worker publication"]
    WORKER --> BROKER["Kafka ou IBM MQ"]
    BROKER --> CONSUMER["Consommateur idempotent"]
    API --> READ["GET statut autorisé"]
    READ --> SOURCE["Source autoritative / projection qualifiée"]
```

## Séquence transactionnelle et réponse perdue
```mermaid
sequenceDiagram
    participant UI as Client
    participant API as REST Spring
    participant UC as PaymentUseCase
    participant DB as PostgreSQL
    participant W as Outbox Worker
    participant B as Broker
    UI->>API: POST ordre 500 EUR + clé stable
    API->>UC: submit(...)
    UC->>DB: début transaction locale
    UC->>DB: insert ordre + événement Outbox
    DB-->>UC: commit
    UC-->>API: reçu / référence
    Note over API,UI: réponse HTTP peut être perdue
    W->>DB: lire événements committés
    W->>B: publier (rejouable, doublon possible)
    UI->>API: GET statut avec autorisation
    API-->>UI: statut connu, jamais inventé
```

## Arbitrages
- `202 Accepted` peut indiquer une demande en traitement ; ne signifie ni acceptation financière ni règlement.
- L'autorité de règlement ne dépend pas de Spring ni du broker.
- Les transactions SQL et broker ne sont pas atomiques du seul fait de `@Transactional`.
- L'Outbox peut émettre plusieurs fois : déduplication et idempotence jusqu'à l'exécution.
- Isolation des données et droits objet obligatoires ; pas de secrets dans les configurations versionnées.
- Liveness/readiness, arrêt et reprise après redémarrage sur OpenShift à qualifier.
- Les métriques, observations et vues ne doivent pas remplacer l'audit financier source de vérité.

## Tests GO/NO-GO
1. Requête répétée après timeout et commit : pas de deuxième ordre.
2. Erreur SQL avant Outbox : rollback commun.
3. Panne de broker : Outbox non perdue, reprise ensuite.
4. Doublon de publication : un seul effet métier.
5. État incomplet dans projection : information « en cours/inconnue » plutôt que faux règlement.
6. Cinq pods : aucune donnée d'ordre stockée dans des champs singleton.
7. Accès à l'ordre d'un autre client : refus par la source autorisée.
8. Configuration invalide et secret indisponible : démarrage ou service non prêt selon politique.

[Programme 74–83](../README.md) · [Cahier de révision](../exercices-et-corriges/cours-74-83.md)
