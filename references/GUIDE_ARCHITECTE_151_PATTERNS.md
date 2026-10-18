# Guide d'architecte senior — choisir parmi 151 patterns

**Version V3 — 18 octobre 2026.** Référentiel de conception générique et **totalement fictif**. Il ne représente aucune organisation réelle ni réalisation en production. Les 151 fiches se répartissent en 10 patterns d'intégration, 15 d'IA, 30 Kubernetes/OpenShift, et 96 nouveaux patterns d'architecture d'entreprise, applicative, données, résilience, sécurité, cloud, SRE et modernisation.

## 1. De la stratégie métier à la décision technique

~~~mermaid
flowchart TB
  M["Stratégie et capacités métier"] --> E["Enterprise Architecture : domaines, AS-IS, TO-BE, roadmap"]
  E --> S["Solution Architecture : exigences, NFR, arbitrages"]
  S --> A["Application : modules, DDD, transactions"]
  S --> I["Intégration : API, messages, ACL, événements"]
  S --> D["Data : ownership, contrats, CDC, analytics"]
  S --> T["Technique : IAM, réseau, compute, stockage"]
  T --> R["Résilience : quorum, PRA, RPO/RTO"]
  R --> O["SRE : SLO, incidents, preuves et coûts"]
~~~

**Principe fondamental :** un pattern constitue une réponse à des forces contradictoires clairement identifiées ; il n'est pas un produit à déployer ni une certification de disponibilité.

## 2. Quel rôle utilise quels patterns ?

| Fonction | Questions prioritaires | Familles à ouvrir |
|---|---|---|
| Architecte d'entreprise | Quelles capacités créer, conserver, transformer ? Qui possède les données ? Quelles vagues ? | [Entreprise](../10-enterprise-architecture-patterns/README.md), [Data](../12-data-architecture-patterns/README.md), [Cloud hybride](../15-cloud-hybrid-architecture-patterns/README.md) |
| Architecte solutions | Quelle combinaison fonctionnelle et technique répond aux NFR, risques et coûts ? | [Applicative](../11-application-software-patterns/README.md), [Intégration](../01-integration-patterns/01-request-response/README.md), [Sécurité](../14-security-zero-trust-patterns/README.md) |
| Architecte applicatif | Où sont invariants, frontières de domaine, transaction et données ? | [Applicative](../11-application-software-patterns/README.md), [Data](../12-data-architecture-patterns/README.md) |
| Architecte intégration | Synchrone ou async ? Commande ou événement ? Déduplication et états ? | [Intégration](../01-integration-patterns/01-request-response/README.md), [Résilience](../13-resilience-distributed-systems-patterns/README.md) |
| Architecte technique / plateforme | Quel runtime, network, storage, IAM, déploiement et opération ? | [Kubernetes/OpenShift](../09-containerization-kubernetes-openshift-patterns/README.md), [Cloud hybride](../15-cloud-hybrid-architecture-patterns/README.md), [Sécurité](../14-security-zero-trust-patterns/README.md) |
| Architecte résilience | Quelles pannes tolérer, quel ownership, quelle preuve de commit, quelles décisions de PRA ? | [Résilience](../13-resilience-distributed-systems-patterns/README.md), [Performance/SRE](../16-performance-sre-patterns/README.md) |
| Architecte IA | Quels modèles, retrieval, permissions d'outils, évaluation et hosting ? | [IA](../08-ai-architecture-patterns/README.md), [Sécurité](../14-security-zero-trust-patterns/README.md), [Plateforme](../09-containerization-kubernetes-openshift-patterns/README.md) |

## 3. Exemple de conception complet — système de dossiers fictif

**Besoin :** moderniser l'accès aux dossiers, centraliser l'information pertinente et traiter les investigations, sans modifier un système d'écriture autoritatif historique sans preuve.

**Existants hypothétiques :** portail, serveur Java/JEE, base relationnelle, batch, service de messagerie, reporting ancien, runbooks et identité centralisée. Les chiffres, interfaces et noms sont fictifs.

~~~mermaid
flowchart TB
  USER["Canaux autorisés"] --> GW["Gateway et identité"]
  GW --> APP["API Dossiers : modules applicatifs Java"]
  APP --> AC["ACL / intégration contrôlée"]
  AC --> CORE["Système historique autoritatif"]
  APP --> DB[("État opérationnel + Outbox")]
  DB --> EVT["Messages / événements versionnés"]
  EVT --> BI["Data products + analyse"]
  EVT --> AI["Assistance IA investigations (non autoritative)"]
  BI --> OBS["Observabilité / SLO"]
  AI --> OBS
  APP --> OBS
  PLAT["Plateforme Cloud Native / GitOps"] -.-> APP
  SEC["Zero Trust / IAM / politiques / sécurité des secrets"] -.-> GW
  SEC -.-> APP
  DR["PRA / backups / quorum / fencing"] -.-> DB
~~~

**Décisions candidates :**
1. Urbaniser par domaines et capabilities, cartographier les flux existants et choisir une première capacité à faible risque.
2. Conserver temporairement le système autoritatif ; ne pas déplacer le ledger ou une source de vérité sans contrat.
3. Utiliser un monolithe modulaire / architecture hexagonale lorsque les besoins de scaling indépendant ne sont pas démontrés.
4. Préférer un transport de commandes durable et des références stables pour les opérations ayant des effets ; events distincts pour le reporting.
5. Contrôler les données analytiques par contrats et provenance ; ne pas utiliser une projection stale pour décider d'une mutation.
6. Mettre IAM, autorisation de dossier, secrets, network policies et audit séparément du chiffrement transport.
7. Déployer sur un runtime OpenShift compatible, image non-root, GitOps et sondes ; tester SIGTERM et messages redélivrés.
8. Définir RPO/RTO selon BIA, preuve de fencing et des commits reconnus avant toute bascule multisite.
9. Consommer les événements dans une IA d'investigation **sans** lui attribuer l'exécution financière ; HITL pour toute action sensible.
10. Qualifier latence p99, charge, budget d'erreur, coûts et rollback sous données en vol.

## 4. Les compromis à argumenter à l'entretien

| Arbitrage | Question qui tranche | Risque d'un choix automatique |
|---|---|---|
| Monolithe modulaire / microservices | Besoin réel d'isolation, ownership, cadence de release ? | Transactions distribuées inutiles et latence |
| REST / queue | Réponse immédiate exigée ou travail différable ? | Timeout ambigu et doublons |
| Kafka / MQ / broker unique | Rejeu long, abonnés et contrats legacy réellement requis ? | Double coût/complexité |
| SQL OLTP / lakehouse | Transaction autoritative ou analyse de volumes ? | Décision de débit fondée sur projection |
| RAG / outil live | Fait documentaire ou statut actuel de dossier ? | Document périmé pris pour donnée actuelle |
| Active-passive / actif-actif partitionné | RPO, latency WAN, ownership et fencing prouvés ? | Split-brain et perte des commits |
| HPA / quota | Où se situe le goulot mesuré, dans API ou core ? | Multiplication des connexions et saturation |
| Rehost / replatform / refactor / replace | Support, coûts, contrats, objectifs métier ? | Refonte sans bénéfice ni chemin de retour |

## 5. Séquence de diagnostic incident sans inventer un état

~~~mermaid
sequenceDiagram
  actor U as Utilisateur autorisé
  participant A as API moderne
  participant D as Journal et Outbox
  participant C as Système autoritatif
  participant R as Réconciliation
  U->>A: Mise à jour dossier, référence stable
  A->>D: Enregistrer intention et commande
  D->>C: Action autorisée et idempotente
  C--xD: Réponse perdue
  A-->>U: Issue non confirmée
  R->>C: QueryStatus(même référence)
  C-->>R: Résultat attesté / inconnu
  R->>D: Transition uniquement sur preuve
  A-->>U: Statut corrigé, jamais imaginé
~~~

## 6. Méthode systématique pour rédiger une ADR

Un dossier de décision défendable possède **besoin, options, risques, coûts, contraintes, propriétaire, invariant, test, résultats, dérogations et échéance de revue**. Les valeurs d'exemple (TPS, temps de bascule, disponibilité) restent des hypothèses tant qu'aucun test ne les vérifie.

Critères minimaux :
- Décision **métier** et responsabilité des données acceptées ;
- Architecture logique, schémas d'intégration et conventions de statut explicités ;
- Contrat d'accès, identité et habilitation confirmés ;
- Charge, panne et reprise démontrées au périmètre pertinent ;
- Procédures d'incident et plan de sortie opérationnels ;
- Support/licences, budget et compétences disponibles ;
- Absence de double traitement sur effets critiques.

## 7. Parcours d'étude progressif

Commencer par les **12 fiches d'urbanisation**, continuer avec les **15 patterns applicatifs** et **12 données**, puis approfondir **résilience (15)** et **sécurité (12)**. Terminer avec **cloud hybride (10)**, **SRE (10)** et **modernisation (10)**. Croiser à chaque étape avec les patterns d'intégration (10), IA (15) et Kubernetes/OpenShift (30) existants.

**Limites :** il s'agit de fiches de méthode et de conception. Aucun diagramme ou exemple ne prouve des réalisations sur une infrastructure cliente.
