# 02 — Advanced RAG : hybrid retrieval, reranking et contextualisation

> **Famille :** IA générative · **Statut :** pattern d'architecture pédagogique · **Exemples fictifs et anonymisés**, aucun SI ou acteur d'entreprise réel revendiqué.

## 1. Définition et problème

Ensemble de raffinements RAG : recherche hybride lexicale/sémantique, filtres de métadonnées, expansion ou décomposition des requêtes, reranking, contextualisation et parfois récupération multi-sauts.

**Besoin métier :** Une requête comme « que faire après un timeout de règlement ? » emploie un vocabulaire différent de la procédure « absence de confirmation » ; une recherche naïve manque des sources pertinentes.

## 2. Architecture et flux

~~~mermaid
flowchart TB
 Q["Question métier"] --> SEC["Droits + filtres documentaires"]
 SEC --> L["Recherche lexicale BM25"]
 SEC --> V["Recherche vectorielle"]
 L --> MERGE["Fusion des candidats autorisés"]
 V --> MERGE
 MERGE --> RE["Reranking + contrôle de fraîcheur"]
 RE --> C["Context packing"]
 C --> G["LLM + citations"]
 G --> CHECK["Contrôle fidélité / abstention"]
~~~

### Étapes de traitement

1. Analyser l'intention ; extraire type de processus et version des règles sans changer silencieusement la question.
2. Appliquer les ACL et filtres de validité à l'espace documentaire.
3. Interroger en parallèle index lexical et index vectoriel ; fusionner les candidats sans exposer de document interdit.
4. Reranker les candidats selon leur pertinence à la question et leur autorité documentaire.
5. Assembler contexte limité et dédupliquer fragments voisins.
6. Générer avec citations ; vérifier support des affirmations et abstention en cas de preuve insuffisante.

## 3. Diagramme de séquence illustratif

~~~mermaid
sequenceDiagram
 participant U as Analyste
 participant R as Recherche hybride
 participant K as Reranker
 participant L as Modèle
 U->>R: « timeout du règlement »
 R->>R: Termes + variantes métier contrôlées
 R-->>K: Procédure « confirmation absente » et règles associées
 K-->>L: Top passages autorisés et actuels
 L-->>U: Réponse documentée, limites explicites
~~~

**Scénario :** Deux procédures fictives utilisent « attente de retour » et « confirmation manquante ». Le retrieval hybride les retrouve toutes deux ; le reranker classe d'abord la version en vigueur et écarte une note de test obsolète.

## 4. Décisions à prendre en Design Authority

- Mesurer l'amélioration par rapport à un RAG de base avant de multiplier les composants.
- Fusionner les résultats en conservant provenance, scores comparables et filtrage de sécurité.
- Reranking sur candidats autorisés uniquement : pas de divulgation dans traces/modèles externes.
- Définir top-k initial, top-n final, latence p95, qualité multilingue et tolérance aux acronymes.
- Versionner prompts de reformulation et modèle de reranking ; tester le déplacement du sens métier.

## 5. Scénarios de panne et parades

| Échec / attaque | Comportement attendu |
|---|---|
| Reformulation erronée | Conserver question originale et évaluer sur requêtes bancaires difficiles. |
| Reranking onéreux/lent | Limiter candidats, mesurer p95 et proposer mode simplifié. |
| Version périmée mieux notée | Prioriser validité métier avant score sémantique. |
| Document interdit fusionné | Filtrage ACL systématique à tous les stades. |

## 6. Tests d'acceptation

1. Question technique abrégée trouve la procédure correcte.
2. La version retirée ne gagne pas face à une version active.
3. L'augmentation du top-k n'expose pas de données interdites.
4. Comparaison mesurée basic RAG vs hybrid+rerank sur jeu de référence.

**Critère transversal :** chaque décision sensible est explicable, les identités et autorisations sont contrôlées par code, et les exemples n'exécutent aucune opération bancaire réelle.

## 7. Compromis, limites et sélection

Complexité et latence supplémentaires ; adopter seulement si les gains de rappel/fidélité sont démontrés.

À mesurer sur un jeu de référence : **qualité métier, confidentialité, latence p95/p99, coût par demande, robustesse aux attaques et taux d'abstention**. Documenter configuration, modèle, version, corpus et politique.

## 8. Question d'entretien

**Question :** Pourquoi le meilleur score vectoriel ne garantit-il pas le bon document ?

**Réponse :** La proximité sémantique ne code pas les habilitations, la date de validité ni la hiérarchie des sources.

## 9. Mise en œuvre et approfondissement

- Plateforme de référence : API sécurisée, orchestration Java ou Python sur Kubernetes/OpenShift, logs et métriques structurés ; aucun produit commercial imposé.
- [Architecture IA de bout en bout](../reference-ai-platform-openshift/README.md) · [Matrice de sélection](../PATTERNS_DECISION_MATRIX.md) · [Sources techniques](../REFERENCES.md).
- Les mécanismes de sécurité doivent être vérifiés indépendamment des réponses du LLM ; aucun prompt ne remplace AuthZ ou la validation d'un outil.
