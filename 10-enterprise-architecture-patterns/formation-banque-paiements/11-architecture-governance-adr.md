# Cours 11 — Architecture Governance et Architecture Decision Records (ADR)

**Niveau :** Architecture d'entreprise / Gouvernance des choix | **Parcours :** leçon présentée, exercice de validation à faire | [Pattern canonique 11](../11-architecture-governance-adr/README.md)

> Étude pédagogique fictive et anonymisée. Aucune décision ni architecture d'un établissement bancaire réel n'est décrite. Les produits et montants sont illustratifs.

## Compétences visées
1. Distinguer **principes d'architecture**, **standards**, **ADR**, **Design Authority**, **dérogation** et **preuve d'exécution**.
2. Savoir conduire une revue de choix MQ / Kafka / REST sans favoritisme technologique.
3. Rédiger une décision falsifiable : contexte, alternatives, conséquences, invariants, tests, propriétaire et réexamen.
4. Séparer **avis de conception**, **GO conditionnel** et **autorisation de production**.

## 1. Problème métier — quel transport pour le Core Banking ?
Notre banque fictive modernise un moteur Java/JEE vers OpenShift. L'intégration existante avec le Core Banking utilise IBM MQ. Une équipe propose Kafka pour unifier le middleware ; une autre suggère une API REST. L'enjeu métier reste inchangé : **une commande de virement de 500 EUR doit être acheminée, exécutée au plus une fois au niveau autoritatif et suivie jusqu'à un statut attesté**.

Ne pas confondre :
- **Transport accepté** (ACK broker) et **mouvement financier exécuté** (preuve du Core / rail).
- **Rejeu du message** et **rejeu autorisé d'une commande financière**.
- **Standard recommandé** et **obligation applicable à tous les contextes**.
- **POC fonctionnel** et **qualification résilience + sécurité + exploitation**.

## 2. Chaîne de gouvernance
~~~mermaid
flowchart TD
  M["Métier : objectif et invariant financier"] --> A["Architectes : options et impacts inter-SI"]
  A --> O["Évaluer contrats, NFR, sécurité, support, coûts"]
  O --> ADR["ADR proposée, version et owner"]
  ADR --> DA{"Design Authority"}
  DA -->|Acceptée avec preuves| IMP["Implémentation contrôlée"]
  DA -->|Réserves ou conditions| REQ["Tests et remédiations"]
  DA -->|Refusée| REV["Revoir alternatives"]
  REQ --> DA
  IMP --> C["Contrôle de conformité et réexamen"]
~~~

**Design Authority** : instance de décision des choix structurants, composée selon l'organisation (architecture, domaine métier, sécurité, risque, exploitation, données, finance). Elle ne sert pas à approuver automatiquement chaque commit.

## 3. Principes, standards, ADR, dérogations
| Artefact | Exemple bancaire | Gouvernance |
|---|---|---|
| Principe | Un débit financier possède une autorité unique | Règle directrice et impact métier |
| Standard | Contrats versionnés, identifiants stables, journal d'audit | Applicabilité et exceptions formalisées |
| ABB | Transport durable de commandes identifiées | Responsabilités + contrats + NFR |
| SBB | IBM MQ, Kafka+adaptateur ou autre solution | Qualification et support du produit/configuration |
| ADR | Conserver MQ pour les commandes legacy pendant la transition | Options et décision datée |
| Dérogation | Interface temporaire non alignée au standard cible | Responsable, compensation, échéance et sortie |

## 4. ADR détaillée — comparaison de transports
**ADR-PAI-011 (exemple, PROPOSÉE)**  
**Question :** comment conserver un acheminement fiable vers un Core historique pendant la modernisation ?

**Contexte :** paiements SEPA, moteur Java/JEE sur VM, cible applicative OpenShift, commandes MQ historiques, besoin d'événements pour notifications et reporting. Les exigences de délai, débit, budget et de support ne sont pas ici chiffrées ni certifiées.

**Invariant non négociable :** aucune répétition de l'effet financier pour une référence métier ; pas de statut SETTLED issu d'un simple ACK technique ; gestion explicite de UNKNOWN et des échéances.

| Option | Bénéfice plausible | Risque / coût à démontrer |
|---|---|---|
| A — Maintenir IBM MQ pour commandes Core | Continuité des contrats et compétences existants | RUN MQ, licences, résilience et adaptations Java |
| B — Kafka pour commandes Core | Mutualisation potentielle avec l'événementiel | Refonte des consommateurs, transactions, reply, supervision et reprise |
| C — API REST synchrone vers Core | Contrat requête/réponse plus direct | Dépendance temporelle, disponibilité, timeout ambigu |
| D — Mix MQ commandes + Kafka événements | Délimite commandes critiques et faits dérivés | Double exploitation et cohérence DB↔brokers |

**Décision candidate :** pendant la transition, conserver les commandes via MQ si les contrats, support et tests sont satisfaits ; publier les *événements dérivés* vers Kafka après validation durable des statuts. Les alternatives restent réévaluables.

**Conditions d'acceptation :** tests de coupure broker, panne du consommateur, crash après exécution avant ACK, reprise idempotente Core, contrat d'échéance, audit, TLS/ACL, capacité de pointe, plan de rollback, conformité aux règles du scheme applicable.

**Conséquences :** maintien provisoire de deux outils ; coûts et responsabilités supplémentaires ; dette de transition à suivre.

**Responsables à nommer :** sponsor paiement, owner Core, owner intégration, sécurité, exploitation, Design Authority. **Échéance de revue** : à fixer selon la roadmap. **Statut** : `PROPOSED`, jamais `APPROVED` sans décision enregistrée.

## 5. Cycle de vie d'une ADR
~~~mermaid
flowchart LR
  D["DRAFT"] --> P["PROPOSED"]
  P --> A["ACCEPTED sous conditions éventuelles"]
  P --> R["REJECTED"]
  A --> S["SUPERSEDED si choix remplacé"]
  A --> U["REVIEW si conditions changent"]
  U --> P
~~~
Une ADR doit être **append-only sur son historique de décisions** au sens documentaire : un choix dépassé est lié à une nouvelle décision plutôt que réécrit sans traçabilité.

## 6. Fiche type réutilisable
~~~text
ADR-ID : ADR-PAI-xxx
Titre :
Statut : DRAFT | PROPOSED | ACCEPTED | REJECTED | SUPERSEDED
Contexte et besoin métier :
Exigences / NFR / réglementation applicable :
Invariants (ce qui ne doit jamais être violé) :
Options comparées, coût/TCO et dépendances :
Décision candidate et justification :
Conséquences positives et négatives :
Risques résiduels / contrôles compensatoires :
Tests et preuves (nominal, panne, reprise, sécurité, charge) :
Propriétaires et parties consultées :
GO/NO-GO de mise en production (distinct de l'acceptation de l'ADR) :
Date de décision / date de revue :
ADR remplacée ou associée :
~~~

## 7. Risques et scénarios de gouvernance
- **Prototype Kafka réussi, Core non testé** : ne pas autoriser la bascule financière, même si la démonstration de production/consommation est convaincante.
- **Dérogation TLS temporaire** : une exception n'est recevable qu'après évaluation de sécurité, justification, protections acceptables, propriétaire, échéance et décision autorisée ; certains écarts imposent un NO-GO.
- **Nouvelles exigences métier** : rouvrir l'ADR, vérifier que l'ABB est encore satisfait, requalifier les SBB et versionner les contrats.
- **Équipe décide hors Design Authority** : documenter la décision et les impacts ; rétablir le circuit de gouvernance sans bloquer indûment les changements ordinaires.

## 8. Livrables d'architecte senior
Registre des ADR ; dossier d'options et preuves ; principes et standards applicables ; catalogue ABB/SBB ; matrice de risques et de dérogations ; journal des décisions GO/NO-GO ; plan de vérification post-déploiement.

## 9. Exercice corrigé (à faire avant lecture de la correction)
**Situation :** le POC Kafka fonctionne pour remplacer MQ ; aucun test de redélivrance, idempotence Core ou PRA n'a été effectué. La direction veut approuver.

A. Approuver la bascule de production car le POC est vert.  
B. Refuser Kafka définitivement sans comparer.  
C. Enregistrer l'ADR et ses alternatives, poursuivre les travaux autorisés mais bloquer la bascule tant que les preuves critiques manquent.

**Correction : C.** La gouvernance permet la progression des études sans transformer une démonstration fonctionnelle en décision de production. Le comité définit propriétaires, tests, preuve et critères GO/NO-GO.

## 10. Question d'entretien
**Comment défendez-vous une ADR ?** « Je remonte au besoin métier, formule l'invariant, compare des options avec leurs coûts et risques, explicite ce qui est prouvé ou non, puis sollicite une décision datée, traçable, assortie de conditions mesurables et d'un responsable. »

**Approfondissements :** [ADR fictives du système bancaire](../../07-case-studies/banking-payments-reference/decision-records.md) · [Cours 10 ABB/SBB](10-architecture-building-blocks.md) · [Cours 12 conformité](12-architecture-compliance-nfr.md).
