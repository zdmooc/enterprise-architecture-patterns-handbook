# Cours 26 — Gestion fonctionnelle des exceptions

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Comment expliquer une exception métier et éviter les états ambigus ?

## 1. Besoin métier
Un virement SEPA de 500 EUR peut être refusé pour plafond dépassé, informations insuffisantes ou problème de traitement externe.

## 2. Définition
Une exception fonctionnelle décrit un écart au scénario nominal avec cause, décision, responsable, effet sur l'état, communication et éventuelle réparation.

## 3. Étude de cas détaillée
Distinguer RefusMétier (décision finale documentée), IndisponibilitéTechnique (décision suspendue), ConfirmationInconnue (investigation et réconciliation nécessaires). Définir les statuts, motifs visibles et options de reprise pour chaque cas.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Aucune indisponibilité ne devient automatiquement un rejet métier; une demande non confirmée n'est pas rejouée aveuglément; chaque exception est traçable.

**Anti-pattern :** Afficher « paiement refusé » lorsque le système n'a simplement pas reçu la réponse; déclencher un deuxième débit.

## 5. Plan de validation
Vérifier plafond dépassé, panne réseau après émission, notification perdue et doublon d'événement.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Que faire quand la réponse externe est perdue ?**

- **A.** Afficher « réglé » sans preuve.
- **B.** Conserver un état indéterminé et rechercher le résultat avant toute reprise.
- **C.** Émettre sans contrôle un deuxième ordre.

**Correction : B.** Une exception fonctionnelle décrit un écart au scénario nominal avec cause, décision, responsable, effet sur l'état, communication et éventuelle réparation. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
