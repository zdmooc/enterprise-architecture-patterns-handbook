# 11 — AI Gateway — contrôle des accès aux modèles

> Architecture pédagogique et générique. Aucune infrastructure, organisation ni entreprise réelle n'est identifiée. Les exemples de données et seuils sont fictifs.

## 1. Besoin et contexte
Centraliser authentification des consommateurs, limitation de tokens et coûts, routage, observabilité et application des politiques avant l'inférence. L'AI Gateway ne remplace ni les contrôles de contenu ni l'autorisation métier.

**Exemple concret :** Un assistant documentaire envoie une demande d'inférence. La passerelle refuse un modèle hors périmètre et vérifie le quota du tenant.

## 2. Schéma de composants
~~~mermaid
flowchart TB
 U["Client IA"] --> IAM["Identité / tenant / scopes"]
 IAM --> G["AI Gateway"]
 G --> P["Politiques données, région, quotas, budget"]
 P --> R["Model Router"]
 R --> L["Serving de modèles autorisés"]
 L --> O["Validation réponse"]
 O --> G
 G --> U
 G --> MET["Audit / tokens / coût / latence"]
~~~

## 3. Diagramme de séquence
~~~mermaid
sequenceDiagram
 participant C as Client
 participant G as AI Gateway
 participant P as Policy Engine
 participant M as Modèle autorisé
 C->>G: Inferer + tenant + correlationId
 G->>P: Vérifier classe des données et budget
 P-->>G: ALLOW pour modèle local
 G->>M: Appel avec timeout borné
 M-->>G: Résultat + consommation
 G-->>C: Résultat filtré
 G->>G: Trace coût et version
~~~

## 4. Étapes de conception
1. Fournir une API unique par tenant et versionner les contrats de requêtes/réponses.
2. Contrôler token et droits d'accès au **modèle**, puis classification et choix de destination conformes.
3. Limiter débit, tokens entrée/sortie, concurrence et budget monétaire (unité interne si pricing absent).
4. Routage vers modèles **déjà autorisés**; ne jamais envoyer des données sensibles à un fallback non conforme.
5. Gestion des timeouts, circuit breakers et backpressure; distinction erreurs d'inférence vs décisions métier.
6. Enregistrer modelId/modelVersion, promptVersion, policyVersion, latence et quantité de tokens sans journaux de secrets.

## 5. Contrat illustratif
~~~json
{"tenantId":"tenant-demo","requestId":"req-11",
 "dataClass":"internal","modelPolicy":"v1",
 "timeoutMs":2500,"maxBudgetUnits":10,"auditCorrelation":"trace-demo"}
~~~
L'enveloppe est pédagogique. Les budgets et permissions sont appliqués dans les services déterministes, jamais par confiance envers un prompt ou une sortie probabiliste.

## 6. Erreurs à prévoir et plan de tests
- **AI-11-T1 :** Un utilisateur non autorisé à un modèle reçoit un refus avant inférence.
- **AI-11-T2 :** Un quota épuisé bloque les nouveaux appels sans dépassement silencieux.
- **AI-11-T3 :** Un modèle non conforme n'est jamais sélectionné lors d'une panne.
- **AI-11-T4 :** Trace corrélée disponible sans données classifiées en clair.

**Observabilité et qualité :** limites économiques, taux d'erreurs, p95/p99, débits, qualité par version de modèle, policy-deny et absence de fuite.

## 7. Arbitrages et limites
Une API Gateway protège l'entrée générale HTTP ; une AI Gateway ajoute contrôles d'inférence (tokens, coûts, modèles et politiques). Les deux fonctions peuvent partager une plateforme mais restent distinctes.

## 8. Questions d'entretien d'architecture
- **Quel problème est résolu ?** Centraliser authentification des consommateurs, limitation de tokens et coûts, routage, observabilité et application des politiques avant l'inférence. L'AI Gateway ne remplace ni les contrôles de contenu ni l'autorisation métier.
- **Pourquoi ne pas ajouter ce composant partout ?** Cela augmente coût et complexité ; justifier un gain mesuré avec un corpus de référence, un SLO et des limites de confidentialité.
- **Qu'apporte OpenShift ?** Disponibilité des workloads, isolation des namespaces/réseaux, secrets, déploiement contrôlé et métriques; pas de garantie sur l'exactitude des inférences.
- **Quels tests conditionnent le GO ?** Identité/ACL, tests adversariaux, panne d'inférence, version du modèle, contrôles de coût et retour à un état sûr.

## 9. Voir aussi
- [Étude d'architecture IA intégrée](../case-study-ai-platform-openShift/README.md)
- [Matrice de décision AI](../references/decision-matrix.md)
- [Évaluation de la sécurité et de la qualité](../references/risks-evaluation.md)
