# 08 — AI Architecture Patterns : référentiel d'architecture IA

**15 patterns d'IA générative, agentique, sécurité et production**, illustrés par des systèmes documentaires fictifs et des déploiements Kubernetes/OpenShift.

> Ce référentiel est **entièrement pédagogique et anonymisé**. Aucun éditeur, entreprise, établissement bancaire, client, système interne ou réalisation de production n'est revendiqué. Les noms de standards et de technologies open-source désignent des outils ou des concepts, pas une affiliation.

## Parcours de formation

| N° | Pattern | Principe | Illustrations |
|---|---|---|---:|
| 01 | [RAG](01-rag/README.md) | Rechercher avant de répondre, citer les sources | 2 |
| 02 | [Advanced RAG](02-advanced-rag/README.md) | Hybrid retrieval et reranking | 2 |
| 03 | [Model Router](03-model-router/README.md) | Choisir modèle sous contraintes d'accès/coût/qualité | 2 |
| 04 | [Semantic Cache](04-semantic-cache/README.md) | Réutiliser une réponse seulement si contexte sûr | 2 |
| 05 | [ReAct / Tool Calling](05-react-tool-calling/README.md) | Appeler des outils sous politique indépendante | 2 |
| 06 | [Planner–Executor](06-planner-executor/README.md) | Séparer proposition et exécution | 2 |
| 07 | [Multi-Agent](07-multi-agent/README.md) | Collaboration spécialisée et arbitrage | 2 |
| 08 | [Reflection / Evaluator](08-reflection-evaluator/README.md) | Critique vérifiable et révision bornée | 2 |
| 09 | [Guardrails](09-guardrails/README.md) | Contrôles d'entrée, contexte, sortie et outils | 2 |
| 10 | [Human-in-the-Loop](10-human-in-the-loop/README.md) | Approbation humaine immuable sur actions sensibles | 2 |
| 11 | [AI Gateway](11-ai-gateway/README.md) | IAM, quotas, coûts, exposition des modèles | 2 |
| 12 | [Model Serving](12-model-serving/README.md) | Héberger et mettre à l'échelle une inférence | 2 |
| 13 | [Model Fallback](13-model-fallback/README.md) | Alternative autorisée ou dégradation explicite | 2 |
| 14 | [Continuous Evaluation](14-continuous-evaluation/README.md) | Gérer qualité, drift, sécurité et versions | 2 |
| 15 | [Event-Driven AI](15-event-driven-ai/README.md) | Réagir aux événements sans piloter les effets financiers | 2 |

**30 schémas Mermaid** dans les fiches, avec séquences, scénarios de pannes, exemples, arbitrages, tests et questions d'entretien.

## Construire une plateforme complète

- [Architecture de référence IA sur Kubernetes/OpenShift](reference-ai-platform-openshift/README.md).
- [Séquences des cas principaux](reference-ai-platform-openshift/sequences.md) : RAG, agent en lecture, approbation humaine, IA événementielle et panne.
- [Risques et tests de qualification](reference-ai-platform-openshift/risks-and-tests.md).
- [Matrice de sélection des patterns](PATTERNS_DECISION_MATRIX.md).
- [Références ouvertes et méthodologie](REFERENCES.md).
- [Laboratoire Python sans modèle externe](../labs/ai-rag-guardrails/README.md), pour expérimenter le contrôle d'accès et l'outil d'action sous approbation.

## Comment étudier un pattern ?

1. Identifier son **problème précis** et les invariants métier.
2. Dessiner le chemin nominal, puis **deux pannes**.
3. Séparer modèle probabiliste, **décisions de sécurité déterministes** et effets métier autoritatifs.
4. Définir API/outils, idempotency-key, limites de budget, preuves et tests.
5. Réaliser un prototype puis mesurer qualité/latence/coût/sécurité.
6. Comparer à une solution **plus simple** : pas de multi-agent si un RAG suffit.

### Architecture fil conducteur

~~~mermaid
flowchart TB
    U["Collaborateur habilité"] --> G["AI Gateway : IAM, quotas, data policy"]
    G --> A["Orchestrateur IA"]
    A --> R["RAG + ACL documents"]
    R --> V[("Index documentaire")]
    A --> MR["Model Router"]
    MR --> M["Model Serving local"]
    A --> T{"Outil métier ?"}
    T -->|Lecture autorisée| READ["API de consultation"]
    T -->|Mutation sensible| H["Approbation humaine + Policy Engine"]
    H --> WRITE["API métier idempotente"]
    M --> E["Évaluation + règles de sortie"]
    READ --> E
    WRITE --> E
    E --> OUT["Réponse sourcée ou abstention"]
~~~

**Règles transversales :** une source RAG peut contenir une injection ; un LLM peut se tromper ; une approbation humaine doit être liée à des paramètres immuables ; aucun résultat d'IA ne peut se substituer à l'état d'un système transactionnel.
