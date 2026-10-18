# 14 — Continuous Evaluation — qualité, sécurité et dérive

> Architecture pédagogique et générique. Aucune infrastructure, organisation ni entreprise réelle n'est identifiée. Les exemples de données et seuils sont fictifs.

## 1. Besoin et contexte
Mesurer continuellement performances et risques des applications IA en reliant versions du modèle, corpus, prompts, outils et politiques. Un jeu de tests hors ligne ne suffit pas à détecter toutes les dérives en production.

**Exemple concret :** Un assistant de procédures commence à citer des versions obsolètes après une réindexation de documents : des métriques et tests de non-régression doivent révéler cette dérive.

## 2. Schéma de composants
~~~mermaid
flowchart TB
 DATA["Jeu d'or versionné + questions difficiles"] --> RUN["Exécution offline et canary"]
 RUN --> MET["Qualité, groundedness, sécurité, latence, coût"]
 PROD["Traces de production anonymisées + feedback"] --> MET
 MET --> TH{"Seuils et tests négatifs satisfaits ?"}
 TH -->|Oui| PROMO["Promotion/maintien version"]
 TH -->|Non| BLOCK["Bloquer changement / rollback / analyse"]
 BLOCK --> DATA
~~~

## 3. Diagramme de séquence
~~~mermaid
sequenceDiagram
 participant CI as Pipeline
 participant E as Évaluateur
 participant R as Registry/manifest
 participant PROD as Production
 CI->>E: Évaluer model+prompt+index versionnés
 E-->>CI: Scores + tests adversariaux
 CI->>R: Promotion si seuils
 R->>PROD: Canary autorisé
 PROD-->>E: Métriques / dérive sans PII
 E-->>CI: Décision maintenir ou rollback
~~~

## 4. Étapes de conception
1. Créer des jeux d'or représentatifs avec droits d'accès et étiquettes de confiance.
2. Mesurer séparément retrieval, groundedness, exactitude métier, sécurité, biais et refus corrects.
3. Versionner corpus, modèle, prompt, route, outils et politique; le même test doit être reproductible.
4. Exécuter tests sur chaque changement, canary avant promotion et surveillance de dérive en production.
5. Échantillonner des traces anonymisées en respectant confidentialité et rétention; ne pas réentraîner avec des données client sans base légale.
6. Fixer seuils et responsables de décision; corriger puis rejouer la non-régression.

## 5. Contrat illustratif
~~~json
{"tenantId":"tenant-demo","requestId":"req-14",
 "dataClass":"internal","modelPolicy":"v1",
 "timeoutMs":2500,"maxBudgetUnits":10,"auditCorrelation":"trace-demo"}
~~~
L'enveloppe est pédagogique. Les budgets et permissions sont appliqués dans les services déterministes, jamais par confiance envers un prompt ou une sortie probabiliste.

## 6. Erreurs à prévoir et plan de tests
- **AI-14-T1 :** Prompt injection réussit sur banc d'essai → blocage déploiement.
- **AI-14-T2 :** Citation de document retiré → alerte de fraîcheur.
- **AI-14-T3 :** Le juge LLM note trop haut une réponse fausse → calibration humaine.
- **AI-14-T4 :** Hausse de coût et de p95 malgré qualité stable → revue avant promotion.

**Observabilité et qualité :** groundedness, factuality, precision citations, taux d'abstention, sécurité red-team, coût/tokens, p95, drift et accord juges humains.

## 7. Arbitrages et limites
Une bonne disponibilité technique d'inférence ne signifie pas qualité. L'évaluation ne doit pas faire appel uniquement au modèle évalué comme son propre juge.

## 8. Questions d'entretien d'architecture
- **Quel problème est résolu ?** Mesurer continuellement performances et risques des applications IA en reliant versions du modèle, corpus, prompts, outils et politiques. Un jeu de tests hors ligne ne suffit pas à détecter toutes les dérives en production.
- **Pourquoi ne pas ajouter ce composant partout ?** Cela augmente coût et complexité ; justifier un gain mesuré avec un corpus de référence, un SLO et des limites de confidentialité.
- **Qu'apporte OpenShift ?** Disponibilité des workloads, isolation des namespaces/réseaux, secrets, déploiement contrôlé et métriques; pas de garantie sur l'exactitude des inférences.
- **Quels tests conditionnent le GO ?** Identité/ACL, tests adversariaux, panne d'inférence, version du modèle, contrôles de coût et retour à un état sûr.

## 9. Voir aussi
- [Étude d'architecture IA intégrée](../case-study-ai-platform-openShift/README.md)
- [Matrice de décision AI](../references/decision-matrix.md)
- [Évaluation de la sécurité et de la qualité](../references/risks-evaluation.md)
