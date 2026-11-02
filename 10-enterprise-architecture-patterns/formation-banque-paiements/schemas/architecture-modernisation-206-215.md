# Architecture de synthèse — Modernisation Legacy · cours 206–215

> **Cas fictif, architecture illustrative** : non raccordée à un SI bancaire, à une licence propriétaire ou aux clusters réels. Les tests décrits sont à exécuter.

## 1. HLD
~~~mermaid
flowchart LR
    USER["Canal / partner"] --> ROUTE["Façade / routage Strangler"]
    ROUTE --> LEG["WAS / EJB legacy"]
    ROUTE --> NEW["Liberty ou Spring sur OpenShift"]
    LEG --> SRC["État métier autoritatif"]
    NEW --> SRC
    SHADOW["Shadow sans effet"] -. "Comparaison" .-> NEW
    DB["Expand–Contract versionné"] --> NEW
    CUT["GO/NO-GO + cutover"] --> ROUTE
~~~

## 2. Frontières, invariants et décisions
1. **[Rehost](../206-rehost.md)** — Runtime et contrats identiques ou écarts expliqués.
2. **[Replatform](../207-replatform.md)** — Compatibilité EJB/JTA/JMS et support éditeur qualifiés.
3. **[Refactor](../208-refactor.md)** — Règles métier et effets inchangés.
4. **[Replace](../209-replace.md)** — Historique et contrats repris sans perte.
5. **[Retire](../210-retire.md)** — Zéro consommateur actif et rétention préservée.
6. **[Retain](../211-retain.md)** — Legacy conservé sous contrôle et roadmap.
7. **[Strangler Fig Migration](../212-strangler-fig-migration.md)** — Un seul exécuteur autoritatif à la fois.
8. **[Parallel Run / Shadow](../213-parallel-run-shadow.md)** — Shadow sans effet métier externe.
9. **[Expand–Contract Database](../214-expand-contract-db.md)** — Coexistence versions API et schémas.
10. **[Cutover / Rollback](../215-cutover-rollback.md)** — Bascule exclusive et rapprochement financier.

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

[Sommaire](../README.md) · [Cahier de révision](../exercices-et-corriges/cours-206-215.md) · [Matrice des preuves](matrice-preuves-186-225.md)
