# 01 — RAG (Retrieval-Augmented Generation)

> **Famille :** IA générative · **Statut :** pattern d'architecture pédagogique · **Exemples fictifs et anonymisés**, aucun SI ou acteur d'entreprise réel revendiqué.

## 1. Définition et problème

Le RAG associe une recherche documentaire contrôlée à la génération d'une réponse par un modèle de langage. Il fournit du contexte externe au modèle sans modifier ses poids. Il n'établit pas par lui-même la véracité de la réponse.

**Besoin métier :** Un assistant doit expliquer une procédure opérationnelle à partir de documents internes versionnés. Le modèle seul peut inventer une règle, utiliser une version périmée ou répondre hors du périmètre autorisé.

## 2. Architecture et flux

~~~mermaid
flowchart TB
 U["Employé autorisé"] --> AUTH["Authentification + ACL documentaire"]
 AUTH --> Q["Recherche documentaire"]
 DOC["Procédures génériques validées"] --> ING["Ingestion + chunks + métadonnées"]
 ING --> IDX[("Index lexical / vectoriel")]
 Q --> IDX
 IDX --> FIL["Re-filtrage ACL + fraîcheur"]
 FIL --> CTX["Contexte cité + règles de sortie"]
 CTX --> LLM["LLM : synthèse"]
 LLM --> VER["Vérification de l'ancrage"]
 VER --> OUT["Réponse + références ou abstention"]
~~~

### Étapes de traitement

1. Ingestion documentaire : version, source, propriétaire, classification, date de validité.
2. Découpage en fragments pertinents et indexation lexicale/vectorielle, avec identité du document et droits.
3. Vérification de l'identité de l'utilisateur, puis filtrage des documents autorisés AVANT et APRÈS la recherche.
4. Récupération des fragments pertinents ; contrôle de fraîcheur, de qualité et de nombre de passages.
5. Construction d'un contexte limité, clairement séparé des instructions fiables ; génération d'une réponse qui cite ses passages.
6. Validation du fait que chaque affirmation matérielle est étayée ; si aucune preuve suffisante, répondre « information introuvable ». 

## 3. Diagramme de séquence illustratif

~~~mermaid
sequenceDiagram
 actor U as Utilisateur
 participant A as Assistant
 participant I as Index documentaire
 participant M as Modèle
 U->>A: Quelle est la procédure d'investigation d'un paiement non confirmé ?
 A->>I: Recherche ACL + version
 I-->>A: Extraits autorisés P-04 §2, P-09 §1
 A->>M: Question + extraits délimités
 M-->>A: Projet de synthèse et citations
 A->>A: Contrôle citations et droits
 A-->>U: Synthèse référencée ; pas d'ordre financier
~~~

**Scénario :** Demande fictive : « Un virement instantané n'a pas reçu sa confirmation ; quelle procédure consulter ? » Le RAG retrouve une procédure d'investigation P-04 et une instruction de rapprochement P-09. Il explique les vérifications à effectuer, mais **n'interroge pas automatiquement les comptes** et **n'affirme pas que le paiement est rejeté**.

## 4. Décisions à prendre en Design Authority

- Choisir recherche lexicale, vectorielle ou hybride selon langues, vocabulaire bancaire et corpus.
- Définir le modèle de droits à la granularité document/section ; le chunk ne doit pas hériter de droits plus larges.
- Choisir stratégie de chunking, overlap, mise à jour et suppression des index ; conserver la chaîne de provenance.
- Limiter nombre de passages et tokens ; pas de prompt contenant des données personnelles sans base légale/contrôles.
- Mesurer retrieval recall@k, précision/citations correctes, taux d'abstention justifié, latence et coût.

## 5. Scénarios de panne et parades

| Échec / attaque | Comportement attendu |
|---|---|
| Injection dans une procédure indexée | Traiter le document comme donnée non fiable, jamais comme instruction prioritaire. |
| Document retiré mais toujours indexé | Synchroniser ACL, version et suppression ; test de révocation. |
| Aucune source pertinente | Répondre « je ne trouve pas de source » plutôt que deviner. |
| Citation valide mais conclusion inventée | Vérifier que le passage soutient réellement la phrase générée. |

## 6. Tests d'acceptation

1. Utilisateur A ne reçoit jamais un fragment réservé à B.
2. Une phrase de type « ignore les règles » incluse dans un document n'exécute aucun outil.
3. Un document supprimé n'apparaît plus dans les réponses.
4. Question sans preuve déclenche abstention plutôt qu'affirmation.

**Critère transversal :** chaque décision sensible est explicable, les identités et autorisations sont contrôlées par code, et les exemples n'exécutent aucune opération bancaire réelle.

## 7. Compromis, limites et sélection

À préférer quand l'information change souvent ou que les réponses doivent être sourcées. Ne remplace ni une requête transactionnelle fiable ni une vérité financière autoritative.

À mesurer sur un jeu de référence : **qualité métier, confidentialité, latence p95/p99, coût par demande, robustesse aux attaques et taux d'abstention**. Documenter configuration, modèle, version, corpus et politique.

## 8. Question d'entretien

**Question :** Pourquoi RAG n'est-il pas une garantie contre les hallucinations ?

**Réponse :** Il apporte des sources, mais le modèle peut mal les comprendre, citer une mauvaise version ou extrapoler. Il faut évaluer récupération ET fidélité de génération.

## 9. Mise en œuvre et approfondissement

- Plateforme de référence : API sécurisée, orchestration Java ou Python sur Kubernetes/OpenShift, logs et métriques structurés ; aucun produit commercial imposé.
- [Architecture IA de bout en bout](../reference-ai-platform-openshift/README.md) · [Matrice de sélection](../PATTERNS_DECISION_MATRIX.md) · [Sources techniques](../REFERENCES.md).
- Les mécanismes de sécurité doivent être vérifiés indépendamment des réponses du LLM ; aucun prompt ne remplace AuthZ ou la validation d'un outil.
