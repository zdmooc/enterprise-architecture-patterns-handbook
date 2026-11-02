# Cours 183 — Model Fallback — Repli sous politique · Architecture IA et agentique

> Banque fictive · ordre SEPA de 500 EUR. **Support pédagogique publié avec corrigé théorique ; aucun exercice individuel ni test sur cluster n'est déclaré validé.**

## 1. Besoin métier et problème
Le modèle local utilisé pour rechercher des procédures est saturé. Il existe un modèle alternatif, mais sa localisation ou sa politique de confidentialité peut différer.

## 2. HLD : responsabilités des composants
~~~mermaid
flowchart LR
    A["Requête classifiée"] --> B["Policy-safe fallback selector"]
    B --> C["Modèle autorisé ou dégradation"]
    B -. "Risque / absence de preuve" .-> STOP["Refus, attente ou abstention"]
~~~

**Décision d'architecture :** Construire un ensemble de modèles alternatifs approuvés par classification, tenant, budget, région et compatibilité ; en cas de panne, choisir un repli autorisé ou fournir une abstention/degradation. Revalider qualité et sortie.

**Invariant à défendre :** La panne d'un modèle local n'autorise pas la fuite d'un document bancaire vers un modèle public non approuvé.

## 3. Contrat de contrôle
~~~text
fallback = allowedModels.filter(dataClass, tenant, region, budget).firstHealthyOrNone()
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
2. **Attaque simulée :** Couper l'inférence locale pour provoquer un fallback externe ; la Gateway refuse tout endpoint hors région et politique.
3. **Panne / non-régression :** Panne, quota, timeouts, divergence de format, modèle plus faible, cache périmé et perte de qualité en fallback.
4. **Reprise et confidentialité :** ne jamais interpréter une indisponibilité de l'IA comme un règlement rejeté ou réglé ; conserver la classification des données.
5. **Mesures à instrumenter :** fallback success sans violation, déclenchements, écarts de qualité, p99, coût, perte de contexte et refus appropriés.
6. **Responsabilité métier :** toute opération sensible conserve une politique déterministe et, le cas échéant, une approbation humaine indépendante.

## 6. ADR et choix d'alternatives
Comparer la solution à une application déterministe, à un RAG sans agent et à un modèle local lorsque cela réduit le coût, la latence ou le risque. Documenter limites de contexte, budgets, risques indirects, versions, capacités OpenShift et stratégie de retrait.

## 7. Auto-évaluation corrigée
**Que faire si aucun modèle de repli n'est autorisé pour des données classifiées ?**
- **A.** Appeler le modèle public le moins cher pour maintenir le service.
- **B.** Supprimer les passages sensibles du log tout en les envoyant au modèle.
- **C.** Refuser ou différer explicitement ; ne jamais contourner les politiques de classification.

**Bonne réponse théorique : C.** Refuser ou différer explicitement ; ne jamais contourner les politiques de classification.

Cette clé est un corrigé de cours, pas une validation individuelle.

## 8. Référence détaillée existante dans le dépôt
[Fiche source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/13-model-fallback/README.md)

> **Famille :** Production / MLOps · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

#### 1. Définition et besoin

Basculement contrôlé vers une autre version/modèle ou un mode dégradé lorsque la cible principale est indisponible, sous la contrainte que la cible secondaire respecte **les mêmes politiques d'accès et de résidence** et les exigences de qualité minimales.

**Problème :** Un modèle d'extraction saturé doit continuer à produire une réponse limitée ou indiquer son indisponibilité sans transmettre des documents confidentiels à une destination non autorisée.

#### 2. Architecture logique

~~~mermaid
flowchart TB
 R["Requête + classe de données"] --> PRI["Modèle principal"]
 PRI -->|"Réussite"| OUT["Réponse vérifiée"]
 PRI -->|"Timeout / erreur"| POLICY{"Alternative autorisée et capable ?"}
 POLICY -->|Oui| SEC["Modèle secondaire validé"]
 SEC --> OUT
 POLICY -->|Non| NO["Indisponible / réponse partielle sûre"]
~~~

#### Déroulement

1. Maintenir une liste de cibles approuvées avec capacités, versions, région et classification des données.
2. Détecter pannes techniques avec timeout/Circuit Breaker et distinguer erreurs métier/qualité.
3. Vérifier que le fallback satisfait politique de sécurité, capacité d'outil, contexte et seuil qualité.
4. Borner retries, temps total et coût avant de sélectionner la cible secondaire.
5. Si aucune cible compatible, passer à un mode explicitement dégradé ou à l'abstention.
6. Enregistrer modèle/version réellement utilisés, réponse, cause et effets sur SLO.

#### 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
 participant A as Application
 participant R as Routeur
 participant M1 as Modèle A local
 participant M2 as Modèle B local approuvé
 A->>R: Demande classifiée interne
 R->>M1: Inférence
 M1--xR: 503 / surcharge
 R->>R: Budget restant et politique locale
 R->>M2: Inférence même données, dans zone autorisée
 M2-->>R: Réponse version B
 R-->>A: Réponse validée + version réellement utilisée
~~~

**Exemple pratique :** Le modèle local d'extraction est arrêté pour maintenance. Un second modèle local autorisé prend le relais avec le même contrat JSON. S'il ne sait pas extraire un champ obligatoire, l'application retourne une erreur explicite au lieu d'inventer une valeur.

#### 4. Décisions d'architecture

- Liste ordonnée d'alternatives avec preuves qualité et politique d'accès.
- Chiffrement/transport et non-propagation de données à l'extérieur du périmètre.
- Distinguer fallback technique, dégradation de qualité et abstention.
- Préserver compatibilité de schéma API et tests interversions.
- Traçabilité effective model id, p95, coûts, taux de fallback et erreurs introduites.

#### 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| Second modèle interdit pour données classifiées | Refus et indisponibilité explicite. |
| Second modèle change le format JSON | Validation de contrat et adaptation sûre. |
| Retries multiplient coût et latence | Budget commun, backoff, Circuit Breaker. |
| Appel initial peut encore traiter malgré timeout | Outils de mutation à idempotence forte ; pas de double action. |

#### 6. Tests et preuves attendues

1. Fallback reste dans allowlist classifiée.
2. Modèle secondaire incompatible provoque abstention.
3. Coupure du primaire ne viole pas les budgets.
4. La version et la cause de fallback sont observables.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

#### 7. Compromis et critères de choix

Augmente disponibilité si modèles compatibles ; peut diminuer qualité et doubler coûts, donc exige des tests spécifiques.

#### 8. Question d'entretien

**Question :** Peut-on basculer automatiquement un modèle confidentiel vers n'importe quelle API disponible ?

**Réponse :** Non. Confidentialité, région, permissions et capacité exigée priment sur la continuité de service.

#### 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Sources](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.

[Retour au programme](README.md) · [Cahier des exercices IA](exercices-et-corriges/cours-171-185.md)
