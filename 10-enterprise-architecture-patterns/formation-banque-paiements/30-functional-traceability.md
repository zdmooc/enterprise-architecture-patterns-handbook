# Cours 30 — Traçabilité fonctionnelle

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Comment prouver qu'aucun besoin métier n'a été oublié ?

## 1. Besoin métier
Le métier exige l'acceptation contrôlée, le motif de refus, le suivi des virements et la gestion des confirmations incertaines.

## 2. Définition
La traçabilité relie besoin → règle → fonction → contrat/flux → scénario → critère d'acceptation et preuve. Les liens sont bidirectionnels pour analyser les écarts.

## 3. Étude de cas détaillée
Construire une matrice : B-001 « plafond respecté » → F-ContrôlerPlafond → BR-001 → CT-PLAFOND → test limite; B-002 « expliquer refus » → F-Suivi → motif métier → test de restitution. Isoler les exigences non couvertes.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Chaque besoin prioritaire a une fonction et un test; toute fonction significative justifie sa nécessité; les décisions d'arbitrage sont conservées.

**Anti-pattern :** Confondre liste de fonctionnalités livrées et couverture des besoins; omettre les exceptions.

## 5. Plan de validation
Audit de matrice : détecter un besoin sans test, une fonction sans propriétaire, un statut sans preuve.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Que doit faire l'architecte si un besoin n'a aucune fonction associée ?**

- **A.** Déclarer le projet terminé.
- **B.** Retirer le besoin sans accord.
- **C.** Signaler le trou de couverture et définir fonction et validation adaptées.

**Correction : C.** La traçabilité relie besoin → règle → fonction → contrat/flux → scénario → critère d'acceptation et preuve. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
