# 03 — Model Router

> **Famille :** IA générative · **Statut :** pattern d'architecture pédagogique · **Exemples fictifs et anonymisés**, aucun SI ou acteur d'entreprise réel revendiqué.

## 1. Définition et problème

Un composant de politique dirige une requête vers le modèle admissible selon complexité, capacité, latence, coût, confidentialité, région de traitement et disponibilité. Il diffère du routage vers un Pod d'un même modèle.

**Besoin métier :** Une extraction structurée de deux lignes n'exige pas nécessairement le même modèle qu'une synthèse approfondie de longues procédures, et certaines données ne doivent pas quitter un périmètre d'exécution.

## 2. Architecture et flux

~~~mermaid
flowchart TB
 IN["Requête et classification"] --> POLICY{"Politique de données"}
 POLICY -->|"Confidentiel"| LOCAL["Modèle local approuvé"]
 POLICY -->|"Données publiques"| SCORE["Score : qualité, latence, coût"]
 SCORE --> SIMPLE["Petit modèle"]
 SCORE --> COMPLEX["Modèle large"]
 LOCAL --> G["Sortie vérifiée"]
 SIMPLE --> G
 COMPLEX --> G
~~~

### Étapes de traitement

1. Classifier demande (lecture documentaire, extraction, code, assistance métier) et sensibilité sans confier la seule sécurité au classifieur LLM.
2. Appliquer politique de résidence, confidentialité, autorisations et famille de modèles approuvés.
3. Comparer budget tokens, taille de contexte, qualité attendue, SLO et coûts.
4. Sélectionner le modèle puis le servir via une interface versionnée.
5. Contrôler réponse, usage tokens, durée, taux d'erreur et motif du routage.
6. Sur erreur, basculer seulement vers une cible **également autorisée** selon Model Fallback.

## 3. Diagramme de séquence illustratif

~~~mermaid
sequenceDiagram
 actor U as Collaborateur
 participant R as Routeur de modèles
 participant P as Moteur de politique
 participant M as Model Serving local
 U->>R: Classer un document interne
 R->>P: Classe de données, tâche, budget
 P-->>R: Local uniquement, modèle compact v3
 R->>M: Infer(version=v3)
 M-->>R: Résultat JSON
 R-->>U: Résultat + trace de routage
~~~

**Scénario :** Extraction fictive d'un code d'incident dans un document interne : modèle local compact. Analyse approfondie de documents publics : modèle plus puissant autorisé si coût et latence le permettent. Les règles de confidentialité passent avant l'optimisation de prix.

## 4. Décisions à prendre en Design Authority

- Routing déterministe par politique pour cas à fort risque ; routeur ML en option évaluée.
- Registre de modèles approuvés avec version, capacités, licences, région, type de données.
- Budget maximal coût/tokens et latence, dimensionnement et prévention de surconsommation.
- Politique de failover : ne jamais échanger la confidentialité contre la disponibilité.
- Mesures : exactitude par classe de tâche, routing accuracy, coûts et changement de comportement par version.

## 5. Scénarios de panne et parades

| Échec / attaque | Comportement attendu |
|---|---|
| Classification erronée de données sensibles | Politique de classification en amont, choix local en cas de doute. |
| Modèle bon marché trop faible | Évaluation sur jeu de tests par catégorie et escalade contrôlée. |
| Fallback vers une région interdite | Allowlist de destinations par classe de données. |
| Variabilité des résultats selon routage | Traçabilité modèle/version et suite de tests de régression. |

## 6. Tests d'acceptation

1. Requête confidentielle ne sort pas du périmètre autorisé.
2. Faible complexité route vers modèle approuvé compact.
3. Modèle indisponible avec aucune alternative autorisée : réponse indisponible, pas fuite.
4. Changement de version produit un compte-rendu de régression.

**Critère transversal :** chaque décision sensible est explicable, les identités et autorisations sont contrôlées par code, et les exemples n'exécutent aucune opération bancaire réelle.

## 7. Compromis, limites et sélection

À privilégier avec plusieurs modèles et une politique de données mature ; inutile pour une plateforme mono-modèle sans besoin d'optimisation.

À mesurer sur un jeu de référence : **qualité métier, confidentialité, latence p95/p99, coût par demande, robustesse aux attaques et taux d'abstention**. Documenter configuration, modèle, version, corpus et politique.

## 8. Question d'entretien

**Question :** Quelle est la première règle d'un routeur de modèles ?

**Réponse :** Respecter les contraintes de sécurité, d'autorisation et de localisation, avant coût et performance.

## 9. Mise en œuvre et approfondissement

- Plateforme de référence : API sécurisée, orchestration Java ou Python sur Kubernetes/OpenShift, logs et métriques structurés ; aucun produit commercial imposé.
- [Architecture IA de bout en bout](../reference-ai-platform-openshift/README.md) · [Matrice de sélection](../PATTERNS_DECISION_MATRIX.md) · [Sources techniques](../REFERENCES.md).
- Les mécanismes de sécurité doivent être vérifiés indépendamment des réponses du LLM ; aucun prompt ne remplace AuthZ ou la validation d'un outil.
