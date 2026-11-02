# Cours 182 — Model Serving — Inférence sur Kubernetes/OpenShift · Architecture IA et agentique

> Banque fictive · ordre SEPA de 500 EUR. **Support pédagogique publié avec corrigé théorique ; aucun exercice individuel ni test sur cluster n'est déclaré validé.**

## 1. Besoin métier et problème
Une banque pédagogique souhaite servir un LLM local pour des documents classifiés avec maîtrise de l'accès, des versions et de la capacité GPU/CPU.

## 2. HLD : responsabilités des composants
~~~mermaid
flowchart LR
    A["API contrôlée / modèle et tokenizer"] --> B["Model Server + scheduler OpenShift"]
    B --> C["Réponse, métriques et traces"]
    B -. "Risque / absence de preuve" .-> STOP["Refus, attente ou abstention"]
~~~

**Décision d'architecture :** Versionner modèle, tokenizer et paramètres ; appliquer IAM, isolation des tenants, images signées, quotas GPU, readiness, warmup, batching adapté, limites de tokens, autoscaling et suivi de saturation. Mesurer performance et compatibilité du runtime.

**Invariant à défendre :** Un endpoint doit exposer uniquement le modèle approuvé et ne pas accepter une requête sans droits ni budget.

## 3. Contrat de contrôle
~~~text
serve = authorized && pinnedModelVersion && withinTokenBudget && capacityAvailable // métriques et timeouts explicites
~~~

Ce pseudo-code est conceptuel et ne constitue pas un composant d'IA ou un connecteur bancaire exécutable.

## 4. Séquence principale et incident
~~~mermaid
sequenceDiagram
    participant U as Analyste habilité
    participant P as AI Gateway et Policy Engine
    participant A as Composant IA
    participant R as Source ou modèle autorisé
    U->>P: demande et identité
    P->>A: contexte filtré + budget / version
    A->>R: traitement autorisé
    alt résultat valide
        R-->>A: preuves et données
        A-->>P: réponse sourcée ou proposition
        P-->>U: résultat clairement non autoritatif
    else panne, refus ou sortie incertaine
        R--xA: timeout / erreur
        A-->>P: refus, attente ou UNKNOWN
        P-->>U: abstention ou incident
    end
~~~

## 5. Sécurité, qualité et preuves de laboratoire
1. **Contrôle nominal :** mesurer la réussite d'une tâche à périmètre et modèle fixés.
2. **Attaque simulée :** Déployer un modèle au digest différent ou appel non authentifié : admission ou appel rejeté.
3. **Panne / non-régression :** Saturer le GPU, redémarrer un pod pendant inférence, tester cold start, délais, OOM, versions et bascule contrôlée.
4. **Reprise et confidentialité :** ne jamais interpréter une indisponibilité de l'IA comme un règlement rejeté ou réglé ; conserver la classification des données.
5. **Mesures à instrumenter :** tokens/s, time-to-first-token, p95/p99, GPU utilization, queue time, erreurs OOM, coût par 1000 tokens.
6. **Responsabilité métier :** toute opération sensible conserve une politique déterministe et, le cas échéant, une approbation humaine indépendante.

## 6. ADR et choix d'alternatives
Comparer la solution à une application déterministe, à un RAG sans agent et à un modèle local lorsque cela réduit le coût, la latence ou le risque. Documenter limites de contexte, budgets, risques indirects, versions, capacités OpenShift et stratégie de retrait.

## 7. Auto-évaluation corrigée
**Un pod Model Serving Ready garantit-il une réponse correcte et sûre ?**
- **A.** Oui, Ready signifie qualité métier validée.
- **B.** Non : disponibilité du serveur, qualité du modèle, autorisation et sécurité doivent être testées séparément.
- **C.** Oui si plusieurs GPU sont alloués.

**Bonne réponse théorique : B.** Non : disponibilité du serveur, qualité du modèle, autorisation et sécurité doivent être testées séparément.

Cette clé est un corrigé de cours, pas une validation individuelle.

## 8. Référence détaillée existante dans le dépôt
[Fiche source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/12-model-serving/README.md)

> **Famille :** Production / MLOps · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

#### 1. Définition et besoin

Pattern d'exposition d'un modèle par une API de prédiction/inférence, avec version de modèle, isolation, ressources CPU/GPU, observabilité, sécurité, mise à l'échelle et reprise. Model Serving n'est pas la phase d'entraînement.

**Problème :** Une application souhaite invoquer un LLM interne 24/7, mais le modèle consomme mémoire et accélérateurs ; une montée de charge peut saturer la file et allonger le temps au premier token.

#### 2. Architecture logique

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

#### Déroulement

1. Publier artefact modèle immuable, provenance, licence, checksum et politique de données.
2. Établir image/serveur d'inférence et contrat de réponse (synchrone, streaming, batch).
3. Planifier Pods selon CPU/GPU, mémoire, stockage des poids, quantization éventuelle et compatibilité runtime.
4. Établir TLS/Service/Route selon exposition, identités et NetworkPolicies.
5. Mesurer queue depth, requêtes en vol, temps premier token, tokens/s et latences p95/p99.
6. Configurer readiness réelle, capacité chaude, autoscaling sur signaux adaptés, rollout/rollback et DR.

#### 3. Diagramme de séquence

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

#### 4. Décisions d'architecture

- Serving via Deployment standard ou contrôleur d'inférence qualifié (KServe, si compatible).
- Demande ressources CPU/GPU, quantization, mémoire KV cache, scheduling et isolation des accélérateurs.
- Scale-to-zero seulement si cold start est compatible avec SLO ; souvent maintenir des réplicas chauds.
- Évaluer batching, longueur de contexte, flux streaming, limite de concurrence et fairness.
- Gestion versions modèles : provenance, canary, rollback, changement de tokenizer/prompt et droit de licence.

#### 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| GPU saturé et temps premier token élevé | Admission, quotas, file bornée, scaling selon métriques inférence. |
| Pod prêt mais modèle non chargé | Readiness ne passe qu'après chargement et test minimal. |
| Téléchargement artefact compromis | Poids vérifiés, registry approuvé, contrôle de provenance. |
| Scaling sur CPU seul inefficace | Mesurer KV cache/queue/running, pas seulement CPU. |
| Panne d'accélérateur | Routage vers réplicas prêts, fallback autorisé. |

#### 6. Tests et preuves attendues

1. Rolling update du modèle sans réponse mixte non maîtrisée.
2. Charge constante avec p95/p99 mesuré.
3. Cold start et eviction GPU simulés.
4. Refus des modèles non signés/non approuvés.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

#### 7. Compromis et critères de choix

Cœur plateforme requis pour héberger des modèles en production, mais il ne garantit ni qualité de contenu ni sécurité des actions.

#### 8. Question d'entretien

**Question :** Quels indicateurs spécifiques LLM utiliser pour scaler ?

**Réponse :** En plus CPU/GPU/mémoire, mesurer nombre de requêtes en attente/en cours, utilisation du KV cache, TTFT et débit de tokens.

#### 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Sources](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.

[Retour au programme](README.md) · [Cahier des exercices IA](exercices-et-corriges/cours-171-185.md)
