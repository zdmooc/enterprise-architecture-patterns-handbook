# Cours 173 — Model Router — Routage des modèles · Architecture IA et agentique

> Cas fictif : banque pédagogique, suivi d'un virement SEPA de 500 EUR. La plateforme IA est **distincte du système autoritatif financier**. **Corrigé théorique fourni, exercice individuel non encore validé.**

## 1. Besoin et objectifs
La plateforme dispose d'un modèle local pour données sensibles et d'un autre pour des textes publics ; les requêtes doivent être dirigées selon coût, capacité, disponibilité et classification.

## 2. Fonctionnement et HLD
~~~mermaid
flowchart LR
    A["Tâche + classification + identité"] --> B["Politique déterministe de sélection"]
    B --> C["Modèle autorisé et version tracée"]
    B -. "Droits, preuve ou confiance insuffisants" .-> X["Refus / abstention / investigation"]
~~~

**Décision architecturale :** Définir une allowlist de modèles par classification, localisation, contrat et budget ; router sans permettre au LLM de s'accorder seul un fournisseur ou une région interdits.

## 3. Frontières de confiance
Une indisponibilité du modèle autorisé ne permet pas d'envoyer le contenu bancaire à un modèle public non homologué.

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
    participant A as Model Router
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
- **Test de sécurité :** Demander une baisse de coût avec un document confidentiel alors que seul un modèle local est autorisé : refus ou attente, pas d'exfiltration.
- **Test d'échec :** Tester 4 types de données, un modèle down, budget dépassé et changement de policy ; vérifier le modèle réellement appelé.
- **Révocation :** retirer un droit ou supprimer une source puis vérifier que résultat et cache ne la réexposent pas.
- **Timeout / reprise :** budget borné, pas de mutation répétée, statut bancaire consulté via système compétent.
- **Mesures de qualité :** Taux de routage conforme, coût par requête, latence, qualité par modèle, saturation, incidents de data residency.

## 6. ADR, compromis et non-garanties
Comparer systématiquement une solution plus simple, sans agent, ou avec un modèle local lorsque les NFR l'autorisent. Documenter résidence des données, coût, performance, périmètre d'outil, attaques indirectes et taux d'erreur acceptable.

## 7. Exercice corrigé
**Que faire si le modèle autorisé est indisponible ?**
- **A.** Basculer sans contrôle vers un fournisseur externe moins cher.
- **B.** Laisser le texte du prompt choisir sa zone géographique.
- **C.** Rester dans l'ensemble des modèles autorisés, sinon dégrader ou refuser explicitement la requête.

**Bonne réponse théorique : C.** Rester dans l'ensemble des modèles autorisés, sinon dégrader ou refuser explicitement la requête.

> L'exercice est disponible pour auto-étude ; aucun score individuel n'est déclaré.

## 8. Fiche de référence existante — approfondissement
[Fiche source détaillée](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/03-model-router/README.md)

> **Famille :** IA générative · **Statut :** pattern d'architecture pédagogique · **Exemples fictifs et anonymisés**, aucun SI ou acteur d'entreprise réel revendiqué.

#### 1. Définition et problème

Un composant de politique dirige une requête vers le modèle admissible selon complexité, capacité, latence, coût, confidentialité, région de traitement et disponibilité. Il diffère du routage vers un Pod d'un même modèle.

**Besoin métier :** Une extraction structurée de deux lignes n'exige pas nécessairement le même modèle qu'une synthèse approfondie de longues procédures, et certaines données ne doivent pas quitter un périmètre d'exécution.

#### 2. Architecture et flux

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

#### Étapes de traitement

1. Classifier demande (lecture documentaire, extraction, code, assistance métier) et sensibilité sans confier la seule sécurité au classifieur LLM.
2. Appliquer politique de résidence, confidentialité, autorisations et famille de modèles approuvés.
3. Comparer budget tokens, taille de contexte, qualité attendue, SLO et coûts.
4. Sélectionner le modèle puis le servir via une interface versionnée.
5. Contrôler réponse, usage tokens, durée, taux d'erreur et motif du routage.
6. Sur erreur, basculer seulement vers une cible **également autorisée** selon Model Fallback.

#### 3. Diagramme de séquence illustratif

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

#### 4. Décisions à prendre en Design Authority

- Routing déterministe par politique pour cas à fort risque ; routeur ML en option évaluée.
- Registre de modèles approuvés avec version, capacités, licences, région, type de données.
- Budget maximal coût/tokens et latence, dimensionnement et prévention de surconsommation.
- Politique de failover : ne jamais échanger la confidentialité contre la disponibilité.
- Mesures : exactitude par classe de tâche, routing accuracy, coûts et changement de comportement par version.

#### 5. Scénarios de panne et parades

| Échec / attaque | Comportement attendu |
|---|---|
| Classification erronée de données sensibles | Politique de classification en amont, choix local en cas de doute. |
| Modèle bon marché trop faible | Évaluation sur jeu de tests par catégorie et escalade contrôlée. |
| Fallback vers une région interdite | Allowlist de destinations par classe de données. |
| Variabilité des résultats selon routage | Traçabilité modèle/version et suite de tests de régression. |

#### 6. Tests d'acceptation

1. Requête confidentielle ne sort pas du périmètre autorisé.
2. Faible complexité route vers modèle approuvé compact.
3. Modèle indisponible avec aucune alternative autorisée : réponse indisponible, pas fuite.
4. Changement de version produit un compte-rendu de régression.

**Critère transversal :** chaque décision sensible est explicable, les identités et autorisations sont contrôlées par code, et les exemples n'exécutent aucune opération bancaire réelle.

#### 7. Compromis, limites et sélection

À privilégier avec plusieurs modèles et une politique de données mature ; inutile pour une plateforme mono-modèle sans besoin d'optimisation.

À mesurer sur un jeu de référence : **qualité métier, confidentialité, latence p95/p99, coût par demande, robustesse aux attaques et taux d'abstention**. Documenter configuration, modèle, version, corpus et politique.

#### 8. Question d'entretien

**Question :** Quelle est la première règle d'un routeur de modèles ?

**Réponse :** Respecter les contraintes de sécurité, d'autorisation et de localisation, avant coût et performance.

#### 9. Mise en œuvre et approfondissement

- Plateforme de référence : API sécurisée, orchestration Java ou Python sur Kubernetes/OpenShift, logs et métriques structurés ; aucun produit commercial imposé.
- [Architecture IA de bout en bout](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice de sélection](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Sources techniques](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- Les mécanismes de sécurité doivent être vérifiés indépendamment des réponses du LLM ; aucun prompt ne remplace AuthZ ou la validation d'un outil.

[Programme des cours](README.md) · [Exercices IA 171–185](exercices-et-corriges/cours-171-185.md)
