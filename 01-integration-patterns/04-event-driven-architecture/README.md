# 04 — Event-Driven Architecture (EDA)

## Définition : un style architectural, pas un broker
Une **EDA** organise les applications autour de faits significatifs (« PaymentRequested », « FundsReserved », « PaymentSettled »). Un service réagit à un fait métier et produit à son tour une décision, un état ou un nouvel événement. **Pub/Sub** est l'un de ses mécanismes de distribution ; Kafka ou messagerie MQ sont des choix d'infrastructure et non la définition de l'EDA.

## Exemple bancaire fictif : virement de 500 €
~~~mermaid
flowchart TD
  A["Demande de virement"] --> E1["PaymentRequested"]
  E1 --> V["Contrôles / risque"]
  V -->|autorisé| E2["PaymentAuthorized"]
  V -->|refusé| R["PaymentRejected"]
  E2 --> F["Gestion des fonds"]
  F --> E3["FundsReserved"]
  E3 --> P["Exécution bancaire"]
  P -->|confirmation autoritative| E4["PaymentSettled"]
  E4 --> N["Notification / Reporting"]
~~~

Ce flux est *logique*. Pour une opération critique, les décisions d'avancement peuvent être **orchestrées par une Saga**. On ne confond jamais événements « commandés », « acceptés » et « réglés ».

## Deux modèles de communication
- **Notification d'événement** : renseigne sur un fait accompli ; abonnés autonomes.
- **Event-carried state transfer** : transporte certaines données permettant une projection autonome ; données minimales, vie privée et fraîcheur à cadrer.
Ne pas faire dépendre une décision financière irréversible de données reçues tardivement ou dont l'autorité est incertaine.

## Event contract (illustratif)
~~~json
{
  "eventId":"evt-002",
  "type":"PaymentAuthorized",
  "schemaVersion":1,
  "aggregateId":"VIR-001",
  "occurredAt":"2026-10-18T10:00:00Z",
  "correlationId":"corr-01",
  "causationId":"evt-001"
}
~~~
Les champs correlationId / causationId permettent le suivi de chaînes d'événements. Ne pas inscrire secrets, PAN, IBAN complets ou autres données sensibles inutilement.

## Garanties à concevoir
- **Publication atomique avec changement d'état local** : Outbox ou alternative rigoureusement justifiée.
- **At-least-once et redélivrance** : consommateurs idempotents ; eventId stable.
- **Ordre** : les événements peuvent arriver hors ordre entre partitions et producteurs ; numéro de version/sequence par agrégat, contrôle des transitions.
- **Convergence** : projections éventuellement cohérentes ; indiquer aux consommateurs quelle source fait autorité.
- **Évolution** : schémas gouvernés, compatibilité et métadonnées.
- **Supervision** : DLQ/parking, métriques de délais bout en bout, lag, taux de duplication et événements sans propriétaire.

## Scénarios de panne et décisions
| Incident | Mauvaise réaction | Réaction correcte |
|---|---|---|
| Notification hors service | Bloquer le règlement | Rejouer notification indépendamment |
| Event PaymentSettled en double | Double écriture comptable | Déduplication par transition métier |
| Événements hors ordre | Basculer SETTLED vers PROCESSING | Refuser transition arrière |
| Publication perdue | Considérer le SI convergent | Outbox + rapprochement |
| Contrôle antifraude en échec | Avancer automatiquement | Décision explicite selon politique |

## Quand ne pas choisir une EDA
Un CRUD simple à faible couplage, une décision exigeant une cohérence strictement synchrone, ou un workflow à états très réglementés mais sans mécanisme de corrélation/reprise. La multiplication de microservices événementiels peut augmenter les coûts de compréhension et d'exploitation.

## Gouvernance d'architecture
Identifier propriétaire de chaque événement, matrice producteur/consommateur, catalogue, fréquence/volumétrie, version, classification des données, SLO de propagation et tests de contract. Documenter les transitions interdites.

## Questions entretien
**EDA vs Pub/Sub ?** EDA = organisation des réactions autour de faits ; Pub/Sub = diffusion. **EDA = Event Sourcing ?** Non : Event Sourcing reconstruit l'état depuis le journal des événements ; ce n'est pas une exigence EDA. **Le broker fait-il respecter le cycle de vie financier ?** Non : la logique métier et la réconciliation appartiennent à l'application et au système autoritatif.

Liens : 03 Pub/Sub, 05 Event Streaming, 08 Saga, 10 Idempotency.

---

## Illustrations complémentaires — une architecture réactive aux faits métier

### La chaîne du virement et les branches indépendantes
~~~mermaid
flowchart TD
    A["PaymentRequested"] --> B["Contrôles obligatoires"]
    B -->|"Validé"| C["PaymentAuthorized"]
    B -->|"Refusé"| R["PaymentRejected"]
    C --> D["Gestion des fonds"]
    D --> E["FundsReserved"]
    E --> F["Soumission et confirmation de règlement"]
    F --> G["PaymentSettled"]
    G --> N["Notification"]
    G --> S["Supervision"]
    G --> L["Projection analytique"]
~~~
Chaque bloc réagit à un **fait publié** selon un contrat. En pratique, la Saga peut orchestrer les commandes critiques ; les branches de notification restent indépendantes.

### Différence d'intention : événement et commande
~~~mermaid
flowchart LR
    O["Saga"] -->|"Commande : ReserveFunds"| F["Service Fonds"]
    F -->|"Fait : FundsReserved"| T["Bus événementiel"]
    T --> S["Saga : étape suivante"]
    T --> A["Audit métier"]
~~~
Un événement ne doit pas être traité comme une commande déguisée : le producteur annonce ce qui **a eu lieu** ; le consommateur reste responsable de sa réaction.

### Point de vigilance
Si \`PaymentSettled\` arrive deux fois, le service de notification évite deux envois non souhaités par déduplication ; si \`PaymentRejected\` arrive **après** \`PaymentSettled\`, la machine à états refuse une régression sans preuve de correction.

