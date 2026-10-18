# 05 — ReAct / Tool Calling

> **Famille :** IA agentique · **Statut :** pattern d'architecture pédagogique · **Exemples fictifs et anonymisés**, aucun SI ou acteur d'entreprise réel revendiqué.

## 1. Définition et problème

Boucle structurée où un agent choisit une action/outillage, observe un résultat contrôlé, puis produit une réponse. ReAct est une stratégie d'interleaving raisonnement/actions, tandis que **Tool Calling** est une interface structurée d'invocation d'outils ; les deux ne sont pas synonymes.

**Besoin métier :** Un modèle ne peut pas connaître en direct le statut d'un dossier. Il doit interroger un service autorisé plutôt qu'inventer le résultat. Mais un agent avec outils d'écriture peut produire des effets métier dangereux.

## 2. Architecture et flux

~~~mermaid
flowchart TB
 U["Question : statut du dossier fictif D-001"] --> L["Agent LLM"]
 L --> DEC{"Besoin d'information actualisée ?"}
 DEC -->|Oui| POL["Politique outils autorisés"]
 POL --> READ["Tool: get_case_status (lecture seule)"]
 READ --> OBS["Observation non fiable / structurée"]
 OBS --> L
 DEC -->|Non| ANSWER["Réponse"]
 L --> ANSWER
 POL -.-> BLOCK["Outil de modification refusé sans approbation"]
~~~

### Étapes de traitement

1. Recevoir objectif et identité ; séparer instruction du demandeur et documents/outils moins fiables.
2. Lister les outils autorisés à cet utilisateur et à ce contexte (allowlist, schémas d'arguments).
3. Choisir et valider l'appel avec contrôle déterministe des droits et des paramètres.
4. Exécuter l'outil via médiateur sécurisé, avec timeout et journaux d'audit.
5. Interpréter la **réponse comme donnée**, jamais comme instruction permettant une nouvelle permission.
6. Limiter nombre d'itérations et budget, gérer erreurs et demander validation humaine avant effets sensibles.

## 3. Diagramme de séquence illustratif

~~~mermaid
sequenceDiagram
 actor U as Utilisateur
 participant A as Agent
 participant P as Policy Engine
 participant T as Outil lecture
 U->>A: Quel est le statut du dossier D-001 ?
 A->>P: Autoriser get_case_status(D-001) ?
 P-->>A: Lecture autorisée
 A->>T: get_case_status(D-001)
 T-->>A: {"status":"PENDING_REVIEW"}
 A-->>U: Statut = PENDING_REVIEW, provenance outil
~~~

**Scénario :** L'agent consulte un dossier fictif par une API en lecture seule. Il ne peut **ni approuver** une demande ni **émettre** un paiement ; ces outils ne figurent pas dans son jeu de permissions. Une demande d'action sensible passe par HITL.

## 4. Décisions à prendre en Design Authority

- Outils typés avec schémas validés et sous-ensemble de permissions par utilisateur.
- Compte de service restreint, contrôle d'accès côté API, pas seulement dans le prompt.
- Budget max étapes, temps, tokens, coût ; compensation pour actions réversibles.
- Traçabilité appels/retours expurgés et liaison à traceId/decisionId.
- Protection contre prompt injection indirecte dans résultats d'outils (texte retourné est non fiable).

## 5. Scénarios de panne et parades

| Échec / attaque | Comportement attendu |
|---|---|
| Agent appelle un outil non autorisé | Policy engine rejette, API métier vérifie la permission. |
| Boucle infinie d'outils | Budget d'itérations et timeout global. |
| Réponse API contient instruction malveillante | Traiter contenu comme donnée ; pas de changement de règles. |
| Action répétée après timeout | Idempotency-key, interrogation statut, suspension si outcome inconnu. |

## 6. Tests d'acceptation

1. Agent ne peut invoquer un outil absent de l'allowlist.
2. Résultat d'outil contenant « ignore les règles » ne déclenche aucune nouvelle action.
3. Timeout ne provoque pas de deuxième mutation.
4. Budget max tool calls est strictement appliqué.

**Critère transversal :** chaque décision sensible est explicable, les identités et autorisations sont contrôlées par code, et les exemples n'exécutent aucune opération bancaire réelle.

## 7. Compromis, limites et sélection

Utile pour collecte ou investigation assistée ; jamais un moyen de contourner autorisations ou procédures métier.

À mesurer sur un jeu de référence : **qualité métier, confidentialité, latence p95/p99, coût par demande, robustesse aux attaques et taux d'abstention**. Documenter configuration, modèle, version, corpus et politique.

## 8. Question d'entretien

**Question :** Une instruction dans le résultat d'un outil peut-elle autoriser une mutation ?

**Réponse :** Non, seule une politique applicative et une éventuelle approbation humaine le peuvent.

## 9. Mise en œuvre et approfondissement

- Plateforme de référence : API sécurisée, orchestration Java ou Python sur Kubernetes/OpenShift, logs et métriques structurés ; aucun produit commercial imposé.
- [Architecture IA de bout en bout](../reference-ai-platform-openshift/README.md) · [Matrice de sélection](../PATTERNS_DECISION_MATRIX.md) · [Sources techniques](../REFERENCES.md).
- Les mécanismes de sécurité doivent être vérifiés indépendamment des réponses du LLM ; aucun prompt ne remplace AuthZ ou la validation d'un outil.
