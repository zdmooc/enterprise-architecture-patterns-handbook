# 08 — Transition Architecture / Architecture intermédiaire

> **Référentiel d'architecture d'entreprise** · Exemple intégralement fictif et anonymisé · Approche inspirée des pratiques d'architecture d'entreprise, sans affiliation ni description d'un SI réel.

## 1. Problème et intention

Passer de l'existant à la cible d'un seul coup crée une dépendance au big bang et des risques financiers.

**Pattern / méthode :** Définir un ou plusieurs états intermédiaires viables, avec interfaces temporaires, coûts et contrôles de coexistence.

## 2. Schéma conceptuel

~~~mermaid
flowchart LR
  A["AS-IS"] --> B["Coexistence contrôlée"] --> C["TO-BE"]
~~~

### Comment le lire

1. **AS-IS** — inventorier le contexte, sa source de preuve et son propriétaire.
2. **Coexistence contrôlée** — définir les responsabilités et contraintes de passage entre les étapes.
3. **TO-BE** — documenter le résultat, les indicateurs et ses impacts sur les domaines voisins.

## 3. Séquence de décision et gouvernance

~~~mermaid
sequenceDiagram
  actor Owner as Responsable métier
  participant Arch as Architecte d'entreprise
  participant DA as Revue d'architecture
  Owner->>Arch: Besoin métier / contrainte du SI fictif
  Arch->>Arch: Produire modèle 08 et collecter les preuves
  Arch->>DA: Options, impact, coût, NFR et arbitrage
  DA-->>Arch: Décision et conditions de validation
  Arch-->>Owner: Trajectoire et propriétaire des actions
~~~

## 4. Exemple concret sur un SI fictif

Une façade provisoire route la consultation vers un nouveau service, mais l'écriture reste exclusivement sur le système initial.

**Précaution :** Une architecture intermédiaire peut durer des années si la dette temporaire n'est pas budgétée.

## 5. Application pratique pas à pas

1. Nommer un **sponsor métier** et distinguer faits observés des hypothèses.
2. Identifier les processus, capacités, flux et applications concernés.
3. Formaliser le modèle dans une représentation métier lisible, avec propriétaires et dépendances.
4. Comparer AS-IS, états intermédiaires et TO-BE ; évaluer options, coûts, licences, sécurité, exploitabilité et risques.
5. Enregistrer l'ADR et organiser la revue avec parties prenantes.
6. Définir indicateurs de succès, tests d'acceptation, date de révision et conditions de sortie.

## 6. Décisions, limites et anti-patterns

- **Principe de structuration :** Rendre explicite le propriétaire des écritures à chaque étape.
- **Décision à enregistrer :** Prévoir arrêt, retour arrière et retrait des interfaces temporaires.
- **Anti-pattern :** produire une carte statique sans propriétaire, preuve de flux ni processus de mise à jour.
- **À éviter :** inventer des chiffres d'organisation, de patrimoine ou de niveau de service ; les valeurs d'exemple sont des hypothèses.
- **Revue de risques :** rechercher dépendances cachées, propriétaires multiples, changements de données et retour arrière.

## 7. Pannes organisationnelles ou techniques à tester

| Incident fictif | Contrôle ou remédiation |
|---|---|
| Application supprimée alors qu'un flux caché existe | Inventaire des flux et test de non-régression avant retrait |
| Donnée maîtresse modifiée par deux domaines | Identifier autorité unique, contrat et procédure de réconciliation |
| Coût ou licence sous-estimé | Actualiser la matrice TCO et faire approuver une enveloppe |
| Architecture cible incompatible avec une obligation réglementaire | Revue conformité, contrôle compensatoire et décision bloquante |

## 8. Critères de qualification

- **Preuve attendue :** Chaque état intermédiaire peut fonctionner, être exploité et réconcilié sans double traitement.
- Les dépendances P0, la sécurité et les données sont vérifiées avec les responsables.
- Les ADR distinguent décision **approuvée**, **proposée** et **non démontrée**.
- Un état intermédiaire comporte plan de migration, rollback et stratégie de coexistence.

## 9. Question d'entretien

**Question :** comment démontrez-vous que « Transition Architecture / Architecture intermédiaire » crée de la valeur ?

**Réponse attendue :** articuler as-is, coexistence contrôlée et to-be, puis apporter des preuves : chaque état intermédiaire peut fonctionner, être exploité et réconcilié sans double traitement.

## 10. Documents connexes

- [Index des 12 patterns d'entreprise](../README.md)
- [Étude transversale d'urbanisation d'un SI fictif](../CASE_STUDY.md)
- [Matrice de gouvernance et de décision](../DECISION_MATRIX.md)
- [15 patterns applicatifs](../../11-application-software-patterns/README.md)
