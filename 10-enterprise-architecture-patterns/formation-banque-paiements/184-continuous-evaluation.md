# Cours 184 — Continuous Evaluation — Qualité, drift et sécurité · Architecture IA et agentique

> Banque fictive · ordre SEPA de 500 EUR. **Support pédagogique publié avec corrigé théorique ; aucun exercice individuel ni test sur cluster n'est déclaré validé.**

## 1. Besoin métier et problème
Le corpus, les prompts, le modèle et les règles évoluent ; une réponse autrefois exacte peut citer une procédure périmée ou révéler des données après une mise à jour.

## 2. HLD : responsabilités des composants
~~~mermaid
flowchart LR
    A["Jeux de référence + traces expurgées"] --> B["Évaluation qualité / sécurité / drift"]
    B --> C["Gates de release et suivi continu"]
    B -. "Risque / absence de preuve" .-> STOP["Refus, attente ou abstention"]
~~~

**Décision d'architecture :** Définir un jeu de référence avec gold answers, vérité de sources, tests d'ACL et d'injection, métriques qualité/coût/latence ; comparer à une baseline, détecter drift et bloquer les versions régressives.

**Invariant à défendre :** Aucune version de modèle, prompt, index ou politique ne passe en production sans critères de sécurité et de fidélité définis.

## 3. Contrat de contrôle
~~~text
release = qualityGatesPass && accessControlsPass && securityGatesPass && costWithinBudget
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
2. **Attaque simulée :** Une version augmente les réponses plausibles mais fait passer 1 fuite cross-tenant : gate bloquant malgré meilleur score moyen.
3. **Panne / non-régression :** Comparer versions sur jeu hors échantillon et données adversariales ; tester citations, abstentions, permissions, outils, drift, latence et rollback.
4. **Reprise et confidentialité :** ne jamais interpréter une indisponibilité de l'IA comme un règlement rejeté ou réglé ; conserver la classification des données.
5. **Mesures à instrumenter :** qualité métier, groundedness, précision/rappel, fuite d'ACL, coût, p95/p99, taux d'abstention.
6. **Responsabilité métier :** toute opération sensible conserve une politique déterministe et, le cas échéant, une approbation humaine indépendante.

## 6. ADR et choix d'alternatives
Comparer la solution à une application déterministe, à un RAG sans agent et à un modèle local lorsque cela réduit le coût, la latence ou le risque. Documenter limites de contexte, budgets, risques indirects, versions, capacités OpenShift et stratégie de retrait.

## 7. Auto-évaluation corrigée
**Peut-on promouvoir un modèle si sa moyenne de qualité augmente mais qu'il fuit une pièce client ?**
- **A.** Non : les critères bloquants de confidentialité et de sécurité priment sur la note moyenne.
- **B.** Oui, une meilleure moyenne compense une fuite occasionnelle.
- **C.** Oui si la fuite n'apparaît que dans les tests adversariaux.

**Bonne réponse théorique : A.** Non : les critères bloquants de confidentialité et de sécurité priment sur la note moyenne.

Cette clé est un corrigé de cours, pas une validation individuelle.

## 8. Référence détaillée existante dans le dépôt
[Fiche source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/14-continuous-evaluation/README.md)

> **Famille :** Production / MLOps · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

#### 1. Définition et besoin

Évaluer les applications IA avant mise en production et continuellement après chaque changement de modèle, prompt, index, outil ou politique. On distingue qualité offline sur jeu de référence, tests de sécurité et métriques online.

**Problème :** Un changement d'embedding ou de modèle améliore les réponses génériques mais dégrade l'exactitude de procédures techniques et augmente la proportion de citations non pertinentes.

#### 2. Architecture logique

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

#### Déroulement

1. Créer un jeu de référence versionné : questions, réponses attendues, passages probants et permissions.
2. Mesurer offline retrieval (recall@k), fidélité aux sources, qualité métier, abstentions justifiées et schémas.
3. Tester sécurité/adversarial : prompt injection, exfiltration, données hors périmètre, tool misuse.
4. Déployer en environnement de qualification/shadow, puis canary selon profil de risque.
5. Surveiller online latence, tokens, coûts, retours utilisateurs, drift des requêtes et erreurs de citations.
6. Analyser les régressions ; rollback modèle/prompt/index et mise à jour contrôlée du jeu de référence.

#### 3. Diagramme de séquence

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

#### 4. Décisions d'architecture

- Jeu de référence représentatif, avec cas rares, langues et scénarios de refus.
- Critères objectifs séparant génération, retrieval, sécurité, coût et délai.
- Revue humaine échantillonnée et analyse du désaccord entre juges automatisés.
- Cohérence des versions modèle, embeddings, index, prompt, guardrail et data lineage.
- Définir qui approuve rollback, canary et modification de seuils.

#### 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| Golden set trop simple | Inclure cas difficiles et adversariaux, stratifier par segment. |
| Judge LLM biaisé ou instable | Références humaines, calibration et règles déterministes. |
| Observations online contiennent PII | Agrégation/minimisation, consentements et rétention. |
| Mise à jour index sans réévaluation | Gate déclenché sur toute modification de corpus/schéma. |
| Régression de sécurité non détectée | Red-team continu et simulation de tool misuse. |

#### 6. Tests et preuves attendues

1. Le pipeline refuse un score de fidélité sous seuil.
2. Retirer un document d'accès restreint ne provoque pas fuite.
3. Rétablir version antérieure du corpus et modèle possible.
4. Chaque sortie critique est associée à des références ou abstention.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

#### 7. Compromis et critères de choix

Nécessaire pour fiabilité mesurée ; attention à la validité des métriques et au coût des évaluations.

#### 8. Question d'entretien

**Question :** Peut-on évaluer uniquement le taux de réponses jugées utiles ?

**Réponse :** Non : mesurer également exactitude aux preuves, refus, permissions, latence/coût, robustesse et sécurité.

#### 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Sources](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.

[Retour au programme](README.md) · [Cahier des exercices IA](exercices-et-corriges/cours-171-185.md)
