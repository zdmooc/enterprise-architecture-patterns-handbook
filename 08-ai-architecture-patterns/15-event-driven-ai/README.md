# 15 — Event-Driven AI

> **Famille :** Production / IA événementielle · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

## 1. Définition et besoin

Déclencher une inférence ou un agent à partir d'un événement de domaine publié par un système autoritatif. L'IA reste un consommateur dérivé ; son résultat est une **analyse/proposition**, pas une preuve financière ni une commande implicite.

**Problème :** Un incident technique ou un paiement au statut incertain doit déclencher une analyse documentaire assistée sans ralentir le règlement et sans exécuter une transaction.

## 2. Architecture logique

~~~mermaid
flowchart TB
 CORE["Service métier autoritatif"] --> OUT["État durable + Outbox"]
 OUT --> BUS["Broker : event incident détecté"]
 BUS --> IA["Worker IA, idempotent"]
 IA --> RAG["RAG des runbooks autorisés"]
 RAG --> LLM["LLM local"]
 LLM --> REPORT["Rapport d'investigation suggéré"]
 REPORT --> HUMAN["Expert humain : décision"]
 BUS --> MON["Autres consommateurs métier"]
~~~

### Déroulement

1. Publier un événement post-commit avec eventId, schemaVersion, correlationId et classification.
2. Livrer dans un broker durable et appliquer contrôle d'accès des abonnés.
3. Consommateur IA traite événements idempotemment, valide schémas, TTL et règle d'admission.
4. Assembler contexte RAG autorisé puis générer un rapport, un score ou une recommandation.
5. Enregistrer résultat dérivé, provenance, version modèle et lien vers événement source.
6. Pour agir, traverser policy engine + outil autorisé et HITL si action sensible.
7. Sur échec, retry borné, DLQ/parking et backpressure, sans bloquer le système de paiement.

## 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
 participant S as Service métier
 participant B as Broker
 participant A as Worker IA
 participant R as RAG
 participant H as Analyste
 S->>B: PaymentStatusUnknown(eventId=E01)
 B->>A: Redélivrance possible E01
 A->>A: Inbox / déduplication E01
 A->>R: Chercher runbook autorisé
 R-->>A: Sections validées
 A-->>H: Diagnostic hypothétique sourcé
 Note over A,H: Pas d'exécution du virement depuis IA
~~~

**Exemple pratique :** Un événement fictif `PaymentConfirmationMissing` déclenche un assistant qui retrouve la procédure de rapprochement et crée une fiche d'investigation. Il n'émet aucun paiement ni mouvement sur compte.

## 4. Décisions d'architecture

- Événements d'affaires et d'exploitation différenciés, contrat schema/owner, horodatage/TTL.
- Consommateur IA isolé, quotas de ressources pour ne pas saturer le chemin critique.
- Déduplication inbox pour ne pas dupliquer coûts, notifications ni tickets.
- Guardrails sur données transportées et RAG ; aucune donnée sensible inutile dans le topic.
- Budgets de latence distincts du rail de paiement, observabilité et indicateurs de fraîcheur.

## 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| Broker redélivre 10 fois | Inbox durable, un seul résultat logique. |
| Modèle indisponible | Queue/backpressure/parking selon TTL ; règlement indépendant. |
| Événement frauduleux ou non autorisé | Authentification broker, ACL, validation signatures/schémas. |
| Diagnostic IA pris pour fait bancaire | Étiqueter comme recommandation ; preuve financière demeure au core. |
| Retards et événements expirés | Conserver statut de traitement, écarter résultat obsolète. |

## 6. Tests et preuves attendues

1. Duplicate eventId ne crée pas deux investigations.
2. AI worker indisponible ne ralentit pas le traitement financier.
3. Résultat est marqué « suggestion » et cite un runbook.
4. Event source non authentifiée ne déclenche pas d'outil.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

## 7. Compromis et critères de choix

Très utile pour surveillance, support et enrichissement asynchrone. Ne pas insérer un LLM lent dans le chemin réglementaire du règlement sans nécessité démontrée.

## 8. Question d'entretien

**Question :** L'IA peut-elle publier PaymentSettled à partir d'un score de confiance ?

**Réponse :** Non, seul le système financier autoritatif peut attester le règlement. L'IA peut publier une observation ou recommandation distincte.

## 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice](../PATTERNS_DECISION_MATRIX.md) · [Sources](../REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.
