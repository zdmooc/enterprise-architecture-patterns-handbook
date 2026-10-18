# Étude de référence — Architecture de données, gouvernance et analytique

**Cas fictif / non contractuel / aucun SI d'entreprise réel.**

## 1. Contexte métier et AS-IS

Des domaines fictifs Clients, Contrats et Dossiers publient données structurées et événements. Les rapports prennent des jours à produire, des définitions diffèrent et les copies n'ont ni owner ni lineage.

**Objectif de transformation :** Consolider un reporting de dossiers à partir de flux changeants tout en conservant les sources autoritatives.

## 2. Hypothèse TO-BE (logique)

~~~mermaid
flowchart LR
  A["Sources maîtresses par domaine"] --> B["CDC / Data Products / qualité"] --> C["Lakehouse & BI sans autorité financière"]
  B --> D["Observabilité + preuve de décision"]
~~~

Les flèches représentent des **responsabilités et contrats**, non l'assurance qu'un message réseau vaut opération métier finalisée. Toute donnée financière conserve sa source autoritative.

## 3. Chemin de décision — séquence d'architecture

~~~mermaid
sequenceDiagram
  actor Owner as Responsable métier
  participant EA as Architecture
  participant DA as Revue d'architecture
  participant Run as Exploitation / sécurité
  Owner->>EA: Exigences, criticité et état existant
  EA->>EA: Identifier risques, invariants et scénarios
  EA->>DA: Comparer options, coûts et preuves
  DA->>Run: Vérifier déploiement, sécurité et reprise
  Run-->>DA: Conditions et écarts documentés
  DA-->>Owner: Décision conditionnelle / NO GO
~~~

## 4. Trajectoire en cinq étapes

1. Définir SoR et classification des jeux de données.
2. Cataloguer contrats, versions, droits et lineage.
3. Choisir CDC, batch ou événements par exigences de fraîcheur.
4. Gouverner zones brutes, validées et produits exposés.
5. Rapprocher volumes et qualité contre sources.

## 5. Scénarios de panne et mesures

| Injection d'échec | Comportement attendu |
|---|---|
| F-01 : Donnée effacée reste dans un index analytique | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-02 : CDC redélivre un changement | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-03 : Producteur change enum sans version | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-04 : Qualité de dataset sous le seuil | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |

**Chaque test** enregistre précondition, commande d'injection autorisée, observations, durée, état de données avant/après, résultat PASS/FAIL et date. Aucune injection destructrice ne doit être faite sur un système réel sans autorisation.

## 6. Décisions candidates / Design Authority

- **ADR-01 — Source unique d'autorité par attribut critique** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-02 — Data product versionné par domaine** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-03 — Lakehouse pour analyse et non écriture transactionnelle** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-04 — Politique de rétention et suppression propagée** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.

## 7. Indicateurs et preuve de succès

- Fraîcheur max des données.
- Pourcentage d'éléments avec lineage.
- Taux de divergence source/projection.
- Taux de contrats incompatibles détectés.

## 8. Architecture non démontrée et questions ouvertes

- Quelle est la source autoritative des données et quel composant exécute les effets métier ?
- Quelles technologies sont déjà en place et supportées contractuellement ?
- Quels objectifs RPO/RTO/SLO proviennent de l'analyse d'impact métier ?
- Quels déploiements, flux, politiques et capacités ont été **mesurés** plutôt que supposés ?
- Quelles approbations rendent la cible admissible en production ?

**Résultat documentaire :** une architecture de référence, non une preuve de réalisation de production.
