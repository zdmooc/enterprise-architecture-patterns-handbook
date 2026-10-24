# Cours 32 — Tests de non-régression fonctionnelle

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Comment démontrer qu'un changement ne casse pas l'existant ?

## 1. Besoin métier
Une catégorie de clients bénéficie désormais d'un plafond journalier fictif de 2 000 EUR; les autres conservent leur plafond.

## 2. Définition
La non-régression garantit le comportement attendu des fonctions non censées changer, en complément de la validation des nouvelles règles.

## 3. Étude de cas détaillée
Constituer une suite stable de scénarios : client éligible 1 500 EUR autorisé à cumul zéro; client non éligible toujours soumis au plafond précédent; dépassement et cumul correctement rejetés; historique et information client inchangés hors nouveaux cas.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Comparer avant/après sur un jeu de référence; diagnostiquer les écarts voulus et non voulus; aucun résultat incertain ne devient accepté à tort.

**Anti-pattern :** Valider uniquement un heureux chemin du nouveau plafond.

## 5. Plan de validation
Exécuter tests de limite, cumul, refus, client non ciblé, disponibilité de la source et reprise après échec.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Que doit-on vérifier après la modification ?**

- **A.** Uniquement le nouvel écran.
- **B.** Rien dès que l'équipe a déployé.
- **C.** Les nouvelles règles et les comportements existants potentiellement impactés.

**Correction : C.** La non-régression garantit le comportement attendu des fonctions non censées changer, en complément de la validation des nouvelles règles. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
