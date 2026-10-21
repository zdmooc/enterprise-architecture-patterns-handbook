# Atlas 1 — Architecture bancaire logique, capacités et flux

Ce document regroupe trois perspectives sur un **cas fictif** de virement de 500 EUR. Elles sont complémentaires, mais ne doivent pas être confondues. Ni noms de files ni topologie ne représentent une installation réelle.

## Vue 1 — Capacité et domaines métier
~~~mermaid
flowchart TB
  P["Gérer un paiement SEPA"]
  P --> I["Initier"]
  P --> C["Contrôler et autoriser"]
  P --> X["Exécuter / échanger"]
  P --> S["Suivre, rejeter, réconcilier"]
  C -.-> F["Domaine Fraude"]
  X -.-> B["Domaine Comptes"]
  X -.-> E["Domaine Interbancaire"]
  I -.-> CL["Domaine Clients"]
~~~

## Vue 2 — Applications et responsabilité financière
~~~mermaid
flowchart TB
  U["Web/mobile"] --> G["API Gateway / IAM"]
  G --> A["Payment API Java"]
  A --> P["Orchestrateur paiement"]
  A --> D[("PostgreSQL suivi / intentions / Outbox")]
  P --> D
  P --> F["Fraude et contrôles"]
  D --> O["Relay commande"]
  O --> Q["IBM MQ / commandes"]
  Q --> AD["Adaptateur Core"]
  AD --> C["Core Banking / source autoritative"]
  C <--> R["Passerelle / réseau SEPA"]
  C -->|"PaymentResult corrélé"| AD
  AD -->|"Réponse via MQ et consumer"| P
  D --> OE["Relay événements"]
  OE --> K["Kafka / statuts dérivés"]
  K --> N["Notification / BI"]
~~~

## Vue 3 — Classification des interfaces
| Type | Exemple | Information à préserver |
|---|---|---|
| Appel synchrone | Mobile → Payment API | Authentification, idempotence, statut d'intention |
| Commande asynchrone | Outbox → IBM MQ → Core | paymentId, deadline, schéma, ACK distinct du règlement |
| Résultat métier | Core → moteur via MQ/ACL | Preuve d'exécution corrélée |
| Événement | DB Outbox → Kafka | Fait attesté, contrat versionné, permissions |
| Lecture / projection | Reporting → vue dérivée | Fraîcheur, source, confidentialité |

## Invariants de revue
- **Ne pas** traiter un ACK de broker comme une confirmation de débit/règlement.
- **Ne pas** créer un paiement neuf après timeout sans réconciliation.
- **Ne pas** confier l'autorité financière à une projection de reporting.
- **Ne pas** supposer l'atomicité d'une transaction couvrant automatiquement DB, MQ et Core.
- **Ne pas** réexécuter aveuglément un ordre instantané hors échéance.

[Retour au parcours](../README.md).
