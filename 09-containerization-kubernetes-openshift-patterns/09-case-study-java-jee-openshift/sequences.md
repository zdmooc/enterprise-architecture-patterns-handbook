# Séquences d'architecture — Java/JEE vers OpenShift

## S1 — Build immuable et admission OpenShift
~~~mermaid
sequenceDiagram
  autonumber
  participant D as Développeur
  participant CI as CI / Security Gates
  participant R as Registry OCI
  participant G as GitOps
  participant K as OpenShift
  D->>CI: Commit code Java + Dockerfile multi-stage
  CI->>CI: Compiler / tester / scanner / SBOM / signer
  CI->>R: Push image identifiée par digest
  CI->>G: Proposer mise à jour de digest Git
  G->>K: Réconcilier les manifests approuvés
  K->>K: SCC, admission, pods startup/readiness
  K-->>D: Image et état observés
~~~

## S2 — Rolling Update sans supposer zéro downtime
~~~mermaid
sequenceDiagram
  participant K as Deployment Controller
  participant O as Replica existante
  participant N as Replica nouvelle
  participant S as Service
  K->>N: Créer Pod v2
  N->>N: Charger runtime Java et config
  N-->>K: Startup et readiness OK
  K->>S: Ajouter endpoint nouveau
  K->>O: Terminer Pod ancien (SIGTERM)
  O->>O: Refuser nouvelles tâches, drainer
  O-->>K: Exit gracieux / checkpoint
  K-->>S: Retirer endpoint ancien
~~~
La propagation d'endpoints, les requêtes en cours et SIGKILL exigent un test réel. Le diagramme est logique, pas un ordre strict garanti pour toutes les implémentations.

## S3 — Message traité, ACK perdu, Pod redémarré
~~~mermaid
sequenceDiagram
  participant Q as Queue de messages
  participant P as Worker Java Pod
  participant C as Core autoritatif
  Q->>P: Commande M-001
  P->>C: Traiter référence stable OP-001
  C-->>P: Effet enregistré
  Note over P: Crash avant ACK
  Q->>P: Redélivrer M-001
  P->>C: Vérifier référence OP-001
  C-->>P: Déjà traité : même preuve
  P-->>Q: ACK
~~~
**Transport durable ≠ exactement une fois métier**. La reprise est démontrée au système effectuant la transaction, non au Pod.

## S4 — Migration Strangler avec shadow read-only
~~~mermaid
sequenceDiagram
  actor U as Canal
  participant F as Façade d'intégration
  participant O as Ancien serveur Java/JEE
  participant N as Nouvelle API Java
  participant V as Comparateur de résultats
  U->>F: Consultation statut fictif
  F->>O: Lecture par chemin autoritatif
  O-->>F: Statut v1
  F-->>U: Réponse v1
  F->>N: Copie shadow READ-ONLY
  N-->>V: Résultat nouveau
  O-->>V: Résultat ancien
  V->>V: Comparer écarts, latence, décisions
~~~
**Jamais** dupliquer une commande de débit réel dans l'ancien et le nouveau moteur pendant un shadow test.

## S5 — Bascule de site contrôlée
~~~mermaid
sequenceDiagram
  participant A as Cluster site A
  participant D as Data/Quorum/Fencing
  participant B as Cluster site B
  participant C as Core financier
  A->>D: Dernier commit reconnu / writer epoch
  Note over A: Perte de site ou réseau
  B->>D: Demande promotion
  D-->>B: Bloqué tant que fencing/preuve incomplets
  B->>D: Ancien writer isolé ; comparer journaux
  D-->>B: Promotion autorisée selon runbook
  B->>C: Reconciliation in-flight avant réadmission
  C-->>B: Statuts réels
  B->>B: Réouvrir écritures sur partition autorisée
~~~
Une réplication async seule ne prouve pas le RPO 0. Un contrôle manuel peut être requis.
