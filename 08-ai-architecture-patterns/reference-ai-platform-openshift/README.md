# Architecture de référence — Plateforme IA d'entreprise sur Kubernetes / OpenShift

**Étude de conception fictive et anonymisée.** Projet pédagogique : assistant de consultation de procédures, assistance aux investigations et production de rapports sur incidents de paiement. **Aucune donnée de client réel, aucun ordre financier ni outil bancaire connecté.**

## 1. Objectif et principes

Proposer une plateforme IA où un collaborateur habilité peut :
- Poser des questions sur des procédures internes et obtenir une réponse sourcée ;
- Interroger **en lecture seule** le statut d'un dossier fictif via outil sécurisé ;
- Recevoir une suggestion d'investigation lors d'un événement technique ;
- Préparer une demande de modification, mais **jamais exécuter une opération sensible sans approbation indépendante et revalidation du système métier**.

### Invariants P0
| Code | Invariant | Preuve |
|---|---|---|
| AI-01 | Un document non autorisé ne figure jamais dans contexte ou réponse | Test ACL par rôle/tenant |
| AI-02 | Une instruction trouvée dans un document ne modifie pas les règles d'agent | Test prompt injection indirecte |
| AI-03 | Un outil ne s'exécute qu'après une politique serveur indépendante | Test allowlist + AuthZ métier |
| AI-04 | Une mutation sensible exige approbation spécifique, valide et non expirée | Hash de payload + approbation |
| AI-05 | Une même action approuvée ne produit pas deux effets après retry | Référence stable / idempotence |
| AI-06 | Les résultats IA sont des **hypothèses**, pas des preuves financières | Statuts séparés |
| AI-07 | La réponse documentée est accompagnée de passages autorisés ou d'abstention | Golden set de citations |
| AI-08 | Les données confidentielles ne quittent jamais leur périmètre autorisé | Test routage et fallback |
| AI-09 | Un événement redélivré n'engendre pas des diagnostics répétés sans contrôle | Inbox / eventId |
| AI-10 | Une mise à jour de modèle/index/prompt est bloquée en cas de régression critique | Evaluation gate |

## 2. Architecture globale

~~~mermaid
flowchart TB
    U["Collaborateur authentifié"]
    G["API / AI Gateway : IAM, quotas, politique"]
    ORC["Orchestrateur IA / session + budgets"]
    ROUTE["Model Router"]
    SVC["Model Serving local CPU/GPU"]
    RAG["RAG service : retrieval et post-ACL"]
    IDX[("Index vectoriel/lexical + métadonnées")]
    DOC[("Documents versionnés + ACL")]
    TOOLS["Tool broker : schémas + allowlist"]
    READ["API d'investigation READ-ONLY"]
    HITL["Workflow HITL + policy engine"]
    MUT["Outil sensible (désactivé par défaut)"]
    EVAL["Evaluation / sortie avec citations"]
    AUDIT[("Traces expurgées + audit + metrics")]
    BUS["Broker événements / Inbox"]
    WORK["Worker IA asynchrone"]
    U --> G --> ORC
    ORC --> RAG --> IDX
    DOC -->|"Ingestion contrôlée"| IDX
    ORC --> ROUTE --> SVC
    ORC --> TOOLS
    TOOLS --> READ
    TOOLS -. "Seulement avec approbation" .-> HITL
    HITL --> MUT
    RAG --> EVAL
    SVC --> EVAL
    READ --> EVAL
    EVAL --> U
    BUS --> WORK --> ORC
    G --> AUDIT
    ORC --> AUDIT
    SVC --> AUDIT
~~~

**Lecture :** les accès métiers ne sont **pas** accordés par la sortie du LLM. L'outillage est en lecture seule par défaut ; le workflow HITL n'expose la mutation qu'après décision indépendante. Les diagrammes sont logiques ; les relations ne constituent pas toutes des connexions synchrones. L'agent et les consumers sont **hors chemin du règlement financier**.

## 3. Architecture applicative et responsabilité des données

| Composant | Fonction | État durable | Restriction majeure |
|---|---|---|---|
| API Gateway | Exposition API et auth du client | Journaux contrôlés | Pas d'outils métier directs |
| AI Gateway | Accès aux modèles, routage, quotas et consommation | Compteurs/version | Ne remplace pas AuthZ métier |
| Orchestrateur | Réponses, budgets, traces, plans | État de session/plan si nécessaire | Pas de droit implicite |
| RAG Service | Retrieval, ACL, ranking, citations | Index et métadonnées versionnés | Documents restent non fiables |
| Model Serving | Inférence (CPU/GPU) | Poids immuables + runtime | Pas de mutation financière |
| Tool Broker | Validation des appels d'outil | Journal d'autorisation | Strict allowlist / schémas |
| HITL Workflow | Demande, approbation, expiration | ApprovalRequest immutable | Revalidate action |
| Evaluation | Qualité, citations, sécurité, drift | Datasets et verdicts | Ne doit pas inventer les faits |
| Event Worker | Reçoit events techniques + résume | Inbox + rapports | Redélivrance idempotente |
| Observabilité | Latence, erreur, coût, provenance | Traces expurgées | Pas de corpus ou IBAN complets |

### Données et frontières de confiance
1. Les documents d'entreprise sont classifiés, versionnés, soumis à ACL et règles de conservation.
2. L'index vectoriel hérite des mêmes contraintes que le document source : un fragment n'est pas public parce qu'il est dans l'index.
3. Les résultats d'outils et textes des documents sont du **contenu non fiable** du point de vue des instructions.
4. Le modèle a seulement le pouvoir de **proposer un appel**, jamais d'augmenter un droit.
5. Le système bancaire source reste propriétaire des états/écritures. L'IA ne publie pas de « règlement confirmé » depuis une supposition.

## 4. Parcours synchrones et asynchrones

- **RAG / question-réponse** : client → Gateway → policy → ACL retrieval → modèle → validation des citations → réponse.
- **Tool Calling READ-ONLY** : client → agent → schéma → AuthZ serveur → API métier → observation → synthèse.
- **HITL** : plan immuable → ApprovalRequest persistée → approbateur autorisé → revalidation → action idempotente → lecture du résultat.
- **Event-Driven AI** : événement technique durable → Inbox → Worker IA → rapport sourcé → expert ; la panne IA n'arrête pas les paiements.
- **Fallback** : erreur d'inférence → décision de routage compatible résidence/classification → modèle approuvé ou réponse d'indisponibilité.

Les [séquences illustrées](sequences.md) montrent ces parcours avec les points de sécurité.

## 5. Modèles et inférence : CPU, GPU, capacité

### Trois modes de travail
- **Mode local CPU pédagogique** : petit modèle ou simulateur, sans promesse de latence ni de qualité production.
- **Mode local GPU production candidate** : sizing mémoire des poids, KV cache et batch, compatibilité OpenShift/drivers/accélérateurs et coûts.
- **Mode inférence externalisée autorisée** : uniquement si la classification et les politiques de résidence et de traitements l'autorisent, avec contrats et mécanismes de sécurité validés.

### Model Serving
- Registre immuable des modèles : version, provenance, licences, checksum, type de tâche, tests de sécurité.
- Contrat de réponse : synchrone et/ou streaming, usage de tokens, version du modèle, erreurs normalisées.
- SLO à négocier : disponibilité, **TTFT** (time to first token), latence p95/p99, taux d'échec, coût/tokens et throughput.
- Mesures capacité : queue depth, in-flight requests, GPU memory, KV cache, tokens/sec ; CPU seul peut être un signal insuffisant.
- Scaling : HPA/KEDA suivant architecture et version des contrôleurs ; maintenir capacité chaude si cold start incompatible avec SLO.

## 6. Déploiement Kubernetes / OpenShift

### Namespaces logiques proposés
~~~mermaid
flowchart TB
    subgraph Edge["ai-edge"]
      G["AI/API Gateways + route"]
    end
    subgraph App["ai-workflows"]
      A["Orchestrator / Policy / Tools / HITL"]
      E["Evaluation workers"]
    end
    subgraph Data["ai-data"]
      D[("Documents ACL / index / journaux")]
    end
    subgraph Inference["ai-inference"]
      M["Model Serving CPU/GPU"]
    end
    G --> A
    A --> D
    A --> M
    A --> E
~~~
Les namespaces n'isolent réellement les flux qu'avec politiques réseau, identités et permissions. Les composants stateful peuvent vivre hors du cluster selon exigences.

### Contrôles de plateforme
- **Isolation réseau** : NetworkPolicy default-deny, autoriser précisément HTTP/gRPC entre pods, DB/index et egress vers ressources approuvées.
- **Identité** : ServiceAccount par service, RBAC minimal, mTLS/TLS selon contrats, tokens courts et renouvellement des certificats.
- **Supply chain** : images et modèles provenant de registres approuvés, scans, SBOM, signatures et politiques d'admission.
- **Secrets** : externalisation, rotation, aucun token dans images, YAML publics ou corps de traces.
- **GPU** : quotas, scheduling par accélérateur, réservation mémoire et isolation multi-tenant selon support.
- **Sondes** : startupProbe pour chargement lourd ; readiness seulement quand le modèle est réellement opérationnel ; liveness sans redémarrer pour une panne d'index amont.
- **Scalabilité** : modèle, routeur et outils mis à l'échelle selon saturation réelle ; quotas de charge et de coût.
- **GitOps** : versions de manifestes et politiques, déploiements progressifs ; tests de migration de schéma et d'index.
- **HA/DR** : conserver indices/documents/approbations durables ; reconstruire un index depuis sources autoritatives si nécessaire.

## 7. Observabilité, sécurité et LLMOps

### Signaux minimaux
| Famille | Indicateurs / traces |
|---|---|
| RAG | retrieval recall@k sur jeu de référence, citations correctes, autorisations, fraîcheur index |
| Modèle | TTFT, tokens/s, queue depth, in-flight, timeouts, erreurs, version |
| Agent | outil demandé/exécuté/refusé, étapes, timeouts, coût, appels invalides |
| HITL | durée d'attente, expiration, approbation, mutation réellement effectuée |
| Sécurité | tentatives injection/exfiltration, violations ACL détectées, secrets masqués |
| EDA | event lag, duplicate suppressed, DLQ, âge des rapports |
| Exploitation | saturation CPU/GPU, mémoire, stockage, erreurs DB, coût par réponse |

### LLMOps = gestion des versions combinées
Versionner ensemble modèles, prompts, embeddings, corpus, index, code d'outils, schémas et policies. Toute modification significative déclenche les **tests offline + sécurité + canary**. Un taux de satisfaction seul ne prouve ni absence de fuite ni fidélité aux procédures.

## 8. Comportement en panne

| Panne | Stratégie |
|---|---|
| Index documentaire indisponible | Abstention documentée, pas de réponse inventée |
| Document supprimé mais encore dans index | Révocation et re-indexation prioritaire, blocage ACL côté retrieval |
| Modèle principal indisponible | Fallback autorisé ou erreur, sans fuite de données |
| Modèle retourne une instruction tool non autorisée | Refus déterministe, audit, pas d'exécution |
| Workflow d'approbation en panne | Aucune mutation ; demande en attente/reprise |
| Outil de mutation timeout après exécution possible | QueryStatus + référence stable ; pas de retry naïf |
| Broker redélivre un incident | Inbox événementiel et rapport logique unique |
| Perte de GPU | Rétablir replicas/modèle approuvé ou dégradation claire |
| Modification de prompt cause régression | Evaluation gate + rollback |

## 9. Gouvernance des décisions

- **ADR-AI-01** : classification et accès au corpus avant recherche.
- **ADR-AI-02** : modèles locaux prioritaires pour données classifiées, alternatives sous politique.
- **ADR-AI-03** : outils read-only par défaut ; tout outil sensible géré via HITL.
- **ADR-AI-04** : source financière distincte des sorties d'IA.
- **ADR-AI-05** : prompts/modèles/index évalués en continu avec critères bloquants.
- **ADR-AI-06** : événements d'incident asynchrones avec idempotence et aucune dépendance du règlement au LLM.
- **ADR-AI-07** : scaling et fallback conditionnés par SLO, budget, sûreté et capacités hardware réelles.

Ces ADR sont **proposées**, pas approuvées par une entreprise.

## 10. Qualification préalable à production

1. Passer [la matrice de tests et d'incidents](risks-and-tests.md) sans violation P0.
2. Définir classification/corpus, IAM, rétention et preuve de suppression.
3. Valider un jeu de référence métier avec experts indépendants.
4. Mesurer p95/p99 et charge avec les modèles **réellement** prévus.
5. Injecter prompt injection, fuite inter-tenant, outil non autorisé, crash du modèle et broker indisponible.
6. Vérifier DR des workflows persistants et des validations HITL.
7. Signer sécurité, architecture, données, risques, exploitation et responsabilités.

**Conclusion :** une plateforme IA d'entreprise robuste n'est pas une collection de Pods contenant un LLM. Elle repose sur des **frontières de confiance contrôlées, une source de vérité externe au modèle et des preuves de qualité, de résilience et de sécurité**.

**Copyright © 2026 Zidane Djamal. Tous droits réservés.**
