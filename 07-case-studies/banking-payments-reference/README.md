# Cas d'étude — Architecture bancaire de paiement bout en bout

**Référence métier externe :** [architecture métier unique des paiements bancaires](https://github.com/zdmooc/banking-payments-business-architecture). Ce document est un exercice spécialisé et ne doit pas être consulté comme dictionnaire de règles de paiement.


> **Simulation de conception, pas description d'un SI bancaire réel.** Aucun produit (MQ, Kafka, PostgreSQL, OpenShift) n'est présenté comme effectivement déployé dans un établissement. Montants, comptes, noms des files et services sont fictifs.

## Objectif
Concevoir un virement de **500 EUR** initié par application bancaire, accepté dans un canal API, contrôlé, transmis à un cœur bancaire historique et suivi jusqu'au résultat autoritatif, sans doublons après crash/retry. Démontrer comment les **10 patterns** coopèrent sans confondre commande, message, événement, ordre accepté et règlement définitif.

## Vue logique
~~~mermaid
flowchart TB
  UI["Web / Mobile / Partner"]
  IDP["Identity Provider / SCA"]
  GW["API Gateway / APIM"]
  ROUTE["OpenShift Route"]
  API["Payment API Java"]
  PG[("PostgreSQL : intention, état, Outbox")]
  SAGA["Saga Orchestrator"]
  CTRL["Contrôles métier / antifraude"]
  ACL["Anti-Corruption Layer + MQ adapter"]
  RELAY["Relais Outbox"]
  MQ["messagerie MQ PAYMENT.REQUEST / RESPONSE"]
  CORE["Cœur bancaire, autorité financière"]
  CLEAR["Infrastructure de paiement / règlement"]
  KAFKA["Kafka payments.status.v1"]
  NOTIF["Notifications"]
  ANA["Analytique / Observabilité"]
  UI -->|HTTPS + token + idem-key| GW --> ROUTE --> API
  UI <-.-> IDP
  GW <-.-> IDP
  API --> PG
  API --> SAGA
  SAGA --> CTRL
  SAGA <--> PG
  SAGA --> ACL
  ACL --> PG
  PG --> RELAY
  RELAY --> MQ
  MQ <--> CORE <--> CLEAR
  MQ -->|Réponse via adapter, durablement traitée| ACL
  PG -->|Outbox event relay| KAFKA
  KAFKA --> NOTIF
  KAFKA --> ANA
~~~
Les flèches sont **logiques** ; notamment, la publication des commandes au broker s'effectue par un relais durable. Le schéma ne prétend pas qu'un composant unique ait des transactions ACID simultanées sur PostgreSQL, MQ et le cœur bancaire.

## Responsabilités et propriété des données

| Composant | Propriétaire de | Ne doit PAS faire |
|---|---|---|
| API Gateway | Contrôle runtime des appels | Décider que des fonds sont réglés |
| Payment API | Contrat/API + unicité de l'intention | Exécuter deux fois une même instruction |
| PostgreSQL | État de suivi, réservation Saga si sous ce domaine, Outbox | Devenir un second grand livre bancaire |
| Saga | Coordination durable et transitions | Annuler un règlement irrévocable par « rollback » |
| ACL | Traductions de données et sémantiques | Convertir « accepté » en « exécuté » |
| messagerie MQ | Transport durable de commandes/réponses | Garantir la sémantique exactly-once externe |
| Cœur bancaire | Effet financier autoritatif | Exécuter une commande expirée sans vérification |
| Kafka | Journal d'événements dérivés | Devenir l'unique preuve de règlement |
| Notification | Informer, avec retries propres | Relancer l'ordre de paiement |

## Décisions structurantes
1. **API synchrone** pour créer une intention durable et retourner un identifiant, puis suivi fiable de statut.
2. **Unicité de l'intention** par scope+idempotencyKey+empreinte de payload ; unicité de la commande au cœur.
3. **Outbox** transactionnelle pour messages de commande et événements métier ; relais **at least once**, consommateurs idempotents.
4. **Saga orchestrée** pour suivi des étapes et compensations réversibles.
5. **ACL** protège Java moderne de MQ/COBOL legacy.
6. **MQ** pour l'intégration commandée et la réponse du cœur historique.
7. **Kafka** pour diffusion aux abonnés non critiques après validation durable de l'état.
8. **Circuit Breaker / Bulkhead / Timeout** à chaque dépendance selon son contrat.
9. **Réconciliation** pour l'issue inconnue ; aucun mensonge métier en cas de perte de réponse.
10. **Deadline d'exécution SCT Inst** transportée et vérifiée au dernier composant capable d'ordonner l'exécution.

## Statuts et délais : autorité métier centralisée

Les états `RECEIVED`, `SUBMITTED`, `SETTLED`, `REJECTED`, `UNKNOWN` et les obligations SCT Inst ne sont **pas** redéfinis par les patterns d'intégration ci-dessus. Leur sens, leur preuve et le traitement des résultats non confirmés figurent dans [les états métier canoniques](https://github.com/zdmooc/banking-payments-business-architecture/blob/main/04-capacites-metier/ETATS_INVARIANTS.md), le [processus SCT Inst détaillé](https://github.com/zdmooc/banking-payments-business-architecture/blob/main/15-processus-bpmn/PARCOURS_SCT_INST_METIER_12_ETAPES.md) et les [obligations d'exceptions](https://github.com/zdmooc/banking-payments-business-architecture/blob/main/06-sepa-sct-inst/REFERENTIEL_R_TRANSACTIONS_2026.md).

Ici, la Saga, l'Outbox, MQ, Kafka et l'ACL décrivent des **choix de réalisation** : ils ne modifient ni les délais applicables ni le résultat financier.

**Version originale des règles remplacées** : [historique Git 4080ad42](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/4080ad420f8151131d105728c4e52b6d9f6578e7/07-case-studies/banking-payments-reference/README.md).

## Sujets de revue avant toute production
- Partage exact des responsabilités PSP/CSM/settlement et conditions d'irrévocabilité.
- Chiffrement, contrôle d'accès objet, SCA, journaux auditables et rétention adaptée.
- Réalisation de tests de charge au percentile et scénarios d'indisponibilité.
- SLA/SLO du parcours, de la réconciliation, des notifications et de l'Outbox.
- Haute disponibilité DB/brokers, stratégie DR, RTO/RPO et exercices réels.
- Versionnement API, payloads MQ, événements Kafka et schémas legacy.
- Gouvernance des changements avec Design Authority et ADR.

**À lire ensuite :** [séquence complète](sequences.md), [pannes et tests](failure-matrix.md), [ADR](decision-records.md), [règles de choix](../../references/decision-matrix.md).
