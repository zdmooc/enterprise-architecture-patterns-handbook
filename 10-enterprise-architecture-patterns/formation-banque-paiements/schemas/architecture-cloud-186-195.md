# Architecture de synthèse — Cloud hybride / Multicloud · cours 186–195

> **Cas fictif, architecture illustrative** : non raccordée à un SI bancaire, à une licence propriétaire ou aux clusters réels. Les tests décrits sont à exécuter.

## 1. HLD
~~~mermaid
flowchart LR
    SITE["Core bancaire on-prem"] --> LINK["Réseau privé / transit contrôlé"]
    LINK --> LAND["Landing zone cloud gouvernée"]
    LAND --> API["API Java / OpenShift"]
    LAND --> OBS["Audit / IAM / quotas"]
    LAND --> DR["Région secondaire standby"]
    DR --> FENCE["Bascule + fencing"]
    FENCE --> SITE
~~~

## 2. Frontières, invariants et décisions
1. **[Landing Zone](../186-landing-zone.md)** — Gouvernance IAM/réseau/audit avant workload.
2. **[Hub-and-Spoke](../187-hub-spoke.md)** — Flux interspokes autorisés et centralisés.
3. **[Transit Connectivity](../188-transit-connectivity.md)** — Routage hybride sans fuite et sans conflit CIDR.
4. **[Private Connectivity](../189-private-connectivity.md)** — Aucun fallback public implicite pour données sensibles.
5. **[Multi-Account Governance](../190-multi-account-governance.md)** — Projets séparés avec policies communs.
6. **[Multi-Region Strategy](../191-multi-region-strategy.md)** — Un seul writer par clé lors de bascule.
7. **[Hybrid Workload Placement](../192-hybrid-workload-placement.md)** — Placement guidé par résidence, latence, SLA et coût.
8. **[Cloud Bursting](../193-cloud-bursting.md)** — Bursting seulement pour workload et données autorisés.
9. **[Infrastructure as Code](../194-infrastructure-as-code.md)** — Plan/review/drift et secrets protégés.
10. **[Cloud Exit & Portability](../195-cloud-exit-portability.md)** — Restitution des données et redéploiement vérifiable.

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

[Sommaire](../README.md) · [Cahier de révision](../exercices-et-corriges/cours-186-195.md) · [Matrice des preuves](matrice-preuves-186-225.md)
