# 06 — Planner–Executor

> **Famille :** IA agentique · **Référentiel pédagogique anonymisé**. Aucun client ni fournisseur réel n'est identifié.

## 1. Définition et problème métier

Sépare un **planificateur** qui propose une suite d'étapes d'un **exécuteur** qui réalise exclusivement les opérations autorisées et suit leur état. Le plan n'est pas une autorisation et ne garantit pas la faisabilité réelle.

**Pourquoi :** Un assistant chargé de préparer une analyse d'incident doit recueillir plusieurs preuves sans mélanger recherche, décision et action corrective.

## 2. Architecture logique

~~~mermaid
flowchart TB
 U["Objectif : comprendre une alerte de paiement"] --> P["Planner : plan structuré"]
 P --> RULE["Politique : outils de lecture uniquement"]
 RULE --> E["Executor durable"]
 E --> T1["Lire traces autorisées"]
 E --> T2["Consulter statut autoritatif"]
 E --> T3["Rassembler événements"]
 T1 --> V["Évaluer preuves et contraintes"]
 T2 --> V
 T3 --> V
 V --> R["Rapport sourcé ; actions proposées non exécutées"]
~~~

### Déroulement

1. Valider intention, acteur, données et périmètre.
2. Planner élabore un plan structuré : étapes, outils prévus, dépendances, critères d'arrêt.
3. Policy engine approuve les types d'outils, arguments, budgets et exigences de validation.
4. Executor traite les étapes de façon déterministe et persistante, selon deadline et quota.
5. Après chaque étape, contrôler résultat, état, autorisation et preuve ; réviser le plan si nécessaire, sans nouvelles permissions implicites.
6. Finaliser le rapport des résultats et des étapes non réalisées ; toute mutation sensible passe par une approbation humaine distincte.

## 3. Séquence métier illustrative

~~~mermaid
sequenceDiagram
 actor U as Analyste
 participant P as Planner
 participant S as Policy
 participant E as Executor
 participant T as Outils lecture
 U->>P: Dresser le diagnostic D-001
 P-->>S: Plan en 3 étapes, sans écriture
 S-->>E: Autoriser lecture, budget 3 appels
 E->>T: read_status
 T-->>E: Issue inconnue
 E->>T: read_log
 T-->>E: Réponse perdue
 E-->>U: Rapport, action manuelle préconisée
~~~

**Exemple :** Un paiement fictif est en statut « confirmation manquante ». Le planner propose de relire l'historique, le core et les événements ; l'exécuteur ne crée pas d'ordre de paiement et ne modifie aucune écriture.

## 4. Arbitrages d'architecture

- Format de plan typé et validé : étape, outil, dépendances, risque, coût.
- State store durable pour éviter de recommencer un outil d'écriture après crash.
- Timeout global et budget par étape, nombre maximal de replannings.
- Policy engine indépendant du plan et revérification à l'exécution.
- Séparer planification (probabiliste) et effet métier (déterministe/autorisations).

## 5. Scénarios de panne et attaques

| Incident | Parade |
|---|---|
| Étape non réalisable | Rapporter blocage et proposer adaptation contrôlée. |
| Plan modifié pour demander mutation | Revalidation de toutes les capacités/outils. |
| Crash après action externe | Idempotency-key et vérification statut réel. |
| Boucle de replanification | Compteur et deadline fixes. |

## 6. Tests de qualification

1. Plan qui demande un outil interdit est rejeté.
2. Même action ne s'exécute pas deux fois après interruption.
3. Les erreurs partielles restent visibles dans le résultat.
4. Le coût et le nombre d'étapes restent sous quota.

**Critère transversal :** aucun accès à un compte ni changement financier sans la politique du système exécutant et son autorisation explicite.

## 7. Quand choisir, quand éviter

Utile pour tâches longues à dépendances, moins adapté aux simples réponses documentaires. Attention au temps d'exécution et aux effets secondaires.

Mesurer sur un jeu d'essais : qualité, fidélité aux preuves, coût, latence p95/p99, permissions effectivement imposées et sécurité face aux contenus non fiables.

## 8. Question d'entretien

**Question :** Le planner peut-il accorder lui-même une autorisation métier ?

**Réponse :** Non : le plan est une proposition ; l'autorisation est une décision du système de politique et, le cas échéant, d'un humain habilité.

## 9. Mise en œuvre / prolongements

- Services Java ou Python sur Kubernetes/OpenShift, policy engine et métriques, sans dépendance obligatoire à un éditeur particulier.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice des patterns](../PATTERNS_DECISION_MATRIX.md) · [Références](../REFERENCES.md).
- Ne jamais confondre **proposition générée**, **approbation** et **exécution réellement confirmée**.
