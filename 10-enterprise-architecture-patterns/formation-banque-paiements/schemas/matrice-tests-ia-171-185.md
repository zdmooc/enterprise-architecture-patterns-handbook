# Matrice de tests et preuves — Architecture IA, cours 171–185

> **Plan de tests à réaliser** : aucune preuve d'exécution ni résultat de laboratoire ne sont revendiqués par cette publication.

| Cours | Pattern | Propriété de sécurité/qualité | Injection reproductible | Preuve attendue |
|---:|---|---|---|---|
| 171 | [RAG — Retrieval-Augmented Generation](../171-rag.md) | Documents accessibles uniquement selon ACL, citations vérifiées ou abstention | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 172 | [Advanced RAG — Hybrid Search / Reranking](../172-advanced-rag.md) | Retrieval hybride, pertinence évaluée, filtrage ACL sans fuite | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 173 | [Model Router](../173-model-router.md) | Aucun modèle hors politique de classification et région | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 174 | [Semantic Cache](../174-semantic-cache.md) | Cache compatible avec tenant, version, droits et fraîcheur | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 175 | [ReAct / Tool Calling](../175-react-tool-calling.md) | Résultats d'outils non fiables et appels soumis à policy engine | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 176 | [Planner–Executor](../176-planner-executor.md) | Le plan ne confère aucun droit à l'exécution | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 177 | [Multi-Agent](../177-multi-agent.md) | Scopes séparés, coût/latence justifiés et synthèse traçable | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 178 | [Reflection / Evaluator](../178-reflection-evaluator.md) | Critique de réponse sans prétention de preuve financière | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 179 | [Guardrails](../179-guardrails.md) | Injection indirecte bloquée par des contrôles déterministes | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 180 | [Human-in-the-Loop](../180-human-in-the-loop.md) | Approbation liée au hash exact, autorisation et version état | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 181 | [AI Gateway](../181-ai-gateway.md) | Tenant, modèle, région, quotas et données sous politique | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 182 | [Model Serving](../182-model-serving.md) | Serving GPU/CPU disponible, IAM, version et qualité indépendants | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 183 | [Model Fallback](../183-model-fallback.md) | Pas de repli externe contraire à la confidentialité | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 184 | [Continuous Evaluation](../184-continuous-evaluation.md) | Release refusée si défaut bloquant de sécurité malgré note élevée | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |
| 185 | [Event-Driven AI](../185-event-driven-ai.md) | Consommateur idempotent : uniquement suggestion d'investigation, jamais règlement | Fausse donnée / droit retiré / panne contrôlée selon le cours | Contrat, version, logs expurgés, sortie attendue et résultat de test |

## Parcours de qualification pratique
1. **Corpus et ACL** : créer documents publics/privés, rôles A et B, suppression et révocation ; aucun passage non autorisé.
2. **Retrieval** : évaluer lexical, vectoriel, hybride et reranking avec des questions de référence en français.
3. **Prompts adversariaux** : texte externe qui demande d'ignorer les règles, usurpation d'outil, instructions masquées et documents obsolètes.
4. **Tool Calling** : essayer les API non listées, les arguments faux, l'objet d'un autre client, une réponse API hostile, 50 appels et un timeout.
5. **Human-in-the-Loop** : mutation sans approbation, changement de hash, compte approbateur interdit, approbation expirée, double action.
6. **Serving** : saturation CPU/GPU, cold start, échec d'image/digest, version différente et disponibilité de l'inférence.
7. **Routing / fallback** : modèle local indisponible et tentative d'envoi de données classifiées vers un fournisseur externe non autorisé.
8. **Évaluation continue** : jeux de référence, régression de citations, fuite d'ACL, drift, coûts, temps de réponse, tests CI bloquants.
9. **IA événementielle** : duplication du même eventId, worker down, backlog, schéma invalide, aucune publication PaymentSettled par l'IA.
10. **Revue Design Authority** : ADR, coûts d'inférence, provenance des sources, SLO, risque résiduel et GO/NO-GO.

## Grille de statut
| Niveau | Conditions |
|---|---|
| Documenté | Invariant, architecture et tests proposés |
| Simulé | Tests unitaires/laboratoire sur code fictif avec résultats |
| Démontré | Environnement et versions fixés, logs et métriques vérifiables |
| Accepté | Validation autorisée des risques résiduels et critères de qualité |

Un exemple Python sans vrai LLM ne constitue pas un test complet de qualité RAG ou de robustesse d'un modèle.

[HLD IA OpenShift](architecture-ia-openshift-171-185.md) · [Programme](../README.md) · [Cahier d'exercices](../exercices-et-corriges/cours-171-185.md)
