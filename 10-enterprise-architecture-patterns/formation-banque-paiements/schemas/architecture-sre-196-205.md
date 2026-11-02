# Architecture de synthèse — Performance / SRE · cours 196–205

> **Cas fictif, architecture illustrative** : non raccordée à un SI bancaire, à une licence propriétaire ou aux clusters réels. Les tests décrits sont à exécuter.

## 1. HLD
~~~mermaid
flowchart LR
    USER["Client"] --> LB["Load balancer / rate limit"]
    LB --> API["Payment API répliquée"]
    API --> POOL["Pool / budget latence"]
    POOL --> DB["DB / idempotence"]
    API --> MQ["IBM MQ / backlog"]
    MQ --> CORE["Core autoritatif"]
    MET["SLI, SLO / Golden Signals"] --> API
    MET --> MQ
    LIMIT["Backpressure / quota"] --> API
~~~

## 2. Frontières, invariants et décisions
1. **[Caching Patterns](../196-caching-patterns.md)** — Cache sous droits et fraîcheur, non source financière.
2. **[Load Balancing](../197-load-balancing.md)** — Balancer uniquement les pods Ready.
3. **[Sharding](../198-sharding.md)** — Un owner autoritatif par paymentId.
4. **[Connection Pooling](../199-connection-pooling.md)** — Connexions bornées selon capacité aval.
5. **[Async Offload](../200-async-offload.md)** — Tâches différées suivies durablement.
6. **[Rate Limiting](../201-rate-limiting.md)** — Refus avant effet et quotas cohérents.
7. **[Latency Budget](../202-latency-budget.md)** — Budget end-to-end et deadline métier.
8. **[Golden Signals](../203-golden-signals.md)** — Latence, trafic, erreurs et saturation visibles.
9. **[SLI / SLO / Error Budget](../204-sli-slo-error-budget.md)** — SLO basé sur expérience et exactitude métier.
10. **[Capacity Planning](../205-capacity-planning.md)** — Dimensionnement incluant aval, mémoire et MQ.

## 3. Séquence de perte de réponse commune
~~~mermaid
sequenceDiagram
    participant A as Appelant
    participant P as Plateforme / composant
    participant S as Source bancaire autoritative
    A->>P: commande référence stable, 500 EUR
    P->>S: effet autorisé
    S--xP: confirmation non reçue
    P->>P: état incertain, pas de nouveau paymentId
    P->>S: recherche par référence / réconciliation
    S-->>P: état prouvé ou UNKNOWN
    P-->>A: résultat exact, sans invention
~~~

## 4. Plan de validation
| Dimension | Ce qu'il faut démontrer |
|---|---|
| Métier | Aucun double effet, statuts autoritatifs et traçabilité |
| Sécurité | IAM, isolation tenant, secrets, chiffrement et autorisation objet |
| NFR | Débit, latence, disponibilité, RTO/RPO et capacités selon pattern |
| Exploitation | Détection, réconciliation, on-call, rollback approprié |
| Gouvernance | Versioning, ADR, preuves des alternatives et règles GO/NO-GO |

### Limite de preuve
Une documentation, un test statique ou un manifeste YAML ne prouve pas que les flux ont fonctionné dans un cluster. Les seuils réglementaires et contraintes de paiement restent à valider pour l'établissement et le schéma concernés.

[Sommaire](../README.md) · [Cahier de révision](../exercices-et-corriges/cours-196-205.md) · [Matrice des preuves](matrice-preuves-186-225.md)
