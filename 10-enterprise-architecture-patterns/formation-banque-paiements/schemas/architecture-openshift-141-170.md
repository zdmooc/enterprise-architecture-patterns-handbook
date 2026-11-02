# Architecture de référence — Cours 141–170 · Modernisation Java / OpenShift

> Étude fictive : banque pédagogique, moteur de virement SEPA de 500 EUR, Java/JEE modernisé, IBM MQ, PostgreSQL et OpenShift. Ce schéma n'est ni un déploiement réel ni une validation d'un produit IBM/Red Hat.

## 1. HLD : limites de responsabilité et sécurité
~~~mermaid
flowchart LR
    USER["Client / partenaire"] --> GW["Route TLS + API Gateway / OIDC"]
    GW --> API["Payment API Java / Deployment"]
    API --> DB[("PostgreSQL : ordre + Outbox")]
    DB --> RELAY["Outbox Relay / Job ou Deployment"]
    RELAY --> MQ["IBM MQ / broker validé"]
    MQ --> WORKER["Consumers / autoscaling backlog"]
    WORKER --> CORE["Système bancaire source de vérité"]
    GIT["Git : manifests, image digest"] --> ARGO["Argo CD : sync / drift"]
    ARGO --> OCP["API OpenShift"]
    OCP --> API
    OCP --> WORKER
    VAULT["Vault / secrets externes"] --> API
    VAULT --> WORKER
    POLICY["SCC / RBAC / NetworkPolicy / Kyverno"] --> OCP
    OBS["OTel / Prometheus / Grafana / Loki"] --> API
    OBS --> WORKER
~~~

**Flux** : la requête est validée côté Gateway ET backend, l'ordre est stocké de manière idempotente, l'Outbox transporte une intention vers MQ, un consommateur vérifie la référence métier au service autoritatif. Les ACK techniques ne représentent jamais une preuve de règlement.

## 2. Séquence de bout en bout et perte de réponse
~~~mermaid
sequenceDiagram
    participant U as Client
    participant A as API Java sur OpenShift
    participant D as PostgreSQL + Outbox
    participant M as IBM MQ
    participant W as Consumer
    participant C as Core autoritatif
    U->>A: POST ordre 500 EUR / idempotencyKey stable
    A->>D: transaction locale ORDERS + OUTBOX
    D-->>A: Commit
    A--xU: réponse HTTP perdue
    D->>M: publication relay (peut être répétée)
    M->>W: livraison (peut être répétée)
    W->>C: demande avec référence métier immuable
    C-->>W: statut exact ou UNKNOWN
    U->>A: GET statut avec même référence
    A->>D: lire état connu / journal
    D-->>A: état suivi et source
    A-->>U: état non inventé
~~~

## 3. Architecture d'exploitation des 30 patterns
- **Build et admission** : Dockerfile multi-stage, runtime minimal, image à digest promue, SBOM/signature et UID arbitraire compatible SCC.
- **Configuration** : images identiques entre environnements, paramètres validés, Secrets gérés et renouvelés, ServiceAccount distincts.
- **Pods et controllers** : Deployments pour APIs sans état ; StatefulSets/Operators seulement lorsque le produit et la preuve de HA le nécessitent ; Jobs idempotents, init/sidecars à besoins explicites.
- **Readiness/liveness/startup** : probes distinctes, graceful shutdown, PDB encadrant évictions volontaires, topology spread et capacité réelle.
- **Scaling** : HPA et métriques adaptées, scale consommateurs sur queue depth/oldest-message-age, pas de saturation du core.
- **Réseau et sécurité** : DNS Services, Routes/TLS, NetworkPolicy ingress/egress, SCC, RBAC et identité machine mTLS.
- **GitOps / Day-2** : Argo CD drift, self-heal et prune paramétrés, RollingUpdate/Canary selon compatibilité ; des migrations SQL exigent des plans spécifiques.
- **Legacy / multi-site** : strangler progressif avec shadow read-only, bascule exclusive et reprise entre clusters sous fencing.

## 4. Six décisions Design Authority
| Décision | Arbitrage | Rejet / limite |
|---|---|---|
| Conteneur Java | Image minimale + UID arbitraire | Ne pas accorder privileged/anyuid pour compenser une image inadéquate |
| Stateful | StatefulSet uniquement si état et identité nécessaires | StatefulSet n'est pas une solution HA complète |
| Autoscaling | Dimensionner sur demande **et** capacité du core | HPA seul ne garantit aucun gain de débit |
| Livraison | Digest approuvé + Argo CD + readiness | GitOps ne rollback pas un règlement ou une migration SQL |
| Résilience | PDB + spread + probes + drain | Ne couvre pas toutes les pannes brutales |
| DR | Bascule GO/NO-GO et fencing vérifié | Deux clusters n'autorisent pas deux writers de la même référence |

## 5. Limite de preuve
Ceci est une architecture **documentaire**, sans connexion aux clusters CRC ou Kind de l'utilisateur et sans résultat de test runtime. L'acceptation nécessite exécution et collecte des preuves dans un laboratoire isolé.

[Programme](../README.md) · [Matrice des 30 preuves](matrice-tests-openshift-141-170.md)
