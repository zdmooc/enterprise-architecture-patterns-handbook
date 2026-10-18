# 08 — Reflection / Evaluator / Critic

> **Famille :** IA agentique · **Référentiel pédagogique anonymisé**. Aucun client ni fournisseur réel n'est identifié.

## 1. Définition et problème métier

Un second passage (ou composant distinct) examine une réponse ou un plan à partir de critères explicites, signale les erreurs puis autorise au plus un nombre limité de révisions. L'auto-évaluation par LLM seule ne prouve pas la vérité.

**Pourquoi :** Une synthèse générée des règles de reprise bancaire peut confondre « ordre soumis » et « paiement réglé » ; elle doit être contrôlée avant affichage.

## 2. Architecture logique

~~~mermaid
flowchart TB
 Q["Question + corpus"] --> GEN["Générateur"]
 GEN --> DRAFT["Brouillon sourcé"]
 DRAFT --> VALID["Contrôles déterministes"]
 VALID --> EVAL["Évaluateur : grille de preuve"]
 EVAL -->|"Révision bornée"| GEN
 EVAL -->|"Accepté"| OUT["Réponse"]
 EVAL -->|"Échec persistant"| NO["Abstention / revue humaine"]
~~~

### Déroulement

1. Produire un brouillon traçable avec sources.
2. Évaluer avec règles déterministes en premier : schéma de sortie, références, absence de secrets, politique.
3. Faire critiquer par un évaluateur indépendant sur grille : exactitude, sources, complétude, contradictions.
4. Renvoyer uniquement les critiques structurées au générateur pour correction éventuelle.
5. Limiter le nombre de boucles ; en échec persistant, abstention ou escalade.
6. Conserver verdict, version du modèle, tests et logs de décision expurgés.

## 3. Séquence métier illustrative

~~~mermaid
sequenceDiagram
 participant G as Générateur
 participant V as Validateur
 participant E as Évaluateur
 G->>V: « timeout = paiement rejeté »
 V->>E: Brouillon et sources
 E-->>G: Critique : aucun élément ne prouve le rejet
 G->>V: « statut non confirmé : réconciliation »
 V-->>G: Schéma/provenance conformes
 G-->>E: Réponse révisée
~~~

**Exemple :** La première réponse fictive dit « le virement a échoué après 10 s ». L'évaluateur vérifie les sources et fait corriger en « la confirmation n'est pas reçue ; appliquer les obligations du schéma et rapprocher les preuves ». Il ne fabrique aucune preuve de règlement.

## 4. Arbitrages d'architecture

- Définir rubrics sur jeux de données étiquetés par experts.
- Évaluer indépendamment fidélité aux sources et exactitude métier.
- Ne pas accorder d'accès supplémentaires à l'évaluateur.
- Limiter retries et éviter deux modèles commettant la même erreur.
- Mesurer faux positifs/faux négatifs du validateur et taux d'abstention.

## 5. Scénarios de panne et attaques

| Incident | Parade |
|---|---|
| Critique inventée | Demander passage cité / justification ; contrôle humain sur échantillon. |
| Boucle sans fin | 2 ou 3 révisions maximum puis escalade. |
| Fausse confiance d'un score interne | Mesurer sur données de référence humaines indépendantes. |
| Évaluation reçoit une donnée interdite | Même politique d'accès que le générateur. |

## 6. Tests de qualification

1. Phrase sans source rejetée.
2. Confusion ACCEPTED/SETTLED détectée.
3. Réponse correcte préservée, sans dégradation systématique.
4. Après budget maximal, abstention plutôt que nouvelle boucle.

**Critère transversal :** aucun accès à un compte ni changement financier sans la politique du système exécutant et son autorisation explicite.

## 7. Quand choisir, quand éviter

Pertinent sur dossiers structurés et qualité, mais double les ressources et peut introduire sa propre erreur.

Mesurer sur un jeu d'essais : qualité, fidélité aux preuves, coût, latence p95/p99, permissions effectivement imposées et sécurité face aux contenus non fiables.

## 8. Question d'entretien

**Question :** Une seconde IA garantit-elle l'exactitude de la première ?

**Réponse :** Non ; la vérification nécessite des critères indépendants, idéalement des preuves et tests déterministes.

## 9. Mise en œuvre / prolongements

- Services Java ou Python sur Kubernetes/OpenShift, policy engine et métriques, sans dépendance obligatoire à un éditeur particulier.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice des patterns](../PATTERNS_DECISION_MATRIX.md) · [Références](../REFERENCES.md).
- Ne jamais confondre **proposition générée**, **approbation** et **exécution réellement confirmée**.
