# Architecture de synthèse — Platform Engineering · cours 216–220

> **Cas fictif, architecture illustrative** : non raccordée à un SI bancaire, à une licence propriétaire ou aux clusters réels. Les tests décrits sont à exécuter.

## 1. HLD
~~~mermaid
flowchart LR
    TEAMS["Équipes produit"] --> PORTAL["Golden Path / Backstage optionnel"]
    PORTAL --> CI["CI : SBOM / signature"]
    CI --> GIT["GitOps et policies"]
    GIT --> OCP["OpenShift / Control Plane"]
    OCP --> CELL_A["Cell A : workloads Paiements"]
    OCP --> CELL_B["Cell B : workloads Analytics"]
    POLICY["RBAC / quotas / NetworkPolicy / Kyverno"] --> OCP
~~~

## 2. Frontières, invariants et décisions
1. **[Control Plane / Data Plane Separation](../216-control-plane-data-plane.md)** — Panne du contrôle sans nouveau privilège data plane.
2. **[Golden Path / Paved Road](../217-golden-path.md)** — Template non-root, SBOM, probes et admission.
3. **[Multi-Tenant Isolation / Noisy Neighbor](../218-multi-tenant-isolation.md)** — Secret et quotas de A isolés de B.
4. **[Policy as Code / Admission Guardrails](../219-policy-as-code.md)** — CI et admission appliquent policy versionnée.
5. **[Cell-Based Architecture / Fault Containment](../220-cell-based-architecture.md)** — Panne cell A n'affecte pas B et pas de double writer.

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

[Sommaire](../README.md) · [Cahier de révision](../exercices-et-corriges/cours-216-220.md) · [Matrice des preuves](matrice-preuves-186-225.md)
