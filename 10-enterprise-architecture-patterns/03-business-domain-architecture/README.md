# 03 — Business Domains / Bounded Enterprise Domains

> **Référentiel d'architecture d'entreprise** · Exemple intégralement fictif et anonymisé · Approche inspirée des pratiques d'architecture d'entreprise, sans affiliation ni description d'un SI réel.

## 1. Problème et intention

Un portefeuille applicatif sans domaines propriétaires engendre des données dupliquées et des décisions contradictoires.

**Pattern / méthode :** Découper le métier en domaines autonomes dotés de frontières, d'acteurs et de responsabilités explicites.

## 2. Schéma conceptuel

~~~mermaid
flowchart LR
  A["Domaine clients"] --> B["Domaine contrats"] --> C["Domaine mouvements"]
~~~

### Comment le lire

1. **Domaine clients** — inventorier le contexte, sa source de preuve et son propriétaire.
2. **Domaine contrats** — définir les responsabilités et contraintes de passage entre les étapes.
3. **Domaine mouvements** — documenter le résultat, les indicateurs et ses impacts sur les domaines voisins.

## 3. Séquence de décision et gouvernance

~~~mermaid
sequenceDiagram
  actor Owner as Responsable métier
  participant Arch as Architecte d'entreprise
  participant DA as Revue d'architecture
  Owner->>Arch: Besoin métier / contrainte du SI fictif
  Arch->>Arch: Produire modèle 03 et collecter les preuves
  Arch->>DA: Options, impact, coût, NFR et arbitrage
  DA-->>Arch: Décision et conditions de validation
  Arch-->>Owner: Trajectoire et propriétaire des actions
~~~

## 4. Exemple concret sur un SI fictif

Dans un SI fictif, le domaine des clients contrôle l'identité ; le domaine des paiements référence un client, mais ne recrée pas une identité maîtresse.

**Précaution :** Ne pas prendre une équipe ou un namespace Kubernetes pour un domaine métier.

## 5. Application pratique pas à pas

1. Nommer un **sponsor métier** et distinguer faits observés des hypothèses.
2. Identifier les processus, capacités, flux et applications concernés.
3. Formaliser le modèle dans une représentation métier lisible, avec propriétaires et dépendances.
4. Comparer AS-IS, états intermédiaires et TO-BE ; évaluer options, coûts, licences, sécurité, exploitabilité et risques.
5. Enregistrer l'ADR et organiser la revue avec parties prenantes.
6. Définir indicateurs de succès, tests d'acceptation, date de révision et conditions de sortie.

## 6. Décisions, limites et anti-patterns

- **Principe de structuration :** Définir une autorité pour chaque donnée maîtresse.
- **Décision à enregistrer :** Formuler les contrats interdomaines et les dépendances acceptables.
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

- **Preuve attendue :** Chaque donnée critique dispose d'un domaine responsable et d'un contrat interdomaines.
- Les dépendances P0, la sécurité et les données sont vérifiées avec les responsables.
- Les ADR distinguent décision **approuvée**, **proposée** et **non démontrée**.
- Un état intermédiaire comporte plan de migration, rollback et stratégie de coexistence.

## 9. Question d'entretien

**Question :** comment démontrez-vous que « Business Domains / Bounded Enterprise Domains » crée de la valeur ?

**Réponse attendue :** articuler domaine clients, domaine contrats et domaine mouvements, puis apporter des preuves : chaque donnée critique dispose d'un domaine responsable et d'un contrat interdomaines.

## 10. Documents connexes

- [Index des 12 patterns d'entreprise](../README.md)
- [Étude transversale d'urbanisation d'un SI fictif](../CASE_STUDY.md)
- [Matrice de gouvernance et de décision](../DECISION_MATRIX.md)
- [15 patterns applicatifs](../../11-application-software-patterns/README.md)
