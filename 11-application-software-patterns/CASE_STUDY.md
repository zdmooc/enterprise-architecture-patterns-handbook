# Étude de référence — Architecture applicative et conception logicielle

**Cas fictif / non contractuel / aucun SI d'entreprise réel.**

## 1. Contexte métier et AS-IS

Un monolithe Java historique expose HTTP et messages, accède à une DB SQL et met à jour une projection de lecture. Des règles métier se trouvent dans les controllers et des tests end-to-end fragiles ralentissent les releases.

**Objectif de transformation :** Moderniser un système fictif de dossiers avec logique Java et plusieurs consommateurs sans explosion de microservices.

## 2. Hypothèse TO-BE (logique)

~~~mermaid
flowchart LR
  A["Canal & contrat API"] --> B["Modules domaine / ports"] --> C["DB autoritative + projections"]
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

1. Extraire invariants et frontières des agrégats.
2. Choisir monolithe modulaire comme hypothèse de départ.
3. Introduire ports/adapters et tests domaine.
4. Mettre versions de contrats et idempotence sur actions.
5. Extraire services seulement si besoin NFR/ownership prouvé.

## 5. Scénarios de panne et mesures

| Injection d'échec | Comportement attendu |
|---|---|
| F-01 : Deux commandes concurrentes violent un invariant | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-02 : Rejeu d'événement crée un second effet | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-03 : Ancien consommateur ne reconnaît plus un statut | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-04 : Projection de lecture présente une donnée périmée | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |

**Chaque test** enregistre précondition, commande d'injection autorisée, observations, durée, état de données avant/après, résultat PASS/FAIL et date. Aucune injection destructrice ne doit être faite sur un système réel sans autorisation.

## 6. Décisions candidates / Design Authority

- **ADR-01 — Modular monolith avant microservices non justifiés** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-02 — Contrats explicites et tests consumer-driven** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-03 — CQRS seulement si lectures/écritures divergent fortement** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-04 — Cohérence limitée aux frontières transactionnelles** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.

## 7. Indicateurs et preuve de succès

- Couverture des invariants métier.
- Compatibilité de contrats interversions.
- p99 du parcours critique.
- Nombre d'effets dupliqués après crash.

## 8. Architecture non démontrée et questions ouvertes

- Quelle est la source autoritative des données et quel composant exécute les effets métier ?
- Quelles technologies sont déjà en place et supportées contractuellement ?
- Quels objectifs RPO/RTO/SLO proviennent de l'analyse d'impact métier ?
- Quels déploiements, flux, politiques et capacités ont été **mesurés** plutôt que supposés ?
- Quelles approbations rendent la cible admissible en production ?

**Résultat documentaire :** une architecture de référence, non une preuve de réalisation de production.
