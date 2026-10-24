# Cours 27 — Orchestration fonctionnelle

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Qui pilote un processus qui traverse plusieurs fonctions ?

## 1. Besoin métier
Le parcours du virement de 500 EUR dépend de contrôles successifs et peut attendre une confirmation externe.

## 2. Définition
L'orchestration confie la coordination à une fonction pilote qui applique un enchaînement, des décisions, des délais et des reprises explicites; elle ne signifie pas forcément un moteur BPM.

## 3. Étude de cas détaillée
Un orchestrateur reçoit la demande, sollicite l'éligibilité et le plafond, déclenche la transmission après décision autorisée, puis attend ou recherche un résultat. Il conserve l'état et les jalons nécessaires à l'explication d'un incident.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Une étape déjà exécutée n'est pas relancée à l'aveugle; l'orchestrateur ne s'arroge pas les règles propres aux autres domaines; un timeout n'est pas un règlement négatif.

**Anti-pattern :** Centraliser toutes les règles bancaires dans l'orchestrateur, devenu monolithe de décisions.

## 5. Plan de validation
Tester étape 2 refusée, timeout après émission, reprise sur référence stable et double demande.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Quel est le rôle de l'orchestrateur ?**

- **A.** Modifier les comptes sans journaliser.
- **B.** Remplacer toutes les fonctions métier.
- **C.** Coordonner les étapes, leurs états et leurs exceptions.

**Correction : C.** L'orchestration confie la coordination à une fonction pilote qui applique un enchaînement, des décisions, des délais et des reprises explicites; elle ne signifie pas forcément un moteur BPM. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
