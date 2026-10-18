# 11 — AI Gateway : point de contrôle des requêtes de modèles

> **Famille :** Sécurité / gouvernance · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

## 1. Définition et besoin

Une AI Gateway applique des politiques transversales aux requêtes et réponses de modèles : identité, routage, quotas, budgets, observation et gouvernance. Elle ne remplace ni l'API Gateway métier ni les autorisations applicatives.

**Problème :** Des applications internes appellent plusieurs serveurs d'inférence ; sans point de contrôle, la mesure du coût, la classification des données et les quotas divergent entre clients.

## 2. Architecture logique

~~~mermaid
flowchart TB
 A["Appli documentaire"] --> G["AI Gateway"]
 B["Agent spécialisé"] --> G
 G --> SEC["IAM, classification, quotas, coûts"]
 SEC --> ROUTE["Model Router"]
 ROUTE --> LOCAL["Serveur LLM local"]
 ROUTE --> SECOND["Serveur LLM secondaire approuvé"]
 G --> OBS["Métriques, traces expurgées"]
 LOCAL --> OUT["Contrôle et retour"]
 SECOND --> OUT
~~~

### Déroulement

1. Authentifier appelant service et utilisateur final lorsque nécessaire.
2. Appliquer autorisations et règles de données : modèles/régions autorisées.
3. Valider tailles, limites de tokens, rate limits, budget financier et contrôle anti-abus.
4. Sélectionner une cible autorisée via Model Router puis transmettre avec TLS.
5. Collecter métriques d'inférence et traces expurgées : latence, utilisation, erreurs, coût estimé.
6. Valider sortie/streaming et erreurs ; renvoyer des statuts contractuels sans fuite.

## 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
 participant A as Appli
 participant G as AI Gateway
 participant P as Moteur de politiques
 participant M as Service LLM
 A->>G: Chat completions, contexte classifié
 G->>P: Token, tenant, modèle, budget
 P-->>G: Local seulement, max 4000 tokens
 G->>M: Inférence version v3
 M-->>G: Réponse + token usage
 G-->>A: Réponse et identifiant de trace
~~~

**Exemple pratique :** Un assistant documentaire interne sollicite un modèle local autorisé. Un client de reporting public peut utiliser une seconde cible approuvée. Les quotas et décisions sont enregistrés sans exposer les documents dans les métriques.

## 4. Décisions d'architecture

- Distinguer AI Gateway (trafic modèle) et API Gateway (contrats métier) ; elles peuvent être deux fonctions du même produit.
- Exposer authentification service-à-service, identité de l'utilisateur, contexte d'autorisation, tenancy.
- Quota tokens, requêtes simultanées, coût par équipe et prévention d'épuisement de capacité.
- Support streaming, cancel, timeouts, modèles versionnés et interprétation des erreurs.
- Politique de données et résidence inférée **avant** toute sortie du périmètre.

## 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| Requête non autorisée vers autre modèle | Routeur strict à allowlist et politique de confidentialité. |
| Usage tokens incontrôlé | Cap tokens, coûts, rate limit, admission. |
| Traçage stocke PII | Désactiver corps, hachage/minimisation des traces. |
| Gateway indisponible | Réplicas, quotas durables, dégradation contrôlée. |
| Injection de prompt | Guardrails et API métiers restent indispensables. |

## 6. Tests et preuves attendues

1. Tenant A n'appelle pas les modèles réservés à B.
2. Budget 4 000 tokens impossible à dépasser.
3. Données internes restent dans périmètre local même pendant panne.
4. Une annulation client stoppe la consommation si supportée.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

## 7. Compromis et critères de choix

Utile avec de multiples modèles ou applications ; coût/latence d'un saut supplémentaire. Ne pas multiplier les gateways sans responsabilité distincte.

## 8. Question d'entretien

**Question :** AI Gateway suffit-elle à protéger une action agentique ?

**Réponse :** Non, l'autorisation d'outils et l'approbation métier doivent aussi être imposées dans les services destinataires.

## 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice](../PATTERNS_DECISION_MATRIX.md) · [Sources](../REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.
