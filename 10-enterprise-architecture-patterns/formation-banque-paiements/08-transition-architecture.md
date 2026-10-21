# Cours 08 — Transition Architecture / Architecture intermédiaire
**Niveau :** Architecture de transformation | **Progression :** QCM B validé | [Fiche canonique](../08-transition-architecture/README.md)

## Objectifs
Concevoir les **états intermédiaires exploitables** entre moteur Java/JEE sur VM et moteur modernisé sur OpenShift. Assurer coexistence contrôlée, responsabilité unique d'écriture, cutover réconcilié et rollback sans réexécution financière.

## 1. Trois états distincts
- **AS-IS** : ancien moteur reçoit les ordres et pilote l'intégration MQ/Core.
- **TRANSITION** : ancien et nouveau moteurs coexistent ; un routeur stable décide **par catégorie/ordre** qui pilote un nouvel ordre. Les ordres en cours conservent leur autorité et leur référence.
- **TO-BE** : nouveau moteur pilote le périmètre approuvé ; les dépendances héritées conservées ou retirées selon des décisions séparées.

~~~mermaid
flowchart LR
  A["AS-IS : Java/JEE VM"] --> B["Transition : legacy + OpenShift"]
  B --> C["TO-BE : nouveau moteur"]
  B --> D["Propriétaire unique par ordre"]
  D --> E["Journal des références / rapprochement"]
~~~

## 2. Architecture de coexistence
~~~mermaid
flowchart TB
  UI["Canaux"] --> ROUTE["Routage métier stable + idempotence"]
  ROUTE -->|"Périmètre legacy"| OLD["Ancien moteur Java/JEE"]
  ROUTE -->|"Périmètre migré"| NEW["Nouveau moteur OpenShift"]
  OLD --> L["Adaptateur legacy"]
  NEW --> N["Adaptateur cible"]
  L --> MQ["IBM MQ"]
  N --> MQ
  MQ --> CORE["Core Banking autoritatif"]
  CORE --> R["Résultat corrélé VIR-001"]
  R --> OWN["Router résultat vers propriétaire de l'ordre"]
  OWN --> OLD
  OWN --> NEW
  CORE -.-> RECO["Réconciliation financière"]
~~~
**Interdit** : rejouer la même commande financière sous un nouvel identifiant depuis les deux moteurs, ou publier un SETTLED sans preuve. Le routage doit survivre au redémarrage (état durable), traiter les requêtes répétées et les retours tardifs.

## 3. Shadow ≠ double exécution
- Shadow **lecture seule**, avec données sécurisées/synthétiques : on compare comportements, règles et temps.
- Toute sortie ayant un effet réel est inhibée : débit, instruction au Core, notification sensible ou transaction externe.
- Les écarts sont classés : contrat, valeur calculée, latence, horodatage, état, décision.
- L'absence d'écart critique ne suffit pas : risques licences/support, backpressure et PRA restent à tester.

## 4. Canary métier et cutover
Un « 10 % HTTP » aléatoire ne suffit pas : un réessai du même paymentId doit rester orienté vers **le même propriétaire** jusqu'à résolution.

**Cutover contrôlé proposé :**
1. Geler l'admission des *nouveaux* ordres sur le périmètre concerné.
2. Identifier les transactions en vol (DB, MQ, jobs, résultats et événements retardés).
3. Drainer ce qui peut être achevé ; placer les issues non confirmées en réconciliation.
4. Prendre un checkpoint auditable d'ownership et des références.
5. Transférer le droit de créer de nouveaux ordres selon la clé/règle de routage durable.
6. Réouvrir et mesurer : double effet, statuts, p99, rejets, timeouts, âge MQ.
7. Décommissionner les chemins temporaires **seulement après preuves**.

## 5. Rollback et restrictions financières
~~~mermaid
flowchart TB
  E["Anomalie en canary"] --> S["Suspendre nouvelles admissions concernées"]
  S --> D["Drainer et inventorier les ordres en vol"]
  D --> R["Interroger Core et réconcilier"]
  R --> C{"Compatibilité données / contrats prouvée ?"}
  C -->|Oui| O["Rerouter uniquement nouveaux ordres vers legacy"]
  C -->|Non| I["Garder admission suspendue ; incident et reprise supervisés"]
~~~

Un rollback de code **n'annule jamais** automatiquement un virement déjà réglé. Les effets irréversibles exigent un processus métier spécifique. Une base modifiée de façon incompatible peut empêcher le retour à l'ancienne version. Prévoir vérification de schémas et plan de réconciliation.

## 6. Préflight technique Java/JEE pour OpenShift
| Objet | Contrôle | Risque |
|---|---|---|
| EAR/WAR/EJB | Bibliothèques et API supportées | Chargement de classes / runtime |
| JNDI, JDBC, JTA/XA | Datasources et transactions | Commit partiel / rollback ambigu |
| JMS/IBM MQ | Files, DLQ/BOQ, redélivraison | Commandes doublées |
| Fichiers/sessions | État local vs externe | Perte au redémarrage |
| SIGTERM / probes | Arrêt gracieux, drain | Ordres en vol abandonnés |
| Sécurité/licences | Certificats, SCC, support éditeur | Déploiement non conforme |

## 7. Matrice des défaillances
- Crash nouveau moteur **avant** publication : Outbox et reprise contrôlée.
- Crash **après** effet Core mais avant ACK : dédupliquer côté Core et réconcilier.
- Deux chemins d'écriture actifs : verrouillage/fencing logique et alerte.
- Retour tardif vers ancien consommateur : corrélation et propriété durable.
- Ordre instantané expiré : ne pas exécuter aveuglément en différé.

## 8. Livrables
Diagrammes AS-IS, états intermédiaires et cible ; stratégie de routage stable ; plan shadow/canary ; plan cutover ; matrice des ordres en vol ; ADR d'ownership ; plan de rollback/failback ; preuves de tests et d'exploitabilité.

## 9. Exercice corrigé
Incident OpenShift en plein canary. (A) recommencer tous les ordres sur le legacy, (B) suspendre admission, réconcilier, rediriger seulement les nouveaux ordres si sûr, (C) effacer MQ.

**Correction : B.** La priorité est de préserver l'unicité de l'effet financier et de connaître les ordres déjà engagés. Rejouer depuis zéro provoquerait potentiellement des doubles débits.

## 10. Question d'entretien
**« Comment gérez-vous une migration transactionnelle sans big bang ? »** En faisant vivre des architectures intermédiaires supervisables, avec routage déterministe, propriétaire unique de chaque instruction, shadow sans effet et cutover/rollback appuyés sur réconciliation.

---

## Périmètre et intégrité pédagogique
Tous les exemples représentent un **SI bancaire fictif** et non l'architecture réelle d'un client. Les SLO, volumes, technologies et stratégies sont des hypothèses de conception ; les preuves de production ne sont pas revendiquées. Pour des paiements, un statut de transport n'est pas un règlement, un timeout ne démontre pas un échec, et une compensation applicative ne défait pas nécessairement un règlement irréversible. Les échéances métier et règles effectives du scheme doivent être validées.
