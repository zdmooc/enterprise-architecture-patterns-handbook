# Références — architectures d'IA et contrôles

**Cadre :** publications et projets ouverts ; aucune entreprise ni déploiement client n'est décrit. Ces ressources servent à comprendre et **ne remplacent pas** une validation de conception, de sécurité ou de réglementation.

## Gestion des risques et sécurité
- [NIST AI Risk Management Framework — Generative AI Profile (AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) : approche gouverner, cartographier, mesurer et gérer les risques.
- [OWASP — Top 10 for LLM Applications, édition 2025](https://genai.owasp.org/llm-top-10/) : prompt injection, informations sensibles, chaîne d'approvisionnement, empoisonnement, sorties dangereuses, autonomie excessive, faiblesses vecteurs/embeddings, désinformation et consommation sans bornes.
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) : sécurité des APIs utilisées par les agents.

## Kubernetes / OpenShift et inférence
- [Kubernetes — Documentation concepts](https://kubernetes.io/docs/concepts/) : Services, Deployments, probes, scheduling, ressources, secrets, sécurité et réseau.
- [KServe — Generative Inference Autoscaling](https://kserve.github.io/website/docs/model-serving/generative-inference/autoscaling) : mise à l'échelle sur des métriques propres au LLM (requêtes en attente, KV cache, etc.) selon version/mode.
- [KServe — LLM Inference Service Configuration](https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/llmisvc-configuration) : différences entre modes, ressources, scheduler et autoscaling.
- [vLLM — Documentation déploiement Kubernetes](https://docs.vllm.ai/en/latest/deployment/k8s/) : exemple de moteur d'inférence ; compatibilité à vérifier selon installation.

## Patterns et méthodes
- [Saga / transactions distribuées](https://microservices.io/patterns/data/saga.html) pour les actions métiers multi-étapes.
- [Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html), pour émettre après validation durable.
- [Idempotent Consumer](https://microservices.io/patterns/communication-style/idempotent-consumer.html), pour limiter les effets de redélivrance.
- [Documentation des fichiers Mermaid](https://mermaid.js.org/syntax/flowchart.html) pour modifier les diagrammes.

## Limites et exigences de preuve
- Les noms des patterns IA ne constituent **pas tous des normes universelles** : ReAct est une stratégie agentique, Advanced RAG une famille de techniques, Guardrails des contrôles, etc.
- Pour une mise en production, enregistrer les versions des référentiels, de modèles, de prompts, de tests, de runtime et les conditions de support.
- Ne pas mettre en œuvre un outil de mutation financière à partir d'une seule sortie probabiliste.
- Toute démonstration par simulateur doit être étiquetée **preuve locale limitée** : elle n'établit pas la disponibilité ou la sécurité d'un système réel.
