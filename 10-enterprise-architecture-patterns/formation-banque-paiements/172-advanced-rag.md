# Cours 172 — Advanced RAG — Hybrid Retrieval et Reranking · Architecture IA et agentique

> Cas fictif : banque pédagogique, suivi d'un virement SEPA de 500 EUR. La plateforme IA est **distincte du système autoritatif financier**. **Corrigé théorique fourni, exercice individuel non encore validé.**

## 1. Besoin et objectifs
Le corpus d'incidents contient sigles MQ, codes ISO 20022 et termes métier : une recherche vectorielle seule peut manquer une procédure exacte.

## 2. Fonctionnement et HLD
~~~mermaid
flowchart LR
    A["Requête bancaire et droits"] --> B["Hybride lexical + vecteur, fusion/reranking"]
    B --> C["Passages autorisés les plus pertinents"]
    B -. "Droits, preuve ou confiance insuffisants" .-> X["Refus / abstention / investigation"]
~~~

**Décision architecturale :** Combiner BM25/lexical et sémantique, reranker des candidats autorisés, préserver versions et filtres d'ACL ; mesurer qualité des passages réellement utilisés par la synthèse.

## 3. Frontières de confiance
Un reranker optimise la pertinence, pas les habilitations ou la vérité ; un rappel plus élevé ne justifie pas un accès inter-tenant.

1. **Identité :** subject, tenant et autorisations établis par un composant déterministe au point de service.
2. **Données :** classification, provenance, versions de documents et politiques de rétention.
3. **Modèle :** version, paramètres, fournisseur autorisé, coût et contexte réellement transmis.
4. **Outils :** allowlist, schéma d'arguments, contrôle d'objet et privilèges minimaux.
5. **Résultat :** réponse assistée, recommandation ou abstention ; jamais confirmation du règlement d'un paiement sur seule sortie LLM.

## 4. Séquence nominale et incident
~~~mermaid
sequenceDiagram
    participant U as Utilisateur habilité
    participant G as AI Gateway / politique
    participant A as Advanced RAG
    participant R as Sources ou outils autorisés
    U->>G: tâche et identité
    G->>A: contexte validé et budget
    A->>R: lecture / traitement autorisé
    R-->>A: observations (données non fiables)
    alt preuve suffisante
       A-->>G: synthèse sourcée / proposition
       G-->>U: résultat contrôlé
    else droit absent ou résultat incertain
       A-->>G: aucune preuve suffisante / erreur
       G-->>U: refus ou abstention
    end
~~~

## 5. Tests d'architecture et attaques
- **Nominal :** exécuter un scénario de référence et identifier sources, version modèle et décisions appliquées.
- **Test de sécurité :** Injecter un passage très pertinent mais non autorisé : il ne doit ni être reranké dans la liste visible ni servir à la réponse.
- **Test d'échec :** Sur un jeu de questions de sigles, mesurer gain recall/nDCG, latence et absence de fuite comparativement au RAG simple.
- **Révocation :** retirer un droit ou supprimer une source puis vérifier que résultat et cache ne la réexposent pas.
- **Timeout / reprise :** budget borné, pas de mutation répétée, statut bancaire consulté via système compétent.
- **Mesures de qualité :** Recall@k, MRR/nDCG, latence de reranking, pertinence citée, recall par groupe sans fuite.

## 6. ADR, compromis et non-garanties
Comparer systématiquement une solution plus simple, sans agent, ou avec un modèle local lorsque les NFR l'autorisent. Documenter résidence des données, coût, performance, périmètre d'outil, attaques indirectes et taux d'erreur acceptable.

## 7. Exercice corrigé
**Peut-on reranker un passage d'un tenant non autorisé ?**
- **A.** Oui si son score de pertinence dépasse un seuil.
- **B.** Non : seuls des candidats ayant passé les contrôles d'accès peuvent atteindre le modèle de reranking.
- **C.** Oui si on retire le nom du tenant de la citation.

**Bonne réponse théorique : B.** Non : seuls des candidats ayant passé les contrôles d'accès peuvent atteindre le modèle de reranking.

> L'exercice est disponible pour auto-étude ; aucun score individuel n'est déclaré.

## 8. Fiche de référence existante — approfondissement
[Fiche source détaillée](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/02-advanced-rag/README.md)

> **Famille :** IA générative · **Statut :** pattern d'architecture pédagogique · **Exemples fictifs et anonymisés**, aucun SI ou acteur d'entreprise réel revendiqué.

#### 1. Définition et problème

Ensemble de raffinements RAG : recherche hybride lexicale/sémantique, filtres de métadonnées, expansion ou décomposition des requêtes, reranking, contextualisation et parfois récupération multi-sauts.

**Besoin métier :** Une requête comme « que faire après un timeout de règlement ? » emploie un vocabulaire différent de la procédure « absence de confirmation » ; une recherche naïve manque des sources pertinentes.

#### 2. Architecture et flux

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

#### Étapes de traitement

1. Analyser l'intention ; extraire type de processus et version des règles sans changer silencieusement la question.
2. Appliquer les ACL et filtres de validité à l'espace documentaire.
3. Interroger en parallèle index lexical et index vectoriel ; fusionner les candidats sans exposer de document interdit.
4. Reranker les candidats selon leur pertinence à la question et leur autorité documentaire.
5. Assembler contexte limité et dédupliquer fragments voisins.
6. Générer avec citations ; vérifier support des affirmations et abstention en cas de preuve insuffisante.

#### 3. Diagramme de séquence illustratif

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

#### 4. Décisions à prendre en Design Authority

- Mesurer l'amélioration par rapport à un RAG de base avant de multiplier les composants.
- Fusionner les résultats en conservant provenance, scores comparables et filtrage de sécurité.
- Reranking sur candidats autorisés uniquement : pas de divulgation dans traces/modèles externes.
- Définir top-k initial, top-n final, latence p95, qualité multilingue et tolérance aux acronymes.
- Versionner prompts de reformulation et modèle de reranking ; tester le déplacement du sens métier.

#### 5. Scénarios de panne et parades

| Échec / attaque | Comportement attendu |
|---|---|
| Reformulation erronée | Conserver question originale et évaluer sur requêtes bancaires difficiles. |
| Reranking onéreux/lent | Limiter candidats, mesurer p95 et proposer mode simplifié. |
| Version périmée mieux notée | Prioriser validité métier avant score sémantique. |
| Document interdit fusionné | Filtrage ACL systématique à tous les stades. |

#### 6. Tests d'acceptation

1. Question technique abrégée trouve la procédure correcte.
2. La version retirée ne gagne pas face à une version active.
3. L'augmentation du top-k n'expose pas de données interdites.
4. Comparaison mesurée basic RAG vs hybrid+rerank sur jeu de référence.

**Critère transversal :** chaque décision sensible est explicable, les identités et autorisations sont contrôlées par code, et les exemples n'exécutent aucune opération bancaire réelle.

#### 7. Compromis, limites et sélection

Complexité et latence supplémentaires ; adopter seulement si les gains de rappel/fidélité sont démontrés.

À mesurer sur un jeu de référence : **qualité métier, confidentialité, latence p95/p99, coût par demande, robustesse aux attaques et taux d'abstention**. Documenter configuration, modèle, version, corpus et politique.

#### 8. Question d'entretien

**Question :** Pourquoi le meilleur score vectoriel ne garantit-il pas le bon document ?

**Réponse :** La proximité sémantique ne code pas les habilitations, la date de validité ni la hiérarchie des sources.

#### 9. Mise en œuvre et approfondissement

- Plateforme de référence : API sécurisée, orchestration Java ou Python sur Kubernetes/OpenShift, logs et métriques structurés ; aucun produit commercial imposé.
- [Architecture IA de bout en bout](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice de sélection](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Sources techniques](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- Les mécanismes de sécurité doivent être vérifiés indépendamment des réponses du LLM ; aucun prompt ne remplace AuthZ ou la validation d'un outil.

[Programme des cours](README.md) · [Exercices IA 171–185](exercices-et-corriges/cours-171-185.md)
