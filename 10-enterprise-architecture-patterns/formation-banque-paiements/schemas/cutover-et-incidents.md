# Atlas 2 — Séquences d'incident et bascule Java/JEE vers OpenShift

Scénarios **fictifs**, à qualifier avant tout emploi dans une architecture réelle. Le temps imparti aux opérations SCT Inst dépend des règles applicables : aucune redélivrance tardive n'est autorisée aveuglément.

## 1. Perte de réponse métier après exécution
~~~mermaid
sequenceDiagram
  actor U as Client
  participant P as Payment API
  participant D as DB + Outbox
  participant Q as IBM MQ
  participant C as Core Banking
  participant R as Réconciliation
  U->>P: CreatePayment(500 EUR, idem PAY-001)
  P->>D: Commit intention VIR-001 + Outbox
  P-->>U: Identifiant VIR-001 ; statut non final
  D->>Q: Publier commande VIR-001
  Q->>C: Livrer VIR-001
  C->>C: Vérifier délai et unicité, exécuter
  C--xP: Réponse perdue
  P->>D: UNKNOWN / TO_RECONCILE
  U->>P: Retry PAY-001 même corps
  P-->>U: Même VIR-001, pas de débit supplémentaire
  R->>C: QueryPaymentStatus(VIR-001)
  C-->>R: Preuve autoritative
  R->>D: Transition attestée
~~~

## 2. Shadow, canary et transfert d'ownership
~~~mermaid
flowchart TB
  AS["Legacy seul"] --> SH["Shadow lecture seule / sans effets"]
  SH --> G{"Écarts critiques ?"}
  G -->|"Oui"| FIX["Corriger puis requalifier"]
  FIX --> SH
  G -->|"Non"| CAN["Canary sur ordres neufs déterministes"]
  CAN --> CT{"Cutover validé ?"}
  CT -->|"Non"| STOP["Geler admission ; réconcilier en vol"]
  CT -->|"Oui"| TARGET["Nouveau moteur propriétaire des nouveaux ordres"]
  STOP --> R{"Compatibilité rollback ?"}
  R -->|"Oui"| OLD["Legacy reprend nouveaux ordres uniquement"]
  R -->|"Non"| INVEST["Reprise supervisée sans nouvelles commandes aveugles"]
  TARGET --> DEC["Retrait legacy après preuves"]
~~~

## 3. Checklist GO/NO-GO
- Le périmètre et les propriétaires des ordres en cours sont documentés.
- Aucun chemin double d'exécution financière n'est actif pour le même paymentId.
- La cible gère les retours tardifs, les réponses MQ, les erreurs Core et les délais du scheme.
- Les contrats d'interface et de données sont compatibles ou les transformations sont testées.
- Les journaux d'audit et clés de corrélation permettent la réconciliation.
- Le plan de rollback gère la compatibilité des schémas et les effets irréversibles.
- Les tests de panne, d'idempotence, de sécurité, de charge et de PRA attendus sont disponibles et examinés.

## 4. Matrice d'incident
| Injection | Comportement attendu | Preuve |
|---|---|---|
| Arrêt consommateur MQ | Alerte âge/profondeur ; délai métier contrôlé | Reprise admissible ou rejet/réconciliation |
| Crash après effet Core | Aucun deuxième mouvement | Même paymentId et preuve comptable |
| Perte Kafka | Publication reprise depuis Outbox | Événement dérivé, sans recommander un débit |
| Crash pendant cutover | Ownership déterministe après redémarrage | Routage rejoué, inventaire en vol |
| Schema DB incompatible | NO-GO rollback de code | Matrice compatibilité / décision |
| Commande SCT Inst expirée | Aucune exécution tardive aveugle | Log décision et rapprochement |

[Retour au parcours](../README.md).
