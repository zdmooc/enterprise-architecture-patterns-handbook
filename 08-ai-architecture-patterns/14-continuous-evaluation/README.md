# 14 — Continuous Evaluation / LLMOps

> **Famille :** Production / MLOps · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

## 1. Définition et besoin

Évaluer les applications IA avant mise en production et continuellement après chaque changement de modèle, prompt, index, outil ou politique. On distingue qualité offline sur jeu de référence, tests de sécurité et métriques online.

**Problème :** Un changement d'embedding ou de modèle améliore les réponses génériques mais dégrade l'exactitude de procédures techniques et augmente la proportion de citations non pertinentes.

## 2. Architecture logique

~~~mermaid
flowchart TB
 DATA["Jeu de référence versionné"] --> TEST["Évaluations offline : RAG, qualité, sécurité"]
 CAND["Nouvelle version modèle/prompt/index"] --> TEST
 TEST --> GATE{"Seuils qualité / risque satisfaits ?"}
 GATE -->|Non| FIX["Correction / abandon"]
 GATE -->|Oui| CAN["Canary / shadow"]
 CAN --> OBS["Observabilité + audit des réponses"]
 OBS --> REV["Revue et boucle d'amélioration"]
 REV --> DATA
~~~

### Déroulement

1. Créer un jeu de référence versionné : questions, réponses attendues, passages probants et permissions.
2. Mesurer offline retrieval (recall@k), fidélité aux sources, qualité métier, abstentions justifiées et schémas.
3. Tester sécurité/adversarial : prompt injection, exfiltration, données hors périmètre, tool misuse.
4. Déployer en environnement de qualification/shadow, puis canary selon profil de risque.
5. Surveiller online latence, tokens, coûts, retours utilisateurs, drift des requêtes et erreurs de citations.
6. Analyser les régressions ; rollback modèle/prompt/index et mise à jour contrôlée du jeu de référence.

## 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
 participant CI as Pipeline
 participant E as Eval offline
 participant P as Plateforme canary
 participant A as Architecte / Owner
 CI->>E: Candidate v4 + golden set
 E-->>CI: rappel@k, groundedness, attaque, latence
 CI->>A: Rapport et seuils
 A-->>CI: Approve canary
 CI->>P: Shadow / canary sans outil de mutation
 P-->>A: Résultats réels agrégés, anonymisés
 A-->>CI: Promote / rollback
~~~

**Exemple pratique :** Une mise à jour d'index change la procédure retrouvée pour « confirmation bancaire perdue ». Sur 100 questions fictives validées, on constate que certaines citations ne prouvent plus la conclusion. Le gate bloque le déploiement avant production.

## 4. Décisions d'architecture

- Jeu de référence représentatif, avec cas rares, langues et scénarios de refus.
- Critères objectifs séparant génération, retrieval, sécurité, coût et délai.
- Revue humaine échantillonnée et analyse du désaccord entre juges automatisés.
- Cohérence des versions modèle, embeddings, index, prompt, guardrail et data lineage.
- Définir qui approuve rollback, canary et modification de seuils.

## 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| Golden set trop simple | Inclure cas difficiles et adversariaux, stratifier par segment. |
| Judge LLM biaisé ou instable | Références humaines, calibration et règles déterministes. |
| Observations online contiennent PII | Agrégation/minimisation, consentements et rétention. |
| Mise à jour index sans réévaluation | Gate déclenché sur toute modification de corpus/schéma. |
| Régression de sécurité non détectée | Red-team continu et simulation de tool misuse. |

## 6. Tests et preuves attendues

1. Le pipeline refuse un score de fidélité sous seuil.
2. Retirer un document d'accès restreint ne provoque pas fuite.
3. Rétablir version antérieure du corpus et modèle possible.
4. Chaque sortie critique est associée à des références ou abstention.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

## 7. Compromis et critères de choix

Nécessaire pour fiabilité mesurée ; attention à la validité des métriques et au coût des évaluations.

## 8. Question d'entretien

**Question :** Peut-on évaluer uniquement le taux de réponses jugées utiles ?

**Réponse :** Non : mesurer également exactitude aux preuves, refus, permissions, latence/coût, robustesse et sécurité.

## 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice](../PATTERNS_DECISION_MATRIX.md) · [Sources](../REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.
