# 12 — Model Serving : inférence fiable sur Kubernetes/OpenShift

> **Famille :** Production / MLOps · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

## 1. Définition et besoin

Pattern d'exposition d'un modèle par une API de prédiction/inférence, avec version de modèle, isolation, ressources CPU/GPU, observabilité, sécurité, mise à l'échelle et reprise. Model Serving n'est pas la phase d'entraînement.

**Problème :** Une application souhaite invoquer un LLM interne 24/7, mais le modèle consomme mémoire et accélérateurs ; une montée de charge peut saturer la file et allonger le temps au premier token.

## 2. Architecture logique

~~~mermaid
flowchart TB
 A["App IA"] --> GW["AI Gateway"]
 GW --> LB["Inference Service"]
 LB --> P1["Pod inference 1, GPU/CPU"]
 LB --> P2["Pod inference 2, GPU/CPU"]
 REG["Registry modèles immuables"] --> P1
 REG --> P2
 MET["Metrics : tokens/s, TTFT, queue"] --> HPA["Autoscaler HPA / KEDA"]
 P1 --> MET
 P2 --> MET
 HPA -.-> LB
~~~

### Déroulement

1. Publier artefact modèle immuable, provenance, licence, checksum et politique de données.
2. Établir image/serveur d'inférence et contrat de réponse (synchrone, streaming, batch).
3. Planifier Pods selon CPU/GPU, mémoire, stockage des poids, quantization éventuelle et compatibilité runtime.
4. Établir TLS/Service/Route selon exposition, identités et NetworkPolicies.
5. Mesurer queue depth, requêtes en vol, temps premier token, tokens/s et latences p95/p99.
6. Configurer readiness réelle, capacité chaude, autoscaling sur signaux adaptés, rollout/rollback et DR.

## 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
 participant G as AI Gateway
 participant S as Model Serving
 participant K as Scheduling Kubernetes
 participant M as Pod inférence
 G->>S: Générer réponse modèle v3
 S->>K: Pod disponible / admission
 K-->>S: Ressource prête
 S->>M: Tokens demandés
 M-->>G: Flux tokens + résultat
 M-->>S: TTFT, débit, latence
 S-->>G: Usage et version
~~~

**Exemple pratique :** Un modèle local d'assistance documentaire est servi par 2 instances si la capacité le permet. Sur machine d'apprentissage sans GPU, la même chaîne peut fonctionner lentement en CPU à faible débit ; **ne pas présenter un POC CPU comme preuve de SLO production**.

## 4. Décisions d'architecture

- Serving via Deployment standard ou contrôleur d'inférence qualifié (KServe, si compatible).
- Demande ressources CPU/GPU, quantization, mémoire KV cache, scheduling et isolation des accélérateurs.
- Scale-to-zero seulement si cold start est compatible avec SLO ; souvent maintenir des réplicas chauds.
- Évaluer batching, longueur de contexte, flux streaming, limite de concurrence et fairness.
- Gestion versions modèles : provenance, canary, rollback, changement de tokenizer/prompt et droit de licence.

## 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| GPU saturé et temps premier token élevé | Admission, quotas, file bornée, scaling selon métriques inférence. |
| Pod prêt mais modèle non chargé | Readiness ne passe qu'après chargement et test minimal. |
| Téléchargement artefact compromis | Poids vérifiés, registry approuvé, contrôle de provenance. |
| Scaling sur CPU seul inefficace | Mesurer KV cache/queue/running, pas seulement CPU. |
| Panne d'accélérateur | Routage vers réplicas prêts, fallback autorisé. |

## 6. Tests et preuves attendues

1. Rolling update du modèle sans réponse mixte non maîtrisée.
2. Charge constante avec p95/p99 mesuré.
3. Cold start et eviction GPU simulés.
4. Refus des modèles non signés/non approuvés.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

## 7. Compromis et critères de choix

Cœur plateforme requis pour héberger des modèles en production, mais il ne garantit ni qualité de contenu ni sécurité des actions.

## 8. Question d'entretien

**Question :** Quels indicateurs spécifiques LLM utiliser pour scaler ?

**Réponse :** En plus CPU/GPU/mémoire, mesurer nombre de requêtes en attente/en cours, utilisation du KV cache, TTFT et débit de tokens.

## 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice](../PATTERNS_DECISION_MATRIX.md) · [Sources](../REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.
