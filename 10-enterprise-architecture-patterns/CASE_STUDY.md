# Étude de référence — Architecture d'entreprise et urbanisation

**Cas fictif / non contractuel / aucun SI d'entreprise réel.**

## 1. Contexte métier et AS-IS

Une organisation fictive possède des applications de gestion des dossiers, contrats, clients et mouvements. Certains flux sont non documentés, des applications partagent des données et les coûts d'exploitation augmentent.

**Objectif de transformation :** Transformer un patrimoine de 80 applications fictives sans interrompre les fonctions critiques.

## 2. Hypothèse TO-BE (logique)

~~~mermaid
flowchart LR
  A["Capacités métier et valeur"] --> B["Cartographie AS-IS et flux"] --> C["Cible/Transitions/Roadmap"]
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

1. Nommer les domaines et propriétaires des données.
2. Inventorier applications et flux prouvés par observations.
3. Scorer capacités, coûts et risques selon critères publiés.
4. Produire cible logique, ABB/SBB, trajectoires et ADR.
5. Découper en vagues réversibles et fermer les dépendances.

## 5. Scénarios de panne et mesures

| Injection d'échec | Comportement attendu |
|---|---|
| F-01 : Retrait d'une application avec flux caché | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-02 : Deux domaines se déclarent propriétaires d'une même donnée | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-03 : Architecture cible approuvée sans plan de financement | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-04 : Transition active deux chemins d'écriture | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |

**Chaque test** enregistre précondition, commande d'injection autorisée, observations, durée, état de données avant/après, résultat PASS/FAIL et date. Aucune injection destructrice ne doit être faite sur un système réel sans autorisation.

## 6. Décisions candidates / Design Authority

- **ADR-01 — Architecture cible par domaine métier** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-02 — Phases de migration et propriétaire d'écriture unique** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-03 — Gouvernance ADR et dérogations** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-04 — Rationalisation à partir de critères valeur/risque** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.

## 7. Indicateurs et preuve de succès

- Couverture des capacités cartographiées.
- Part des flux critiques vérifiés.
- Nombre d'applications avec propriétaire et décision TIME.
- Incidents de coupure après migration.

## 8. Architecture non démontrée et questions ouvertes

- Quelle est la source autoritative des données et quel composant exécute les effets métier ?
- Quelles technologies sont déjà en place et supportées contractuellement ?
- Quels objectifs RPO/RTO/SLO proviennent de l'analyse d'impact métier ?
- Quels déploiements, flux, politiques et capacités ont été **mesurés** plutôt que supposés ?
- Quelles approbations rendent la cible admissible en production ?

**Résultat documentaire :** une architecture de référence, non une preuve de réalisation de production.
