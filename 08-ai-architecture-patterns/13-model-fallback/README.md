# 13 — Model Fallback et Graceful Degradation

> **Famille :** Production / MLOps · **Exemples fictifs, anonymisés, sans attribution à un SI d'entreprise réel**.

## 1. Définition et besoin

Basculement contrôlé vers une autre version/modèle ou un mode dégradé lorsque la cible principale est indisponible, sous la contrainte que la cible secondaire respecte **les mêmes politiques d'accès et de résidence** et les exigences de qualité minimales.

**Problème :** Un modèle d'extraction saturé doit continuer à produire une réponse limitée ou indiquer son indisponibilité sans transmettre des documents confidentiels à une destination non autorisée.

## 2. Architecture logique

~~~mermaid
flowchart TB
 R["Requête + classe de données"] --> PRI["Modèle principal"]
 PRI -->|"Réussite"| OUT["Réponse vérifiée"]
 PRI -->|"Timeout / erreur"| POLICY{"Alternative autorisée et capable ?"}
 POLICY -->|Oui| SEC["Modèle secondaire validé"]
 SEC --> OUT
 POLICY -->|Non| NO["Indisponible / réponse partielle sûre"]
~~~

### Déroulement

1. Maintenir une liste de cibles approuvées avec capacités, versions, région et classification des données.
2. Détecter pannes techniques avec timeout/Circuit Breaker et distinguer erreurs métier/qualité.
3. Vérifier que le fallback satisfait politique de sécurité, capacité d'outil, contexte et seuil qualité.
4. Borner retries, temps total et coût avant de sélectionner la cible secondaire.
5. Si aucune cible compatible, passer à un mode explicitement dégradé ou à l'abstention.
6. Enregistrer modèle/version réellement utilisés, réponse, cause et effets sur SLO.

## 3. Diagramme de séquence

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

## 4. Décisions d'architecture

- Liste ordonnée d'alternatives avec preuves qualité et politique d'accès.
- Chiffrement/transport et non-propagation de données à l'extérieur du périmètre.
- Distinguer fallback technique, dégradation de qualité et abstention.
- Préserver compatibilité de schéma API et tests interversions.
- Traçabilité effective model id, p95, coûts, taux de fallback et erreurs introduites.

## 5. Pannes et protections

| Échec | Décision sûre |
|---|---|
| Second modèle interdit pour données classifiées | Refus et indisponibilité explicite. |
| Second modèle change le format JSON | Validation de contrat et adaptation sûre. |
| Retries multiplient coût et latence | Budget commun, backoff, Circuit Breaker. |
| Appel initial peut encore traiter malgré timeout | Outils de mutation à idempotence forte ; pas de double action. |

## 6. Tests et preuves attendues

1. Fallback reste dans allowlist classifiée.
2. Modèle secondaire incompatible provoque abstention.
3. Coupure du primaire ne viole pas les budgets.
4. La version et la cause de fallback sont observables.

**Mesures :** qualité sur jeu de référence, autorisations effectives, latence p95/p99, coût/tokens, reprise et traçabilité du modèle/version.

## 7. Compromis et critères de choix

Augmente disponibilité si modèles compatibles ; peut diminuer qualité et doubler coûts, donc exige des tests spécifiques.

## 8. Question d'entretien

**Question :** Peut-on basculer automatiquement un modèle confidentiel vers n'importe quelle API disponible ?

**Réponse :** Non. Confidentialité, région, permissions et capacité exigée priment sur la continuité de service.

## 9. Application Cloud Native

- Déployer les services d'IA par contrat explicite sur Kubernetes/OpenShift : CPU/GPU si disponible, IAM, séparation des namespaces, réseau, secrets, quota et observabilité.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice](../PATTERNS_DECISION_MATRIX.md) · [Sources](../REFERENCES.md).
- La sortie d'un LLM reste une **hypothèse à contrôler** lorsqu'elle détermine des décisions importantes.
