# Étude de référence — Systèmes distribués et résilience

**Cas fictif / non contractuel / aucun SI d'entreprise réel.**

## 1. Contexte métier et AS-IS

Deux sites fictifs servent des partitions de dossiers. Le site A enregistre un commit, la réponse se perd, puis une coupure WAN intervient avant réplication complète. Le site B doit décider s'il peut reprendre.

**Objectif de transformation :** Survivre à la perte de service, de réseau et de site sans double effet autoritatif.

## 2. Hypothèse TO-BE (logique)

~~~mermaid
flowchart LR
  A["Site A : writer & commits"] --> B["Quorum / fencing / reconciliation"] --> C["Site B : writer uniquement après preuve"]
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

1. Définir ce que signifie « commit reconnu » et où sont les preuves.
2. Choisir ownership unique et epoch/fencing à l'autorité d'écriture.
3. Identifier réplication sync/async et objectif RPO attestable.
4. Tester split-brain, timeout, ACK perdu et backup/PITR.
5. Ouvrir le service progressivement après réconciliation.

## 5. Scénarios de panne et mesures

| Injection d'échec | Comportement attendu |
|---|---|
| F-01 : Site A continue à écrire après promotion de B | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-02 : Réplication async manque des commits acquittés | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-03 : Deux leaders actifs durant partition réseau | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |
| F-04 : Restaurer backup sans clés de déchiffrement | Détecter, préserver l'invariant, garder un état durable, rapprocher avec les preuves, alerter et refuser toute mutation incertaine |

**Chaque test** enregistre précondition, commande d'injection autorisée, observations, durée, état de données avant/après, résultat PASS/FAIL et date. Aucune injection destructrice ne doit être faite sur un système réel sans autorisation.

## 6. Décisions candidates / Design Authority

- **ADR-01 — Un writer par partition** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-02 — Fencing validé par l'autorité de stockage/compte** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-03 — Bascule conditionnée par commits visibles** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.
- **ADR-04 — PRA/RTO mesurés par exercice** : confirmer contexte, alternative, coûts, impact sur les NFR et tests.

## 7. Indicateurs et preuve de succès

- Duplication d'effets : cible zéro.
- Ordres/commits reconnus perdus : cible zéro à démontrer.
- RTO réel par domaine de panne.
- Ancienneté des états UNKNOWN.

## 8. Architecture non démontrée et questions ouvertes

- Quelle est la source autoritative des données et quel composant exécute les effets métier ?
- Quelles technologies sont déjà en place et supportées contractuellement ?
- Quels objectifs RPO/RTO/SLO proviennent de l'analyse d'impact métier ?
- Quels déploiements, flux, politiques et capacités ont été **mesurés** plutôt que supposés ?
- Quelles approbations rendent la cible admissible en production ?

**Résultat documentaire :** une architecture de référence, non une preuve de réalisation de production.
