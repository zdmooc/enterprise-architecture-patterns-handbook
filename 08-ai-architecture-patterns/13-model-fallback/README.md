# 13 — Model Fallback — continuité d'inférence

> Architecture pédagogique et générique. Aucune infrastructure, organisation ni entreprise réelle n'est identifiée. Les exemples de données et seuils sont fictifs.

## 1. Besoin et contexte
Lorsqu'un endpoint IA est indisponible ou saturé, proposer une alternative **autorisée et évaluée**, sans compromettre classification des données, qualité minimale ou format de sortie.

**Exemple concret :** Un modèle de résumé local est indisponible : une version secondaire locale évaluée peut prendre le relais, mais un modèle situé hors du périmètre confidentiel ne peut pas être choisi.

## 2. Schéma de composants
~~~mermaid
flowchart TB
 U["Requête + classification"] --> P["Politique tenant / données"]
 P --> M1["Modèle primaire autorisé"]
 M1 --> OK{"Réponse conforme avant deadline ?"}
 OK -->|Oui| O["Réponse validée"]
 OK -->|Non| F{"Fallback compatible et autorisé ?"}
 F -->|Oui| M2["Modèle secondaire évalué"]
 M2 --> V["Validation format / qualité / coûts"]
 V --> O
 F -->|Non| X["Échec explicite / abstention"]
~~~

## 3. Diagramme de séquence
~~~mermaid
sequenceDiagram
 participant C as Client
 participant G as Gateway
 participant M1 as Modèle principal
 participant M2 as Modèle secondaire
 C->>G: Demande confidentielle
 G->>M1: Inferer sous budget
 M1--xG: 503
 G->>G: Vérifier politique + compatibilité + temps restant
 G->>M2: Inferer, même périmètre autorisé
 M2-->>G: Résultat
 G-->>C: Résultat validé / provenance de version
~~~

## 4. Étapes de conception
1. Établir matrice de compatibilité entre modèles : données autorisées, classe de tâche, qualité, contexte, JSON/schema et région.
2. Limiter fallback à quelques destinations préautorisées; pas de parcours aléatoire.
3. Appliquer circuit breaker et timeout sur le primaire, conserver un budget restant pour la tentative.
4. Sur état ambigu d'une action exécutée via agent, ne pas relancer l'**action** lors du changement de modèle.
5. Valider réponse du modèle secondaire avec les mêmes guardrails et les mêmes droits.
6. Journaliser route, motif, version et impact sur le coût/qualité pour audit.

## 5. Contrat illustratif
~~~json
{"tenantId":"tenant-demo","requestId":"req-13",
 "dataClass":"internal","modelPolicy":"v1",
 "timeoutMs":2500,"maxBudgetUnits":10,"auditCorrelation":"trace-demo"}
~~~
L'enveloppe est pédagogique. Les budgets et permissions sont appliqués dans les services déterministes, jamais par confiance envers un prompt ou une sortie probabiliste.

## 6. Erreurs à prévoir et plan de tests
- **AI-13-T1 :** Modèle secondaire hors politique → refus au lieu de fallback.
- **AI-13-T2 :** Modèle secondaire renvoie JSON incompatible → rejet.
- **AI-13-T3 :** Échec du primaire après action outil incertaine → aucune nouvelle exécution sans réconciliation.
- **AI-13-T4 :** Tempête de retries simultanés → concurrence et nombre de tentatives plafonnés.

**Observabilité et qualité :** fallback-rate, quality-delta, policy violations, p95, error-budget, extra-cost et taux de réussite de reprise.

## 7. Arbitrages et limites
Fallback n'est pas haute disponibilité du **même état** : les modèles peuvent diverger de capacités, de contexte et de sorties. Pour décisions sensibles, abstention préférable à une qualité inférieure non validée.

## 8. Questions d'entretien d'architecture
- **Quel problème est résolu ?** Lorsqu'un endpoint IA est indisponible ou saturé, proposer une alternative **autorisée et évaluée**, sans compromettre classification des données, qualité minimale ou format de sortie.
- **Pourquoi ne pas ajouter ce composant partout ?** Cela augmente coût et complexité ; justifier un gain mesuré avec un corpus de référence, un SLO et des limites de confidentialité.
- **Qu'apporte OpenShift ?** Disponibilité des workloads, isolation des namespaces/réseaux, secrets, déploiement contrôlé et métriques; pas de garantie sur l'exactitude des inférences.
- **Quels tests conditionnent le GO ?** Identité/ACL, tests adversariaux, panne d'inférence, version du modèle, contrôles de coût et retour à un état sûr.

## 9. Voir aussi
- [Étude d'architecture IA intégrée](../case-study-ai-platform-openShift/README.md)
- [Matrice de décision AI](../references/decision-matrix.md)
- [Évaluation de la sécurité et de la qualité](../references/risks-evaluation.md)
