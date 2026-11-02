# Architecture de synthèse — Architecture décisionnelle / ODM · cours 221–225

> **Cas fictif, architecture illustrative** : non raccordée à un SI bancaire, à une licence propriétaire ou aux clusters réels. Les tests décrits sont à exécuter.

## 1. HLD
~~~mermaid
flowchart LR
    APPS["Java, batch, COBOL via adapter"] --> API["API Decision Service versionnée"]
    API --> PORT["DecisionEvaluator port"]
    PORT --> PROD["Adapter moteur autoritatif"]
    PORT --> SHADOW["Adapter candidat shadow (sans effet)"]
    PROD --> OUT["Decision + reasonCodes + ruleSetVersion"]
    OUT --> AUDIT["Journal audit / approbation"]
    SHADOW -. "Différences" .-> AUDIT
~~~

## 2. Frontières, invariants et décisions
1. **[Decision Service Boundary](../221-decision-service-boundary.md)** — Contrat versionné et provenance décisionnelle.
2. **[Rule Engine Adapter](../222-rule-engine-adapter.md)** — Domaine découplé du moteur / éditeur.
3. **[Rule Version Pinning / Promotion](../223-rule-version-pinning.md)** — Version hash règles, moteur et input retraçables.
4. **[Shadow Decision Evaluation](../224-shadow-decision-evaluation.md)** — Moteur shadow sans effet ni décision effective.
5. **[Decision Audit & Human Review](../225-decision-audit-human-review.md)** — Audit et approbation sur payload/version exacts.

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

[Sommaire](../README.md) · [Cahier de révision](../exercices-et-corriges/cours-221-225.md) · [Matrice des preuves](matrice-preuves-186-225.md)
