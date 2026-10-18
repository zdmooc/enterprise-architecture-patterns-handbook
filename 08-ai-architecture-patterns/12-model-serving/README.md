# 12 — Model Serving — exposer l'inférence sur Kubernetes/OpenShift

> Architecture pédagogique et générique. Aucune infrastructure, organisation ni entreprise réelle n'est identifiée. Les exemples de données et seuils sont fictifs.

## 1. Besoin et contexte
Déployer un modèle comme un service versionné avec capacité, sécurisation et objectifs de latence contrôlés. Ne pas confondre entraînement, packaging et inférence.

**Exemple concret :** Une plateforme fictive héberge deux modèles sous différents profils CPU/GPU; l'AI Gateway les appelle uniquement lorsque disponibles.

## 2. Schéma de composants
~~~mermaid
flowchart TB
 A["AI Gateway"] --> S["Service HTTP d'inférence"]
 S --> RT["Runtime de modèles"]
 RT --> M[("Artefacts de modèle versionnés et signés")]
 RT --> GPU["Pods CPU/GPU"]
 RT --> OBS["Métriques : queue, tokens/s, p95"]
 S --> AUTO["Autoscaling sous contraintes capacité"]
 AUTO --> GPU
~~~

## 3. Diagramme de séquence
~~~mermaid
sequenceDiagram
 participant G as AI Gateway
 participant S as Serving
 participant Q as Queue interne bornée
 participant R as Runtime du modèle
 G->>S: /infer + modelVersion
 S->>Q: Admission si capacité
 Q->>R: Inference
 R-->>S: Résultat + tokens
 S-->>G: Réponse et version
 Note over S,R: En surcharge, rejet ou attente bornée
~~~

## 4. Étapes de conception
1. Publier artefact modèle immuable, checksum/signature, licence d'usage et version de tokenizer.
2. Construire une image de serving reproductible, non-root, ressources CPU/GPU et mémoire explicites.
3. Prévoir quotas GPU, placement, affinity, storage et secrets sans fuite de modèle.
4. Décider autoscaling HPA/événementiel et minReplicas selon mode d'exécution; ne pas présumer que scale-to-zero marche partout.
5. Encadrer longueur de contexte, concurrence, file d'attente, timeout de génération et politique d'admission.
6. Déployer canary, mesurer p95/p99, qualité et rollback fonctionnel; gérer version de contrat/model.

## 5. Contrat illustratif
~~~json
{"tenantId":"tenant-demo","requestId":"req-12",
 "dataClass":"internal","modelPolicy":"v1",
 "timeoutMs":2500,"maxBudgetUnits":10,"auditCorrelation":"trace-demo"}
~~~
L'enveloppe est pédagogique. Les budgets et permissions sont appliqués dans les services déterministes, jamais par confiance envers un prompt ou une sortie probabiliste.

## 6. Erreurs à prévoir et plan de tests
- **AI-12-T1 :** Pod d'inférence perdu → routage vers réplica sain sans résultat inventé.
- **AI-12-T2 :** OOM GPU ou dépassement KV-cache → rejet contrôlé, métrique et adaptation de concurrence.
- **AI-12-T3 :** Modèle modifié sans version → test de provenance bloquant.
- **AI-12-T4 :** Échelle à zéro nécessitant cold start → latence SLO documentée, pas présumée.

**Observabilité et qualité :** tokens/s, TTFT, tokens par réponse, p95/p99, queue depth, GPU utilization/memory, erreurs et coût par million de tokens.

## 7. Arbitrages et limites
L'hébergement sur Kubernetes/OpenShift ne rend pas un modèle plus exact. Le mode autoscaling et ses capacités (notamment mise à zéro) dépendent des contrôleurs installés, de la configuration et du runtime.

## 8. Questions d'entretien d'architecture
- **Quel problème est résolu ?** Déployer un modèle comme un service versionné avec capacité, sécurisation et objectifs de latence contrôlés. Ne pas confondre entraînement, packaging et inférence.
- **Pourquoi ne pas ajouter ce composant partout ?** Cela augmente coût et complexité ; justifier un gain mesuré avec un corpus de référence, un SLO et des limites de confidentialité.
- **Qu'apporte OpenShift ?** Disponibilité des workloads, isolation des namespaces/réseaux, secrets, déploiement contrôlé et métriques; pas de garantie sur l'exactitude des inférences.
- **Quels tests conditionnent le GO ?** Identité/ACL, tests adversariaux, panne d'inférence, version du modèle, contrôles de coût et retour à un état sûr.

## 9. Voir aussi
- [Étude d'architecture IA intégrée](../case-study-ai-platform-openShift/README.md)
- [Matrice de décision AI](../references/decision-matrix.md)
- [Évaluation de la sécurité et de la qualité](../references/risks-evaluation.md)
