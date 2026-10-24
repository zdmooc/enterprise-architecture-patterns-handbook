# Cours 31 — Analyse d'impact fonctionnelle

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Quelles conséquences lorsque le métier change une règle ?

## 1. Besoin métier
La banque fictive passe le plafond journalier de certains clients de 1 000 à 2 000 EUR.

## 2. Définition
L'analyse d'impact remonte des règles aux fonctions, contrats, flux, vues client, données, tests, organisations et dates d'application concernés.

## 3. Étude de cas détaillée
Étudier ContrôlerPlafond, ConsulterPlafond, SuivreRefus, AuditerDécisions, supports client et référentiel de plafonds. Vérifier les populations éligibles, le calcul du cumul, la temporalité et la gestion des décisions prises avant changement.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Aucun client hors périmètre ne change de plafond; les refus utilisent le motif exact; la nouvelle règle est versionnée et vérifiable.

**Anti-pattern :** Modifier un chiffre dans un seul service et supposer tous les consommateurs cohérents.

## 5. Plan de validation
Tests 1 500 EUR accepté sous nouveau plafond à cumul zéro; 2 500 EUR refusé; ancien client limité à 1 000 EUR; cumul déjà engagé; décisions antérieures explicables.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Quelle démarche faut-il adopter ?**

- **A.** Changer uniquement un paramètre sans analyse.
- **B.** Identifier toutes les fonctions impactées et préparer règles, contrats et tests.
- **C.** Reconstruire tout le SI.

**Correction : B.** L'analyse d'impact remonte des règles aux fonctions, contrats, flux, vues client, données, tests, organisations et dates d'application concernés. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
