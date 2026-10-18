# 15 — Event-Driven AI — inférence déclenchée par événements

> Architecture pédagogique et générique. Aucune infrastructure, organisation ni entreprise réelle n'est identifiée. Les exemples de données et seuils sont fictifs.

## 1. Besoin et contexte
Déclencher une inférence à partir de changements d'état ou messages, sans coupler le système transactionnel aux délais d'un LLM. Conserver corrélation, déduplication et décision humaine lorsque nécessaire.

**Exemple concret :** Un événement d'incident cluster déclenche une analyse IA pour proposer un diagnostic. Le service d'exploitation continue même si l'IA est indisponible.

## 2. Schéma de composants
~~~mermaid
flowchart TB
 S["Système opérationnel"] -->|"Event IncidentDetected"| B["Broker / Topic"]
 B --> I["Consumer idempotent"]
 I --> Q["File d'inférences bornée"]
 Q --> L["Service IA d'analyse"]
 L --> V["Validation + réduction de risque"]
 V --> R["Proposition / ticket"]
 V -.-> H["Approbation humaine avant toute action"]
 I --> D[("Inbox : events déjà traités")]
~~~

## 3. Diagramme de séquence
~~~mermaid
sequenceDiagram
 participant S as Source
 participant B as Broker
 participant C as Consumer
 participant L as Modèle IA
 participant H as Analyste
 S->>B: IncidentDetected(id=E-001)
 B->>C: E-001 (peut être redélivré)
 C->>C: Inbox déduplication
 C->>L: Analyse avec deadline
 L-->>C: Diagnostic suggéré
 C-->>H: Ticket sourcé / pas de mutation
 B->>C: Redélivrance E-001
 C-->>B: Déjà traité, aucune 2e action
~~~

## 4. Étapes de conception
1. Émettre des faits métiers versionnés seulement après transition durable de la source.
2. Consommer avec Inbox/déduplication et filtrage des données sensibles.
3. Classer les événements par urgence et allouer budget inferencing et deadline.
4. Isoler les files d'inférence : panne IA ne doit pas bloquer un flux métier critique.
5. Conserver eventId, causationId, sourceVersion et status; gérer ordre et événements expirés.
6. Stocker diagnostics IA comme **propositions**, pas états financiers ou opérationnels autoritatifs.

## 5. Contrat illustratif
~~~json
{"tenantId":"tenant-demo","requestId":"req-15",
 "dataClass":"internal","modelPolicy":"v1",
 "timeoutMs":2500,"maxBudgetUnits":10,"auditCorrelation":"trace-demo"}
~~~
L'enveloppe est pédagogique. Les budgets et permissions sont appliqués dans les services déterministes, jamais par confiance envers un prompt ou une sortie probabiliste.

## 6. Erreurs à prévoir et plan de tests
- **AI-15-T1 :** Broker redélivre un événement → aucun ticket ou effet métier non souhaité en double.
- **AI-15-T2 :** Modèle inaccessible → message rejouable borné ou DLQ, flux transactionnel reste indépendant.
- **AI-15-T3 :** Événement expiré → abstention/routage investigation, pas action rétroactive.
- **AI-15-T4 :** Message contient prompt malveillant → aucune élévation de droit.

**Observabilité et qualité :** event-to-insight-lag p95, age oldest event, ML processing-errors, déduplication, coût/événement, taux faux positif.

## 7. Arbitrages et limites
Ne pas déclencher une dépense, un débit, une suppression Kubernetes ou une autre action sensible sur une **simple sortie d'IA**. L'événement n'autorise pas l'action.

## 8. Questions d'entretien d'architecture
- **Quel problème est résolu ?** Déclencher une inférence à partir de changements d'état ou messages, sans coupler le système transactionnel aux délais d'un LLM. Conserver corrélation, déduplication et décision humaine lorsque nécessaire.
- **Pourquoi ne pas ajouter ce composant partout ?** Cela augmente coût et complexité ; justifier un gain mesuré avec un corpus de référence, un SLO et des limites de confidentialité.
- **Qu'apporte OpenShift ?** Disponibilité des workloads, isolation des namespaces/réseaux, secrets, déploiement contrôlé et métriques; pas de garantie sur l'exactitude des inférences.
- **Quels tests conditionnent le GO ?** Identité/ACL, tests adversariaux, panne d'inférence, version du modèle, contrôles de coût et retour à un état sûr.

## 9. Voir aussi
- [Étude d'architecture IA intégrée](../case-study-ai-platform-openShift/README.md)
- [Matrice de décision AI](../references/decision-matrix.md)
- [Évaluation de la sécurité et de la qualité](../references/risks-evaluation.md)
