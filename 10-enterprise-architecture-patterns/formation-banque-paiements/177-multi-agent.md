# Cours 177 — Multi-Agent — Collaboration spécialisée · Architecture IA et agentique

> Cas fictif : banque pédagogique, suivi d'un virement SEPA de 500 EUR. La plateforme IA est **distincte du système autoritatif financier**. **Corrigé théorique fourni, exercice individuel non encore validé.**

## 1. Besoin et objectifs
Pour une étude d'architecture IA, plusieurs agents peuvent analyser API, sécurité et exploitation, mais leurs conclusions doivent être réunies avec preuve sans décision autonome de paiement.

## 2. Fonctionnement et HLD
~~~mermaid
flowchart LR
    A["Dossier d'architecture et tâches séparées"] --> B["Agents spécialisés avec scopes indépendants"]
    B --> C["Synthèse arbitrée et vérifiée"]
    B -. "Droits, preuve ou confiance insuffisants" .-> X["Refus / abstention / investigation"]
~~~

**Décision architecturale :** Partitionner les rôles et habilitations, distinguer outils et données, tracer les contributions, limiter boucles et coûts, consolider conflits via un évaluateur et un décideur humain.

## 3. Frontières de confiance
Multiplier les agents multiplie aussi les surfaces d'attaque, les coûts et les risques de propagation d'erreurs ; un agent critique ne s'autorise pas lui-même.

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
    participant A as Multi-Agent
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
- **Test de sécurité :** Un agent documentaire transmet une instruction hostile à l'agent outil : aucune permission supplémentaire accordée.
- **Test d'échec :** Deux agents émettent des recommandations contradictoires ; conserver les sources, signaler le conflit et s'abstenir sans arbitrage.
- **Révocation :** retirer un droit ou supprimer une source puis vérifier que résultat et cache ne la réexposent pas.
- **Timeout / reprise :** budget borné, pas de mutation répétée, statut bancaire consulté via système compétent.
- **Mesures de qualité :** Taux de résolution, erreurs croisées, propagation d'injection, coût total, latence, traçabilité.

## 6. ADR, compromis et non-garanties
Comparer systématiquement une solution plus simple, sans agent, ou avec un modèle local lorsque les NFR l'autorisent. Documenter résidence des données, coût, performance, périmètre d'outil, attaques indirectes et taux d'erreur acceptable.

## 7. Exercice corrigé
**Faut-il choisir multi-agent quand un RAG seul suffit ?**
- **A.** Non : préférer l'architecture minimale qui satisfait les besoins et preuves de qualité.
- **B.** Oui, plus d'agents garantit la justesse.
- **C.** Oui, car le nombre d'agents remplace l'audit.

**Bonne réponse théorique : A.** Non : préférer l'architecture minimale qui satisfait les besoins et preuves de qualité.

> L'exercice est disponible pour auto-étude ; aucun score individuel n'est déclaré.

## 8. Fiche de référence existante — approfondissement
[Fiche source détaillée](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/07-multi-agent/README.md)

> **Famille :** IA agentique · **Référentiel pédagogique anonymisé**. Aucun client ni fournisseur réel n'est identifié.

#### 1. Définition et problème métier

Plusieurs agents aux rôles distincts se coordonnent pour réaliser des sous-tâches. La répartition peut être hiérarchique (superviseur) ou fondée sur un protocole de collaboration ; elle n'améliore pas automatiquement la qualité.

**Pourquoi :** Un dossier d'architecture exige expertise sécurité, plateforme, intégration et exploitation. Un seul agent peut mélanger hypothèses et conclusions ou surcharger son contexte.

#### 2. Architecture logique

~~~mermaid
flowchart TB
 U["Demande de dossier architecture IA"] --> SUP["Coordinateur"]
 SUP --> SEC["Agent sécurité (lecture)"]
 SUP --> INT["Agent intégration (lecture)"]
 SUP --> PERF["Agent performance (lecture)"]
 SEC --> MERGE["Consolidation + provenance"]
 INT --> MERGE
 PERF --> MERGE
 MERGE --> REVIEW["Évaluation des contradictions"]
 REVIEW --> HUMAN["Revue architecte humain"]
~~~

#### Déroulement

1. Décomposer le dossier en missions indépendantes : sécurité, flux, performance, coûts.
2. Définir contrat d'entrée/sortie et propriétaire de chaque sous-tâche.
3. Attribuer à chaque agent une identité limitée et, idéalement, aucun outil de mutation.
4. Faire exécuter les sous-tâches en parallèle sous quotas de temps et tokens.
5. Rassembler et confronter les résultats ; dédoublonner les affirmations, relever contradictions et niveaux de preuve.
6. Un validateur indépendant ou expert humain arbitre ; l'agent superviseur ne transforme pas la discussion en vérité sans contrôle.

#### 3. Séquence métier illustrative

~~~mermaid
sequenceDiagram
 actor U as Architecte
 participant C as Coordinateur
 participant A as Sécurité
 participant B as Intégration
 participant E as Évaluateur
 U->>C: Étude générique d'API IA
 par Analyses parallèles
 C->>A: Analyse menace
 A-->>C: Contrôles, références
 and
 C->>B: Contrats d'intégration
 B-->>C: Flux, hypothèses
 end
 C->>E: Comparer conclusions et preuves
 E-->>U: Dossier + désaccords explicités
~~~

**Exemple :** Un assistant de conception de plateforme évalue un service IA sur OpenShift. Un agent analyse NetworkPolicy et IAM, un autre la chaîne RAG, un troisième les SLO. Le coordinateur remet **les désaccords non résolus**, sans déployer de configuration.

#### 4. Arbitrages d'architecture

- Spécialisation utile seulement si les tâches sont réellement séparables.
- Définir protocole, format JSON, provenance et limites d'accès par agent.
- Prévenir les boucles interagents et l'explosion de coût/tokens.
- Identité distincte et permissions minimales ; le coordinateur n'hérite pas de tous les privilèges.
- Évaluer gain de qualité contre modèle mono-agent sur même dataset.

#### 5. Scénarios de panne et attaques

| Incident | Parade |
|---|---|
| Deux agents donnent des conclusions contradictoires | Conserver les deux preuves et déclencher revue. |
| Agent spécialisé extrapole hors domaine | Validation par contrat de rôle et source. |
| Fuite inter-agent de données sensibles | Isolation des espaces et consentements par audience. |
| Cycles et amplification des coûts | Budget et fan-out maximum. |

#### 6. Tests de qualification

1. Sous-agent ne consulte pas corpus d'un autre domaine interdit.
2. Protocole de réponse malformé conduit à échec contrôlé.
3. Deux réponses contradictoires sont signalées.
4. Évaluer multi-agent contre baseline mono-agent à budget égal.

**Critère transversal :** aucun accès à un compte ni changement financier sans la politique du système exécutant et son autorisation explicite.

#### 7. Quand choisir, quand éviter

La coopération ajoute latence, coût et surface d'attaque ; commencer mono-agent puis prouver le bénéfice.

Mesurer sur un jeu d'essais : qualité, fidélité aux preuves, coût, latence p95/p99, permissions effectivement imposées et sécurité face aux contenus non fiables.

#### 8. Question d'entretien

**Question :** Plus d'agents rendent-ils une architecture automatiquement meilleure ?

**Réponse :** Non ; ils peuvent produire davantage de messages, de contradictions et de coûts. Justifier par métriques sur cas de référence.

#### 9. Mise en œuvre / prolongements

- Services Java ou Python sur Kubernetes/OpenShift, policy engine et métriques, sans dépendance obligatoire à un éditeur particulier.
- [Plateforme IA de référence](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- Ne jamais confondre **proposition générée**, **approbation** et **exécution réellement confirmée**.

[Programme des cours](README.md) · [Exercices IA 171–185](exercices-et-corriges/cours-171-185.md)
