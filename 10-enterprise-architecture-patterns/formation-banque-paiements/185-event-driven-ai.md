# Cours 185 — Event-Driven AI — IA événementielle sans effet financier · Architecture IA et agentique

> Banque fictive · ordre SEPA de 500 EUR. **Support pédagogique publié avec corrigé théorique ; aucun exercice individuel ni test sur cluster n'est déclaré validé.**

## 1. Besoin métier et problème
Un événement PaymentConfirmationMissing doit déclencher une assistance de diagnostic documentaire, sans ralentir le rail de règlement ni réémettre l'ordre bancaire.

## 2. HLD : responsabilités des composants
~~~mermaid
flowchart LR
    A["Source bancaire + Outbox"] --> B["Broker → IA worker idempotent"]
    B --> C["Rapport d'investigation + analyste"]
    B -. "Risque / absence de preuve" .-> STOP["Refus, attente ou abstention"]
~~~

**Décision d'architecture :** Consommer des événements versionnés avec eventId, tenant, classification, TTL et inbox de déduplication ; faire un RAG autorisé, produire une recommandation sourcée et demander HITL pour toute action sensible. Séparer budgets de l'IA et du paiement.

**Invariant à défendre :** Dix redélivrances du même événement créent au plus une investigation logique et aucun virement depuis l'agent IA.

## 3. Contrat de contrôle
~~~text
onEvent(event): dedupe(eventId); validatePolicyAndSchema(); produceInvestigationOnly(event); neverPublishSettlement()
~~~

Ce pseudo-code est conceptuel et ne constitue pas un composant d'IA ou un connecteur bancaire exécutable.

## 4. Séquence principale et incident
~~~mermaid
sequenceDiagram
    participant U as Analyste habilité
    participant P as AI Gateway et Policy Engine
    participant A as Composant IA
    participant R as Source ou modèle autorisé
    U->>P: demande et identité
    P->>A: contexte filtré + budget / version
    A->>R: traitement autorisé
    alt résultat valide
        R-->>A: preuves et données
        A-->>P: réponse sourcée ou proposition
        P-->>U: résultat clairement non autoritatif
    else panne, refus ou sortie incertaine
        R--xA: timeout / erreur
        A-->>P: refus, attente ou UNKNOWN
        P-->>U: abstention ou incident
    end
~~~

## 5. Sécurité, qualité et preuves de laboratoire
1. **Contrôle nominal :** mesurer la réussite d'une tâche à périmètre et modèle fixés.
2. **Attaque simulée :** Un événement frauduleux tente de déclencher un outil de mutation : le worker et l'outil refusent faute de politique et d'approbation.
3. **Panne / non-régression :** Dupliquer eventId, arrêter le modèle, saturer l'IA, expirer l'événement, invalider un schéma et vérifier indépendance du core.
4. **Reprise et confidentialité :** ne jamais interpréter une indisponibilité de l'IA comme un règlement rejeté ou réglé ; conserver la classification des données.
5. **Mesures à instrumenter :** lag du broker, coût par événement, doublons supprimés, TTL, qualité/citations, p99 IA vs latence de paiement indépendante.
6. **Responsabilité métier :** toute opération sensible conserve une politique déterministe et, le cas échéant, une approbation humaine indépendante.

## 6. ADR et choix d'alternatives
Comparer la solution à une application déterministe, à un RAG sans agent et à un modèle local lorsque cela réduit le coût, la latence ou le risque. Documenter limites de contexte, budgets, risques indirects, versions, capacités OpenShift et stratégie de retrait.

## 7. Auto-évaluation corrigée
**L'IA peut-elle émettre PaymentSettled sur la seule base de son score de confiance ?**
- **A.** Oui si sa probabilité de confiance dépasse un seuil.
- **B.** Non : seule la source financière autoritative établit le règlement. L'IA publie une analyse séparée.
- **C.** Oui si l'événement source provient d'un topic Kafka.

**Bonne réponse théorique : B.** Non : seule la source financière autoritative établit le règlement. L'IA publie une analyse séparée.

Cette clé est un corrigé de cours, pas une validation individuelle.

## 8. Référence détaillée existante dans le dépôt
[Fiche source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/15-event-driven-ai/README.md)

> **Famille :** Production / IA événementielle · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

#### 1. Définition et besoin

Déclencher une inférence ou un agent à partir d'un événement de domaine publié par un système autoritatif. L'IA reste un consommateur dérivé ; son résultat est une **analyse/proposition**, pas une preuve financière ni une commande implicite.

**Problème :** Un incident technique ou un paiement au statut incertain doit déclencher une analyse documentaire assistée sans ralentir le règlement et sans exécuter une transaction.

#### 2. Architecture logique

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

#### Déroulement

1. Publier un événement post-commit avec eventId, schemaVersion, correlationId et classification.
2. Livrer dans un broker durable et appliquer contrôle d'accès des abonnés.
3. Consommateur IA traite événements idempotemment, valide schémas, TTL et règle d'admission.
4. Assembler contexte RAG autorisé puis générer un rapport, un score ou une recommandation.
5. Enregistrer résultat dérivé, provenance, version modèle et lien vers événement source.
6. Pour agir, traverser policy engine + outil autorisé et HITL si action sensible.
7. Sur échec, retry borné, DLQ/parking et backpressure, sans bloquer le système de paiement.

#### 3. Diagramme de séquence

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

#### 4. Décisions d'architecture

- Événements d'affaires et d'exploitation différenciés, contrat schema/owner, horodatage/TTL.
- Consommateur IA isolé, quotas de ressources pour ne pas saturer le chemin critique.
- Déduplication inbox pour ne pas dupliquer coûts, notifications ni tickets.
- Guardrails sur données transportées et RAG ; aucune donnée sensible inutile dans le topic.
- Budgets de latence distincts du rail de paiement, observabilité et indicateurs de fraîcheur.

#### 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| Broker redélivre 10 fois | Inbox durable, un seul résultat logique. |
| Modèle indisponible | Queue/backpressure/parking selon TTL ; règlement indépendant. |
| Événement frauduleux ou non autorisé | Authentification broker, ACL, validation signatures/schémas. |
| Diagnostic IA pris pour fait bancaire | Étiqueter comme recommandation ; preuve financière demeure au core. |
| Retards et événements expirés | Conserver statut de traitement, écarter résultat obsolète. |

#### 6. Tests et preuves attendues

1. Duplicate eventId ne crée pas deux investigations.
2. AI worker indisponible ne ralentit pas le traitement financier.
3. Résultat est marqué « suggestion » et cite un runbook.
4. Event source non authentifiée ne déclenche pas d'outil.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

#### 7. Compromis et critères de choix

Très utile pour surveillance, support et enrichissement asynchrone. Ne pas insérer un LLM lent dans le chemin réglementaire du règlement sans nécessité démontrée.

#### 8. Question d'entretien

**Question :** L'IA peut-elle publier PaymentSettled à partir d'un score de confiance ?

**Réponse :** Non, seul le système financier autoritatif peut attester le règlement. L'IA peut publier une observation ou recommandation distincte.

#### 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Sources](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.

[Retour au programme](README.md) · [Cahier des exercices IA](exercices-et-corriges/cours-171-185.md)
