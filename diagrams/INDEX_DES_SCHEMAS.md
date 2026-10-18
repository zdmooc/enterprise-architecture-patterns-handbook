# Atlas des schémas illustratifs — Intégration bancaire et architectures IA

**Objet :** retrouver rapidement tous les schémas Mermaid éditables. Les exemples reposent sur un virement fictif de **500 €** ; les acteurs sont génériques (canal, passerelle, cœur bancaire, CSM, service de notification). **Aucun schéma ne présente une architecture d'entreprise réelle.**

## Nouveau : architecture IA

- [15 patterns d'IA générative, agentique, sécurité et production](../08-ai-architecture-patterns/README.md) : **30 diagrammes** dans les fiches.
- [Architecture de référence IA sur OpenShift](../08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) : **2 diagrammes**.
- [Séquences d'une plateforme IA](../08-ai-architecture-patterns/reference-ai-platform-openshift/sequences.md) : **6 diagrammes de séquence** (RAG, outils, HITL, événement, fallback, évaluation).
- [Matrice de décision IA](../08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) : **1 arbre de décision**.
- [Index des patterns IA](../08-ai-architecture-patterns/README.md) : **1 cartographie transversale**.

En complément des **49 diagrammes historiques d'intégration et paiement**, la famille IA ajoute **40 diagrammes**, soit **89 diagrammes Mermaid** dans les sources du dépôt.

## Navigation par pattern d'intégration

| Pattern | Fiche et illustrations directement visibles | Schémas contenus dans la fiche |
|---|---|---:|
| 01 — Request / Response | [Synchrone, statut et timeout](../01-integration-patterns/01-request-response/README.md) | 3 |
| 02 — Messaging / Queue | [File persistante, consommateur arrêté et redélivrance](../01-integration-patterns/02-messaging-queue/README.md) | 3 |
| 03 — Publish / Subscribe | [Queue vs topic, trois abonnements et panne notification](../01-integration-patterns/03-publish-subscribe/README.md) | 3 |
| 04 — EDA | [Chaîne d'événements, faits et commandes](../01-integration-patterns/04-event-driven-architecture/README.md) | 3 |
| 05 — Event Streaming | [Kafka, partitions/offsets et détection d'anomalies](../01-integration-patterns/05-event-streaming/README.md) | 3 |
| 06 — API Gateway | [Routage et sécurité, API Management vs Gateway](../01-integration-patterns/06-api-gateway/README.md) | 3 |
| 07 — Adapter / ACL | [Traduction Java–legacy et migration progressive](../01-integration-patterns/07-anti-corruption-layer/README.md) | 3 |
| 08 — Saga | [Orchestration, chorégraphie, compensation et pivot](../01-integration-patterns/08-saga/README.md) | 5 |
| 09 — Circuit Breaker | [Closed/Open/Half-Open, simulation et protections associées](../01-integration-patterns/09-circuit-breaker/README.md) | 4 |
| 10 — Retry / Timeout / Idempotency | [Double POST, réponse perdue et Backoff](../01-integration-patterns/10-retry-timeout-idempotency/README.md) | 4 |

**Total des dix fiches : 34 schémas Mermaid**, directement dans les documents concernés.

## Architecture complète

- [Architecture de référence consolidée et anonymisée — SCT Inst / OpenShift](../07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md) : **8 diagrammes Mermaid** ; cartographie globale, états métier, parcours sortant/entrant, Outbox, Saga, infrastructure multisite et réconciliation.
- [Atelier pédagogique — architecture générique des paiements](../07-case-studies/banking-payments-reference/README.md) : **1 diagramme** de la plateforme intégrée.
- [Atelier — diagrammes de séquence nominaux et défaillants](../07-case-studies/banking-payments-reference/sequences.md) : **4 diagrammes de séquence** (nominal, réponse perdue, compensation et commande expirée).
- [Matrice de décision des patterns](../references/decision-matrix.md) : **1 arbre de décision** Mermaid.

## Carte simplifiée des patterns en un diagramme

~~~mermaid
flowchart TB
    CLIENT["Canal : demande de virement 500 EUR"]
    API["P1 : Request/Response"]
    GW["P6 : API Gateway / Sécurité"]
    IDEM["P10 : Idempotency / Timeout / Retry"]
    SAGA["P8 : Saga / orchestration"]
    CB["P9 : Circuit Breaker"]
    ACL["P7 : Adapter / ACL"]
    MQ["P2 : Queue / Messaging"]
    CORE["Système autoritatif de paiement"]
    EDA["P4 : Architecture événementielle"]
    TOPIC["P3 : Pub/Sub"]
    STREAM["P5 : Event Streaming"]
    NOTIF["Notification"]
    ANALYTICS["Supervision / analyse"]
    CLIENT --> GW --> API --> IDEM --> SAGA
    SAGA --> CB --> ACL --> MQ --> CORE
    CORE -->|"Fait confirmé et persistant"| EDA
    EDA --> TOPIC
    TOPIC --> NOTIF
    TOPIC --> STREAM --> ANALYTICS
~~~
**C'est une carte pédagogique**, pas une prescription de routage de tous les appels. Dans la réalisation réelle, la commande peut emprunter une API **ou** un broker selon le contrat. La validation financière vient du cœur bancaire, pas de Kafka.

## Relecture de schémas — checklist

1. Chaque flèche a-t-elle un sens métier identifiable (commande, événement, réponse, ACK technique) ?
2. Le producteur peut-il échouer après commit et avant accusé, et le schéma montre-t-il la reprise ?
3. La source de règlement est-elle autoritative, et l'événement publié après preuve ?
4. Un consommateur à l'arrêt ne bloque-t-il pas une application indépendante ?
5. Le schéma de bascule multisite empêche-t-il **deux écrivains** sur la même partition ?
6. La date limite d'un virement instantané est-elle prise en compte avant de traiter un message tardif ?
7. La légende distingue-t-elle l'exemple de la réalité de production ?

Tous les schémas sont **du texte Mermaid source versionnable** ; ils sont modifiables et rendus par les clients compatibles Markdown Mermaid.
