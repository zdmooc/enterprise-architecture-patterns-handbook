# Cours 174 — Semantic Cache — Réutilisation contrôlée · Architecture IA et agentique

> Cas fictif : banque pédagogique, suivi d'un virement SEPA de 500 EUR. La plateforme IA est **distincte du système autoritatif financier**. **Corrigé théorique fourni, exercice individuel non encore validé.**

## 1. Besoin et objectifs
Des analystes posent souvent la même question sur des procédures, mais les droits d'accès et versions peuvent changer.

## 2. Fonctionnement et HLD
~~~mermaid
flowchart LR
    A["Question + tenant + identité et politique"] --> B["Cache sémantique cloisonné et versionné"]
    B --> C["Réponse cache autorisée ou nouvel appel"]
    B -. "Droits, preuve ou confiance insuffisants" .-> X["Refus / abstention / investigation"]
~~~

**Décision architecturale :** Associer clé du cache au périmètre de droits, classification, version documentaire, modèle, politique et fenêtre de fraîcheur ; vérifier systématiquement les droits à l'utilisation.

## 3. Frontières de confiance
Une similarité de deux questions ne prouve ni égalité des permissions, ni validité temporelle du résultat.

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
    participant A as Semantic Cache
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
- **Test de sécurité :** L'utilisateur B pose une question proche de celle de A pour obtenir la réponse mise en cache : refus si ACL/tenant diffèrent.
- **Test d'échec :** Révoquer un droit, mettre à jour une procédure et comparer hit/miss ; aucune réponse obsolète ou d'un autre tenant.
- **Révocation :** retirer un droit ou supprimer une source puis vérifier que résultat et cache ne la réexposent pas.
- **Timeout / reprise :** budget borné, pas de mutation répétée, statut bancaire consulté via système compétent.
- **Mesures de qualité :** Cache hit valide, baisse des coûts, latence, invalidations, erreurs de fraîcheur et refus cross-tenant.

## 6. ADR, compromis et non-garanties
Comparer systématiquement une solution plus simple, sans agent, ou avec un modèle local lorsque les NFR l'autorisent. Documenter résidence des données, coût, performance, périmètre d'outil, attaques indirectes et taux d'erreur acceptable.

## 7. Exercice corrigé
**Quand une réponse sémantiquement proche peut-elle sortir du cache ?**
- **A.** Uniquement si les droits, le contexte, la version et la politique sont encore compatibles et vérifiés.
- **B.** Dès que la similarité cosinus est élevée.
- **C.** Après avoir masqué les identifiants tout en conservant le contenu confidentiel.

**Bonne réponse théorique : A.** Uniquement si les droits, le contexte, la version et la politique sont encore compatibles et vérifiés.

> L'exercice est disponible pour auto-étude ; aucun score individuel n'est déclaré.

## 8. Fiche de référence existante — approfondissement
[Fiche source détaillée](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/04-semantic-cache/README.md)

> **Famille :** IA générative · **Statut :** pattern d'architecture pédagogique · **Exemples fictifs et anonymisés**, aucun SI ou acteur d'entreprise réel revendiqué.

#### 1. Définition et problème

Cache des réponses récupérées à partir d'une proximité sémantique plutôt que d'une stricte égalité de chaîne. Sa réutilisation exige une identité de contexte, des permissions et des versions compatibles.

**Besoin métier :** Des milliers de questions proches sur une FAQ publique font refaire des inférences coûteuses ; un cache naïf peut toutefois divulguer à l'utilisateur B une réponse créée pour A.

#### 2. Architecture et flux

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

#### Étapes de traitement

1. Qualifier l'opération : ne mettre en cache que les réponses admissibles et non actionnelles.
2. Construire une clé englobant tenant, scopes, classification, collection documentaire/version, modèle/prompt/version et langue.
3. Rechercher candidats sémantiquement voisins avec seuil calibré.
4. Vérifier compatibilité stricte des droits et de la base documentaire AVANT lecture du résultat.
5. Appliquer durée de vie, invalidation par nouvelle procédure, et contrôle des résultats sensibles.
6. Sur miss, effectuer RAG/inférence ; après validation, stocker l'entrée avec métadonnées.

#### 3. Diagramme de séquence illustratif

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

#### 4. Décisions à prendre en Design Authority

- Définir explicitement types cachables, scopes, versions de documents et clé d'isolation.
- Découpler cache public de données sensibles / personnelles ; TTL par criticité.
- Définir mesure de similarité et seuil avec faux hits et miss rates.
- Déclencher invalidation lors du changement de procédures et du registre de modèles.
- Mesurer hit rate valide, latence, coût économisé, taux d'erreur et fuite inter-tenant (cible 0).

#### 5. Scénarios de panne et parades

| Échec / attaque | Comportement attendu |
|---|---|
| Collision entre clients | Partitionner par habilitation et contexte ; sinon ne pas cacher. |
| Réponse périmée | Version du corpus/TTL et invalidation événementielle. |
| Similarité change le sens | Seuil conservateur + réponse réservée à FAQ stable. |
| Donnée sensible dans cache partagé | Bloquer l'écriture et tracer la politique. |

#### 6. Tests d'acceptation

1. Questions similaires de deux tenants ne partagent pas une réponse confidentielle.
2. Après changement de procédure, ancien cache invalidé.
3. Une requête sur paiement individuel ignore Semantic Cache.
4. Évaluer faux hits pour questions « accepté » versus « réglé ».

**Critère transversal :** chaque décision sensible est explicable, les identités et autorisations sont contrôlées par code, et les exemples n'exécutent aucune opération bancaire réelle.

#### 7. Compromis, limites et sélection

Bénéfice en FAQ répétitive ; dangereux sans politique d'isolation. Cache de réponse générative ≠ cache de statut financier autoritatif.

À mesurer sur un jeu de référence : **qualité métier, confidentialité, latence p95/p99, coût par demande, robustesse aux attaques et taux d'abstention**. Documenter configuration, modèle, version, corpus et politique.

#### 8. Question d'entretien

**Question :** Peut-on cacher le statut personnel d'un paiement par similarité ?

**Réponse :** Non comme réponse partagée ; c'est une donnée transactionnelle spécifique et soumise à des permissions et à la fraîcheur.

#### 9. Mise en œuvre et approfondissement

- Plateforme de référence : API sécurisée, orchestration Java ou Python sur Kubernetes/OpenShift, logs et métriques structurés ; aucun produit commercial imposé.
- [Architecture IA de bout en bout](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice de sélection](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Sources techniques](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- Les mécanismes de sécurité doivent être vérifiés indépendamment des réponses du LLM ; aucun prompt ne remplace AuthZ ou la validation d'un outil.

[Programme des cours](README.md) · [Exercices IA 171–185](exercices-et-corriges/cours-171-185.md)
