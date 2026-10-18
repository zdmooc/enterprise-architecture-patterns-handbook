# Étude de référence — Modernisation des applications et systèmes historiques

**Cas fictif / non contractuel / aucun SI d'entreprise réel.**

## 1. Contexte métier et AS-IS

Un serveur fictif héberge EAR/WAR, JMS, JDBC, sessions et batch. La cible envisagée est un runtime supporté sur Kubernetes/OpenShift, mais les dépendances et contrats de licence sont à valider.

**Objectif de transformation :** Migrer une application Java/JEE historique sans interrompre ses contrats ni déclencher deux traitements.

## 2. Hypothèse TO-BE (logique)

~~~mermaid
flowchart LR
  A["EAR/WAR & dépendances historiques"] --> B["Façade / tests contrats / shadow"] --> C["Nouvelle capacité sur OpenShift"]
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

1. Inventorier WAR/EAR, JNDI, JMS, transactions, filesystem et support.
2. Décider rehost/replatform/refactor/replace/retain par fit-gap.
3. Créer image non-root, config externe et tests de caractérisation.
4. Exécuter shadow READ-ONLY, mesurer écarts et readiness.
5. Bascule writer unique, drain et rapprochement des travaux en vol.

## 5. Scénarios de panne et mesures

| Injection d'échec | Comportement attendu |
|---|---|
| F-01 : Deux chemins émettent une commande | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-02 : Schema DB incompatible après rollback | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-03 : Session JEE perdue après rescheduling | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-04 : Runtime construit mais hors support/licence | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |

**Chaque test** enregistre précondition, commande d'injection autorisée, observations, durée, état de données avant/après, résultat PASS/FAIL et date. Aucune injection destructrice ne doit être faite sur un système réel sans autorisation.

## 6. Décisions candidates / Design Authority

- **ADR-01 — Strangler graduel et non big bang** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-02 — Shadow sans effets externes** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-03 — Expand–Contract des schémas** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-04 — Cutover contrôlé et rollback borné** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.

## 7. Indicateurs et preuve de succès

- Écarts fonctionnels non expliqués.
- Contrats passés après upgrade runtime.
- Coupures clients au cutover.
- Effets dupliqués lors de reprise.

## 8. Architecture non démontrée et questions ouvertes

- Quelle est la source autoritative des données et quel composant exécute les effets métier ?
- Quelles technologies sont déjà en place et supportées contractuellement ?
- Quels objectifs RPO/RTO/SLO proviennent de l'analyse d'impact métier ?
- Quels déploiements, flux, politiques et capacités ont été **mesurés** plutôt que supposés ?
- Quelles approbations rendent la cible admissible en production ?

**Résultat documentaire :** une architecture de référence, non une preuve de réalisation de production.
