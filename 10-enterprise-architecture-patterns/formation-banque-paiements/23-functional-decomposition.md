# Cours 23 — Décomposition fonctionnelle

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Comment découper un besoin sans créer des microservices par réflexe ?

## 1. Besoin métier
Le besoin « réaliser un virement SEPA de 500 EUR » doit être traduit en fonctions indépendamment des applications existantes.

## 2. Définition
La décomposition fonctionnelle part d'une capacité métier et identifie des fonctions cohésives puis des sous-fonctions. Une fonction porte un résultat observable, pas un choix de technologie.

## 3. Étude de cas détaillée
Niveau 1 : Gérer les virements. Niveau 2 : Recevoir un ordre; vérifier identité et droits; contrôler plafond; contrôler conformité; piloter traitement; suivre statut; rapprocher résultat; expliquer le rejet. Niveau 3 : ContrôlerPlafond lit le plafond autoritatif, calcule le cumul autorisé et retourne décision + justification.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Les fonctions ont des périmètres non ambigus; chaque règle possède un propriétaire; les dépendances sont explicites; l'acceptation de l'ordre n'est pas le règlement.

**Anti-pattern :** Découper les fonctions selon les classes Java ou doubler le contrôle de plafond sans cohérence.

## 5. Plan de validation
Tester que chaque besoin de l'acteur a une fonction correspondante; détecter les doublons, les trous de couverture et les cas de reprise.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Quel critère guidera le découpage ?**

- **A.** Le nombre de frameworks.
- **B.** Les responsabilités fonctionnelles et leurs résultats observables.
- **C.** Une fonction par méthode Java.

**Correction : B.** La décomposition fonctionnelle part d'une capacité métier et identifie des fonctions cohésives puis des sous-fonctions. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
