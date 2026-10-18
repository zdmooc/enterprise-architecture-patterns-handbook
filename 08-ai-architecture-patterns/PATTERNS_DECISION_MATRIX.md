# Matrice de décision — Architecture IA

| Besoin | Choix minimal | Renforcement si justifié | Faux raccourci à éviter |
|---|---|---|---|
| Répondre sur documents internes versionnés | RAG | Advanced RAG + citation checking | Considérer le LLM comme vérité documentaire |
| Trouver une procédure malgré acronymes/variantes | Advanced RAG | Hybrid search et reranking | Ne faire que augmenter top-k |
| Plusieurs modèles/classes de données | Model Router | AI Gateway et évaluations par tâche | Envoyer document interne vers modèle non autorisé |
| FAQ publique répétée | Semantic Cache | TTL+version corpus | Partager cache de statut personnalisé |
| Consulter données actuelles en lecture | Tool Calling | Planner–Executor si multi-étapes | Donner permissions de mutation à l'agent |
| Workflow long contrôlé | Planner–Executor | HITL et état durable | Laisser le planner accorder des droits |
| Expertise concurrente utile | Multi-Agent | Evaluator avec provenance | Multiplier agents sans baseline |
| Réponse à fort enjeu métier | Evaluator + références | Human review | Prendre jugement LLM pour preuve |
| Données et outils sensibles | Guardrails + IAM/AuthZ | DLP, policy engine, red-team | Sécuriser par prompt seulement |
| Validation d'action irréversible | HITL | Multi-approbation si politique l'impose | Approbation vague ou non liée au payload |
| Plusieurs applications modèles | AI Gateway | Model Router et quotas | Confondre avec API Gateway métier |
| Inférence locale opérationnelle | Model Serving | Autoscale inférence / HA GPU | HPA CPU seul sans mesure des requêtes |
| Panne modèle principal | Model Fallback | Dégradation contrôlée | Basculer dans une zone interdite |
| Nouvelle version modèle/index/prompt | Continuous Evaluation | Canary, rollback, drift | Mesurer seulement satisfaction utilisateur |
| Agir à réception d'événements | Event-Driven AI | Idempotent Consumer, DLQ et RAG | Confondre diagnostic avec règlement bancaire |

## Arbre de choix simplifié

~~~mermaid
flowchart TD
    Q{"Information documentaire ?"} -->|Oui| R["RAG + ACL"]
    Q -->|Non| A{"Données live ou outil ?"}
    A -->|Oui| T["Tool Calling, Policy Engine"]
    A -->|Non| M["Réponse modèle simple"]
    T --> X{"Mutation sensible ?"}
    X -->|Oui| H["HITL + action idempotente"]
    X -->|Non| RD["Lecture contrôlée"]
    R --> E["Evaluation + Guardrails"]
    M --> E
    H --> E
    RD --> E
~~~

**Le pattern est un outil de conception, pas une garantie de sécurité.** Le modèle peut produire une suggestion, seul le service métier peut autoriser et constater un effet financier.

## Critères standard de revue
- **Confiance** : sources, version corpus, références et abstention.
- **Contrôle** : identité, ACL, tool allowlist, HITL, protocole de mutation.
- **Qualité** : golden set, récupération, fidélité, erreurs et dérive.
- **Run** : p95/p99, tokens/s, TTFT, saturation, coût, quota et continuité.
- **Preuve** : incidents, jeux d'essais, runbooks, ADR signées.
