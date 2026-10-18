# Étude de référence — Performance et SRE

**Cas fictif / non contractuel / aucun SI d'entreprise réel.**

## 1. Contexte métier et AS-IS

Une API Java fictive consomme une DB et un service distant. Elle a 99e percentile trop élevé pendant les bursts ; ajouter des replicas augmente les connexions DB et aggrave la saturation.

**Objectif de transformation :** Respecter les délais d'une API critique malgré pics de charge, dépendance lente et perte d'une zone.

## 2. Hypothèse TO-BE (logique)

~~~mermaid
flowchart LR
  A["Trafic / profils de charge"] --> B["Admission + pools + caches"] --> C["Services + SLI/SLO"]
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

1. Définir SLI depuis point de vue client, classe d'opérations et budget.
2. Mesurer profils, queues, GC, CPU throttle et connexions.
3. Ajouter isolation/backpressure avant autoscaling aveugle.
4. Tester charge/stress/endurance et panne de zone.
5. Utiliser error budget pour arbitrer changements et capacité.

## 5. Scénarios de panne et mesures

| Injection d'échec | Comportement attendu |
|---|---|
| F-01 : Cache affiche statut périmé | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-02 : Autoscaling épuise DB | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-03 : Retry storm dépasse deadline | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-04 : Perte de zone double la charge des survivants | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |

**Chaque test** enregistre précondition, commande d'injection autorisée, observations, durée, état de données avant/après, résultat PASS/FAIL et date. Aucune injection destructrice ne doit être faite sur un système réel sans autorisation.

## 6. Décisions candidates / Design Authority

- **ADR-01 — Budget de latence bout en bout et non moyennes** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-02 — Pool maximum global cohérent** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-03 — Rate limits équitables** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-04 — SLO pilotant les releases** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.

## 7. Indicateurs et preuve de succès

- p95/p99 bout en bout.
- Taux de saturation pool.
- Requêtes rejetées correctement.
- Évolution error budget sous incidents.

## 8. Architecture non démontrée et questions ouvertes

- Quelle est la source autoritative des données et quel composant exécute les effets métier ?
- Quelles technologies sont déjà en place et supportées contractuellement ?
- Quels objectifs RPO/RTO/SLO proviennent de l'analyse d'impact métier ?
- Quels déploiements, flux, politiques et capacités ont été **mesurés** plutôt que supposés ?
- Quelles approbations rendent la cible admissible en production ?

**Résultat documentaire :** une architecture de référence, non une preuve de réalisation de production.
