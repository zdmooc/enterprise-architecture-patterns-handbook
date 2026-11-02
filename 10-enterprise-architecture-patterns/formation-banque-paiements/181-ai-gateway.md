# Cours 181 — AI Gateway — IAM, quotas, coûts et politique · Architecture IA et agentique

> Banque fictive · ordre SEPA de 500 EUR. **Support pédagogique publié avec corrigé théorique ; aucun exercice individuel ni test sur cluster n'est déclaré validé.**

## 1. Besoin métier et problème
Plusieurs applications internes appellent des modèles IA dont certains sont externes. La plateforme doit vérifier qui peut utiliser quel modèle et quelles données peuvent sortir.

## 2. HLD : responsabilités des composants
~~~mermaid
flowchart LR
    A["Application + identité OIDC/workload"] --> B["AI Gateway et politique"]
    B --> C["Modèle permis / audit"]
    B -. "Risque / absence de preuve" .-> STOP["Refus, attente ou abstention"]
~~~

**Décision d'architecture :** Centraliser authentification, autorisation, inventaire modèle, classification des données, contrôle de résidence, quotas, budgets, protection des prompts/outputs et observabilité. Les API métiers contrôlent aussi les droits objet.

**Invariant à défendre :** Une équipe non autorisée ne peut ni utiliser un modèle interdit ni transmettre une donnée confidentielle à un endpoint public.

## 3. Contrat de contrôle
~~~text
permit = tokenValid && modelAllowlist(tenant) && dataPolicy(payload) && quotaAvailable && regionAllowed
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
2. **Attaque simulée :** Présenter un token valable pour une autre audience et demander un modèle non homologué : rejet.
3. **Panne / non-régression :** Essayer dépassement quota, dépassement budget, mauvaise audience, modèle indisponible, données sensibles et réponse en streaming.
4. **Reprise et confidentialité :** ne jamais interpréter une indisponibilité de l'IA comme un règlement rejeté ou réglé ; conserver la classification des données.
5. **Mesures à instrumenter :** coût par tenant, taux de 403/429, latence, disponibilité par modèle, volume de PII interceptées.
6. **Responsabilité métier :** toute opération sensible conserve une politique déterministe et, le cas échéant, une approbation humaine indépendante.

## 6. ADR et choix d'alternatives
Comparer la solution à une application déterministe, à un RAG sans agent et à un modèle local lorsque cela réduit le coût, la latence ou le risque. Documenter limites de contexte, budgets, risques indirects, versions, capacités OpenShift et stratégie de retrait.

## 7. Auto-évaluation corrigée
**La Gateway peut-elle remplacer l'autorisation objet de la Payment API ?**
- **A.** Non, l'API bancaire protège chaque ressource et la Gateway impose en plus les politiques d'accès aux modèles.
- **B.** Oui, l'authentification au périmètre IA suffit.
- **C.** Oui si le modèle n'a pas d'outil d'écriture.

**Bonne réponse théorique : A.** Non, l'API bancaire protège chaque ressource et la Gateway impose en plus les politiques d'accès aux modèles.

Cette clé est un corrigé de cours, pas une validation individuelle.

## 8. Référence détaillée existante dans le dépôt
[Fiche source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/11-ai-gateway/README.md)

> **Famille :** Sécurité / gouvernance · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

#### 1. Définition et besoin

Une AI Gateway applique des politiques transversales aux requêtes et réponses de modèles : identité, routage, quotas, budgets, observation et gouvernance. Elle ne remplace ni l'API Gateway métier ni les autorisations applicatives.

**Problème :** Des applications internes appellent plusieurs serveurs d'inférence ; sans point de contrôle, la mesure du coût, la classification des données et les quotas divergent entre clients.

#### 2. Architecture logique

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

#### Déroulement

1. Authentifier appelant service et utilisateur final lorsque nécessaire.
2. Appliquer autorisations et règles de données : modèles/régions autorisées.
3. Valider tailles, limites de tokens, rate limits, budget financier et contrôle anti-abus.
4. Sélectionner une cible autorisée via Model Router puis transmettre avec TLS.
5. Collecter métriques d'inférence et traces expurgées : latence, utilisation, erreurs, coût estimé.
6. Valider sortie/streaming et erreurs ; renvoyer des statuts contractuels sans fuite.

#### 3. Diagramme de séquence

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

#### 4. Décisions d'architecture

- Distinguer AI Gateway (trafic modèle) et API Gateway (contrats métier) ; elles peuvent être deux fonctions du même produit.
- Exposer authentification service-à-service, identité de l'utilisateur, contexte d'autorisation, tenancy.
- Quota tokens, requêtes simultanées, coût par équipe et prévention d'épuisement de capacité.
- Support streaming, cancel, timeouts, modèles versionnés et interprétation des erreurs.
- Politique de données et résidence inférée **avant** toute sortie du périmètre.

#### 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| Requête non autorisée vers autre modèle | Routeur strict à allowlist et politique de confidentialité. |
| Usage tokens incontrôlé | Cap tokens, coûts, rate limit, admission. |
| Traçage stocke PII | Désactiver corps, hachage/minimisation des traces. |
| Gateway indisponible | Réplicas, quotas durables, dégradation contrôlée. |
| Injection de prompt | Guardrails et API métiers restent indispensables. |

#### 6. Tests et preuves attendues

1. Tenant A n'appelle pas les modèles réservés à B.
2. Budget 4 000 tokens impossible à dépasser.
3. Données internes restent dans périmètre local même pendant panne.
4. Une annulation client stoppe la consommation si supportée.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

#### 7. Compromis et critères de choix

Utile avec de multiples modèles ou applications ; coût/latence d'un saut supplémentaire. Ne pas multiplier les gateways sans responsabilité distincte.

#### 8. Question d'entretien

**Question :** AI Gateway suffit-elle à protéger une action agentique ?

**Réponse :** Non, l'autorisation d'outils et l'approbation métier doivent aussi être imposées dans les services destinataires.

#### 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Sources](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.

[Retour au programme](README.md) · [Cahier des exercices IA](exercices-et-corriges/cours-171-185.md)
