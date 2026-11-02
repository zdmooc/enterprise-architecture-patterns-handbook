# Architecture de référence — IA / agentique sur OpenShift · cours 171–185

> **Illustration pédagogique, non déployée dans ce parcours.** Cas : consultation des procédures de paiement et aide à l'investigation d'un ordre fictif de 500 EUR. Aucun modèle connecté au compte, aucun ordre bancaire exécuté.

## 1. Architecture logique de la plateforme
~~~mermaid
flowchart LR
    USER["Collaborateur habilité"] --> AUTH["OIDC / identité utilisateur"]
    AUTH --> GW["AI Gateway : IAM, quotas, classification"]
    GW --> ORCH["Orchestrateur IA / budgets"]
    ORCH --> RAG["RAG : ACL + hybride + rerank"]
    DOCS["Documents versionnés et classifiés"] --> ING["Indexation sous droits / provenance"]
    ING --> INDEX[("Index vectoriel / lexical")]
    RAG --> INDEX
    ORCH --> ROUTER["Model Router / policy"]
    ROUTER --> SERVE["Model Serving sur OpenShift"]
    ORCH --> TOOLS["Tool Gateway : schémas et autorisations"]
    TOOLS --> READ["API statut en lecture seule"]
    TOOLS --> HITL["Workflow approbation si action sensible"]
    HITL --> POLICY["Policy Engine / revalidation"]
    POLICY -. "uniquement si contrat et autorité métier" .-> DOMAIN["Service métier autoritatif"]
    ORCH --> EVAL["Guardrails + évaluateur"]
    EVAL --> OUT["Réponse sourcée ou abstention"]
    DOMAIN --> EVENTS["Outbox / broker"]
    EVENTS --> WORKER["Worker Event-Driven AI / Inbox"]
    WORKER --> ORCH
~~~

Les flèches indiquent les responsabilités : elles ne prouvent ni qu'un outil réel est connecté ni qu'une plateforme IA a été installée.

## 2. Séquence RAG + outil en lecture seule
~~~mermaid
sequenceDiagram
    actor U as Analyste
    participant G as AI Gateway
    participant O as Orchestrateur IA
    participant R as RAG sous ACL
    participant T as API métier en lecture
    participant L as Model Serving
    U->>G: Quelle procédure pour un ordre UNKNOWN ?
    G->>O: identité, tenant, budget et politique
    O->>R: retrouver procédures autorisées
    R-->>O: fragments sourcés et datés
    O->>T: getPaymentStatus(ref) si autorisé
    T-->>O: UNKNOWN + référence et statut exact
    O->>L: question avec sources non fiables délimitées
    L-->>O: proposition de réponse
    O->>O: guardrails, citations et règles de sortie
    O-->>U: procédure / abstention sans ordre émis
~~~

## 3. Human-in-the-Loop — autorité distincte
~~~mermaid
sequenceDiagram
    participant A as Agent
    participant W as Approbation durable
    actor H as Approbateur habilité
    participant S as API métier autoritative
    A->>W: proposer correction et hash payload
    W->>H: afficher paramètres exacts
    H-->>W: approval (hash, identité, expiry)
    W->>W: vérifier hash, état courant, SoD, droits
    alt approbation valide et action autorisée
        W->>S: commande avec clé d'idempotence
        S-->>W: statut exact / preuve / UNKNOWN
    else refus ou modification
        W-->>A: aucune action exécutée
    end
~~~

## 4. Gate de validation et exploitation
- **P0 — identité et confidentialité** : ACL documentaire et outil au backend, sans fuites inter-tenant.
- **P1 — qualité de preuve** : citations soutiennent les affirmations, abstention quand preuve absente.
- **P2 — contrôle d'agent** : tool allowlist, arguments typés, budgets, temps et pas d'escalade par document.
- **P3 — actions sensibles** : approval immuable, SoD, revalidation, idempotence à la frontière financière.
- **P4 — modèle/infra** : image/version digest, modèle autorisé par région, quotas CPU/GPU, monitoring tokens et coûts.
- **P5 — cycle de vie** : évaluation continue après changements de prompt, corpus, route, modèle et guardrails.
- **P6 — asynchrone** : événements authentifiés, consommateurs IA idempotents, absence de blocage du paiement et résultat de type analyse.

## 5. Choix d'architecture à défendre
| Décision | Option à privilégier sous conditions | Non-garantie |
|---|---|---|
| Recherche | RAG sous ACL, hybride si les évaluations le justifient | RAG ne supprime pas les hallucinations |
| Agent | Outils typés, lecture d'abord, approbation sur mutations | Un prompt n'accorde aucun droit |
| Modèles | Sélection et fallback par politiques d'accès et résidence | Disponibilité n'autorise pas une fuite |
| Serving | Modèle versionné et contrôles de capacité OpenShift | Pod Ready ne valide pas qualité |
| Événementiel | Inbox idempotente et analyse asynchrone | L'IA ne prouve jamais le règlement |

**Statut** : HLD de formation. Pour le laboratoire existant, consulter [le lab Python ACL / outils / HITL](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/tree/main/labs/ai-rag-guardrails) ; ce lab est offline, sans vrai LLM, ni embeddings, ni opérations bancaires.

[Retour aux cours](../README.md) · [Matrice de preuves](matrice-tests-ia-171-185.md)
