# Étude de référence — Sécurité, identité et Zero Trust

**Cas fictif / non contractuel / aucun SI d'entreprise réel.**

## 1. Contexte métier et AS-IS

Un utilisateur connecté possède un token valide mais tente d'accéder à un dossier d'un autre périmètre. Des microservices échangent sur le cluster et certains Secrets sont actuellement distribués trop largement.

**Objectif de transformation :** Protéger un dossier sensible partagé entre API, workloads et documents, y compris contre un acteur interne non autorisé.

## 2. Hypothèse TO-BE (logique)

~~~mermaid
flowchart LR
  A["Identité humaine & workload"] --> B["PDP/PEP + RBAC/ABAC"] --> C["Objet métier + audit chiffré"]
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

1. Classer données et opérations sensibles.
2. Définir identités indépendantes pour utilisateurs et workloads.
3. Appliquer authorization objet au service, jamais seulement Gateway.
4. Segmenter réseau, chiffrer, rotation secrets et registre d'audit.
5. Tester révocation, injection et séparation demandeur/approbateur.

## 5. Scénarios de panne et mesures

| Injection d'échec | Comportement attendu |
|---|---|
| F-01 : Utilisateur avec scope API devine un autre objectId | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-02 : Service utilise credential expiré | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-03 : Pod interne contourne Gateway | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-04 : Un approbateur approuve sa propre action | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |

**Chaque test** enregistre précondition, commande d'injection autorisée, observations, durée, état de données avant/après, résultat PASS/FAIL et date. Aucune injection destructrice ne doit être faite sur un système réel sans autorisation.

## 6. Décisions candidates / Design Authority

- **ADR-01 — Zero Trust à chaque frontière** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-02 — PEP côté service métier pour droits objet** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-03 — Identités courtes durées** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-04 — Approvisionnement et révocation des clés sous contrôle** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.

## 7. Indicateurs et preuve de succès

- Accès inter-tenant réussis : zéro.
- Délai de révocation d'identité.
- Taux de secrets renouvelés à temps.
- Pourcentage de flux couverts par politiques réseau.

## 8. Architecture non démontrée et questions ouvertes

- Quelle est la source autoritative des données et quel composant exécute les effets métier ?
- Quelles technologies sont déjà en place et supportées contractuellement ?
- Quels objectifs RPO/RTO/SLO proviennent de l'analyse d'impact métier ?
- Quels déploiements, flux, politiques et capacités ont été **mesurés** plutôt que supposés ?
- Quelles approbations rendent la cible admissible en production ?

**Résultat documentaire :** une architecture de référence, non une preuve de réalisation de production.
