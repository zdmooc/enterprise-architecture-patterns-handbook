# 04 — Semantic Cache

> **Famille :** IA générative · **Statut :** pattern d'architecture pédagogique · **Exemples fictifs et anonymisés**, aucun SI ou acteur d'entreprise réel revendiqué.

## 1. Définition et problème

Cache des réponses récupérées à partir d'une proximité sémantique plutôt que d'une stricte égalité de chaîne. Sa réutilisation exige une identité de contexte, des permissions et des versions compatibles.

**Besoin métier :** Des milliers de questions proches sur une FAQ publique font refaire des inférences coûteuses ; un cache naïf peut toutefois divulguer à l'utilisateur B une réponse créée pour A.

## 2. Architecture et flux

~~~mermaid
flowchart TB
 Q["Question + identité + version docs"] --> A{"Type de demande cachable ?"}
 A -->|Non| R["RAG/LLM normal"]
 A -->|Oui| C["Recherche de voisins sémantiques"]
 C --> ACL{"Permissions, versions, TTL concordent ?"}
 ACL -->|Oui| HIT["Réponse validée du cache"]
 ACL -->|Non| R
 R --> VALID["Valider résultat"]
 VALID --> STORE["Mise en cache si admissible"]
~~~

### Étapes de traitement

1. Qualifier l'opération : ne mettre en cache que les réponses admissibles et non actionnelles.
2. Construire une clé englobant tenant, scopes, classification, collection documentaire/version, modèle/prompt/version et langue.
3. Rechercher candidats sémantiquement voisins avec seuil calibré.
4. Vérifier compatibilité stricte des droits et de la base documentaire AVANT lecture du résultat.
5. Appliquer durée de vie, invalidation par nouvelle procédure, et contrôle des résultats sensibles.
6. Sur miss, effectuer RAG/inférence ; après validation, stocker l'entrée avec métadonnées.

## 3. Diagramme de séquence illustratif

~~~mermaid
sequenceDiagram
 participant U as Utilisateur
 participant C as Cache sémantique
 participant M as RAG / Modèle
 U->>C: « Que signifie un statut de paiement inconnu ? »
 C->>C: ACL + version + voisinage
 alt Hit sûr
 C-->>U: Explication standard datée
 else Miss / ACL incompatible
 C->>M: Inférence documentée
 M-->>C: Réponse validée
 C-->>U: Réponse fraîche
 end
~~~

**Scénario :** Une FAQ **publique** sur le sens d'un timeout peut être cachée. En revanche, une question « quel est l'état de MON virement ? » ne doit pas servir une réponse semantiquement voisine correspondant à un autre ordre ou un autre client.

## 4. Décisions à prendre en Design Authority

- Définir explicitement types cachables, scopes, versions de documents et clé d'isolation.
- Découpler cache public de données sensibles / personnelles ; TTL par criticité.
- Définir mesure de similarité et seuil avec faux hits et miss rates.
- Déclencher invalidation lors du changement de procédures et du registre de modèles.
- Mesurer hit rate valide, latence, coût économisé, taux d'erreur et fuite inter-tenant (cible 0).

## 5. Scénarios de panne et parades

| Échec / attaque | Comportement attendu |
|---|---|
| Collision entre clients | Partitionner par habilitation et contexte ; sinon ne pas cacher. |
| Réponse périmée | Version du corpus/TTL et invalidation événementielle. |
| Similarité change le sens | Seuil conservateur + réponse réservée à FAQ stable. |
| Donnée sensible dans cache partagé | Bloquer l'écriture et tracer la politique. |

## 6. Tests d'acceptation

1. Questions similaires de deux tenants ne partagent pas une réponse confidentielle.
2. Après changement de procédure, ancien cache invalidé.
3. Une requête sur paiement individuel ignore Semantic Cache.
4. Évaluer faux hits pour questions « accepté » versus « réglé ».

**Critère transversal :** chaque décision sensible est explicable, les identités et autorisations sont contrôlées par code, et les exemples n'exécutent aucune opération bancaire réelle.

## 7. Compromis, limites et sélection

Bénéfice en FAQ répétitive ; dangereux sans politique d'isolation. Cache de réponse générative ≠ cache de statut financier autoritatif.

À mesurer sur un jeu de référence : **qualité métier, confidentialité, latence p95/p99, coût par demande, robustesse aux attaques et taux d'abstention**. Documenter configuration, modèle, version, corpus et politique.

## 8. Question d'entretien

**Question :** Peut-on cacher le statut personnel d'un paiement par similarité ?

**Réponse :** Non comme réponse partagée ; c'est une donnée transactionnelle spécifique et soumise à des permissions et à la fraîcheur.

## 9. Mise en œuvre et approfondissement

- Plateforme de référence : API sécurisée, orchestration Java ou Python sur Kubernetes/OpenShift, logs et métriques structurés ; aucun produit commercial imposé.
- [Architecture IA de bout en bout](../reference-ai-platform-openshift/README.md) · [Matrice de sélection](../PATTERNS_DECISION_MATRIX.md) · [Sources techniques](../REFERENCES.md).
- Les mécanismes de sécurité doivent être vérifiés indépendamment des réponses du LLM ; aucun prompt ne remplace AuthZ ou la validation d'un outil.
