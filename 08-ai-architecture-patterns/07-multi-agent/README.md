# 07 — Multi-Agent : coopération spécialisée

> **Famille :** IA agentique · **Référentiel pédagogique anonymisé**. Aucun client ni fournisseur réel n'est identifié.

## 1. Définition et problème métier

Plusieurs agents aux rôles distincts se coordonnent pour réaliser des sous-tâches. La répartition peut être hiérarchique (superviseur) ou fondée sur un protocole de collaboration ; elle n'améliore pas automatiquement la qualité.

**Pourquoi :** Un dossier d'architecture exige expertise sécurité, plateforme, intégration et exploitation. Un seul agent peut mélanger hypothèses et conclusions ou surcharger son contexte.

## 2. Architecture logique

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

### Déroulement

1. Décomposer le dossier en missions indépendantes : sécurité, flux, performance, coûts.
2. Définir contrat d'entrée/sortie et propriétaire de chaque sous-tâche.
3. Attribuer à chaque agent une identité limitée et, idéalement, aucun outil de mutation.
4. Faire exécuter les sous-tâches en parallèle sous quotas de temps et tokens.
5. Rassembler et confronter les résultats ; dédoublonner les affirmations, relever contradictions et niveaux de preuve.
6. Un validateur indépendant ou expert humain arbitre ; l'agent superviseur ne transforme pas la discussion en vérité sans contrôle.

## 3. Séquence métier illustrative

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

## 4. Arbitrages d'architecture

- Spécialisation utile seulement si les tâches sont réellement séparables.
- Définir protocole, format JSON, provenance et limites d'accès par agent.
- Prévenir les boucles interagents et l'explosion de coût/tokens.
- Identité distincte et permissions minimales ; le coordinateur n'hérite pas de tous les privilèges.
- Évaluer gain de qualité contre modèle mono-agent sur même dataset.

## 5. Scénarios de panne et attaques

| Incident | Parade |
|---|---|
| Deux agents donnent des conclusions contradictoires | Conserver les deux preuves et déclencher revue. |
| Agent spécialisé extrapole hors domaine | Validation par contrat de rôle et source. |
| Fuite inter-agent de données sensibles | Isolation des espaces et consentements par audience. |
| Cycles et amplification des coûts | Budget et fan-out maximum. |

## 6. Tests de qualification

1. Sous-agent ne consulte pas corpus d'un autre domaine interdit.
2. Protocole de réponse malformé conduit à échec contrôlé.
3. Deux réponses contradictoires sont signalées.
4. Évaluer multi-agent contre baseline mono-agent à budget égal.

**Critère transversal :** aucun accès à un compte ni changement financier sans la politique du système exécutant et son autorisation explicite.

## 7. Quand choisir, quand éviter

La coopération ajoute latence, coût et surface d'attaque ; commencer mono-agent puis prouver le bénéfice.

Mesurer sur un jeu d'essais : qualité, fidélité aux preuves, coût, latence p95/p99, permissions effectivement imposées et sécurité face aux contenus non fiables.

## 8. Question d'entretien

**Question :** Plus d'agents rendent-ils une architecture automatiquement meilleure ?

**Réponse :** Non ; ils peuvent produire davantage de messages, de contradictions et de coûts. Justifier par métriques sur cas de référence.

## 9. Mise en œuvre / prolongements

- Services Java ou Python sur Kubernetes/OpenShift, policy engine et métriques, sans dépendance obligatoire à un éditeur particulier.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice des patterns](../PATTERNS_DECISION_MATRIX.md) · [Références](../REFERENCES.md).
- Ne jamais confondre **proposition générée**, **approbation** et **exécution réellement confirmée**.
