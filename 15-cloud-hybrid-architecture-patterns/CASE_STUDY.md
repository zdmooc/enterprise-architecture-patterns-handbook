# Étude de référence — Architecture cloud hybride et multienvironnement

**Cas fictif / non contractuel / aucun SI d'entreprise réel.**

## 1. Contexte métier et AS-IS

Un patrimoine fictif conserve une base transactionnelle on-prem tandis que ses APIs et calculs analytiques peuvent fonctionner dans une plateforme conteneurisée et une capacité cloud supplémentaire.

**Objectif de transformation :** Déployer des services applicatifs hybrides avec réseau, IAM et coûts maîtrisés, sans déplacement non autorisé des données.

## 2. Hypothèse TO-BE (logique)

~~~mermaid
flowchart LR
  A["Datacenter / autorité données"] --> B["Transit hybride + identité"] --> C["Cloud workloads gouvernés"]
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

1. Définir landing zone, projets et comptes isolés.
2. Cartographier flux et latence WAN entre core et services.
3. Choisir placement selon résidence, licences, coûts et SLO.
4. Mettre liaisons redondantes et politiques transit/egress.
5. Exercer le retrait d'un cloud ou d'un site et l'export des données.

## 5. Scénarios de panne et mesures

| Injection d'échec | Comportement attendu |
|---|---|
| F-01 : Lien privé perdu pendant traitement | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-02 : Routage entre comptes non prévu | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-03 : Application cloud dépasse budget | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-04 : Région de secours a réplication en retard | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |

**Chaque test** enregistre précondition, commande d'injection autorisée, observations, durée, état de données avant/après, résultat PASS/FAIL et date. Aucune injection destructrice ne doit être faite sur un système réel sans autorisation.

## 6. Décisions candidates / Design Authority

- **ADR-01 — Landing zone minimum avant workload** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-02 — Residency et IAM avant placement** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-03 — Lien privé avec plan de dégradation** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-04 — Portabilité testée selon exigences réelles** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.

## 7. Indicateurs et preuve de succès

- p99 du chemin WAN+core.
- Budget cloud par équipe.
- RTO de la liaison hybride.
- Temps/coût d'exit réellement mesuré.

## 8. Architecture non démontrée et questions ouvertes

- Quelle est la source autoritative des données et quel composant exécute les effets métier ?
- Quelles technologies sont déjà en place et supportées contractuellement ?
- Quels objectifs RPO/RTO/SLO proviennent de l'analyse d'impact métier ?
- Quels déploiements, flux, politiques et capacités ont été **mesurés** plutôt que supposés ?
- Quelles approbations rendent la cible admissible en production ?

**Résultat documentaire :** une architecture de référence, non une preuve de réalisation de production.
