# Cours 10 — Architecture Building Blocks (ABB) et Solution Building Blocks (SBB)
**Niveau :** Architecture d'entreprise / standardisation | **Progression :** QCM B validé | [Fiche canonique](../10-architecture-building-blocks/README.md)

## Objectifs
Distinguer une **responsabilité architecturale réutilisable** (ABB) de sa **réalisation technique** (SBB), définir les contrats et NFR de chaque ABB et gouverner les alternatives de mise en œuvre sans imposer un produit par défaut.

## 1. Distinction fondamentale
- **ABB (Architecture Building Block)** : décrit *quoi doit être assuré*, selon quelles interfaces, contraintes et propriétés, sans choix prématuré de fournisseur.
- **SBB (Solution Building Block)** : fournit une implémentation concrète qualifiée, parfois composée de plusieurs produits, configurations, adaptateurs et pratiques d'exploitation.
- **Architecture contractuelle** : un SBB n'est acceptable que s'il satisfait les interfaces, les invariants et les NFR du ou des ABB concernés.

**Cas bancaire :** ABB « transmission durable des commandes » avec corrélation, reprise, confidentialité et âge maximum ; SBB candidat « IBM MQ configuré avec queue manager, queues, clients JMS, TLS, gestion backout et procédures RUN ». Un cluster MQ n'assure pas seul l'unicité des effets financiers.

## 2. Cartographie ABB ↔ SBB
| ABB (responsabilité) | SBB candidat | Obligation |
|---|---|---|
| Exposition d'API | Gateway + mécanismes IAM | Authentification, contrôle d'accès, quotas |
| Orchestration métier | Service Java/OpenShift | Statuts durables, transactions explicites |
| Messages de commande | IBM MQ + adaptateur | Durabilité, corrélation, redélivrance contrôlée |
| Diffusion de faits | Kafka + relay Outbox | Schémas, abonnement, replay sous rétention |
| Exécution de compte | Core Banking | Autorité financière et preuve |
| Hébergement | OpenShift + GitOps | Exploitabilité, sécurité, stratégie de déploiement |
| État local | PostgreSQL | Intention unique, Outbox atomique |
| Observabilité | OpenTelemetry/Prometheus | Traces, métriques, journal de décision |

Ces correspondances sont **candidates** : un SBB peut servir plusieurs ABB et un ABB peut exiger plusieurs composants.

## 3. Exemple d'assemblage
~~~mermaid
flowchart TB
  A["ABB : accepter intention"] --> B["ABB : orchestrer ordre"]
  B --> C["ABB : transporter commande"]
  C --> D["ABB : appliquer effet financier"]
  B --> E["ABB : diffuser faits"]
  F["SBB : API Gateway / Payment API"] -. "implémente" .-> A
  G["SBB : Java / OpenShift"] -. "implémente" .-> B
  H["SBB : IBM MQ / JMS"] -. "implémente" .-> C
  I["SBB : Core Banking"] -. "implémente" .-> D
  J["SBB : Kafka / Outbox"] -. "implémente" .-> E
~~~

## 4. Fiche d'ABB — commandes financières
**Identifiant :** ABB-PAIEMENT-MSG-01  
**Objet :** acheminer des instructions avec identité métier, échéance et traçabilité.  
**Entrée :** ExecutePayment(paymentId, amountMinor, currency, deadlineUtc, schemaVersion).  
**Sortie :** accusé de transport distinct de PaymentResult métier.  
**Invariants :** pas de re-débit pour une commande déjà traitée, gestion de l'issue UNKNOWN, refus/réconciliation des commandes hors échéance.  
**NFR :** sécurité, délai, capacité, audit, reprise et compatibilité de versions définis par propriétaire.  
**Épreuves :** crash producteur, perte ACK, arrêt consommateur, message dupliqué, délai expiré, perte broker et restauration.  
**Alternatives :** file MQ, Kafka avec adaptateur et modèle explicite, API synchrone + mécanisme de reprise, ou solution existante répondant au contrat.

## 5. Évaluer IBM MQ contre Kafka pour cet ABB
| Critère | IBM MQ | Kafka | Arbitrage |
|---|---|---|---|
| Intégration du Core historique | Contrats potentiellement existants | Adaptateurs à développer ou qualifier | Réutilisation et coûts |
| File de travail et request/reply | Modèle direct | Modèle à concevoir | Besoin réel |
| Historique rejouable | Pas automatique après consommation | Offsets sous rétention | Besoin d'abonnés |
| Exactly once externe | Non fourni seul | Non fourni seul | Idempotence Core |
| Exploitation | Queue manager, canaux, BOQ/DLQ | Brokers, partitions, lag | Compétences et RUN |
| Choix final | À tester | À tester | ADR et preuves |

## 6. Gouvernance
1. Cataloguer l'ABB avec owner métier/architecture et responsabilités.
2. Versionner interfaces, modèles de messages et exigences NFR.
3. Inventorier les SBB candidats, licences, TCO, compétences, dépendances et modes de panne.
4. Définir les cas de test comparatifs, les preuves minimales et la substituabilité effective.
5. Soumettre l'ADR à la Design Authority ; tracer acceptation, réserve ou refus.
6. Contrôler à l'exploitation que le SBB reste conforme ; réviser si les besoins évoluent.

~~~mermaid
flowchart LR
  R["Besoin métier"] --> ABB["ABB + contrats + NFR"]
  ABB --> E["Évaluation des SBB"]
  E --> A["ADR / comité"]
  A --> P["Implémentation et tests"]
  P --> C["Conformité / réexamen"]
~~~

## 7. Anti-patterns et limites
- Imposer Kafka ou IBM MQ comme « standard universel » avant de définir les besoins.
- Multiplier les ABB qui reproduisent exactement l'organigramme ou les composants produits.
- Déclarer un SBB « substituable » malgré des contrats propriétaires non repris.
- Confondre capacité métier « gérer les paiements » et ABB d'intégration « transporter les commandes ».
- Déduire la fiabilité métier de la disponibilité technique du broker.

## 8. Livrables
Catalogue ABB ; fiches de contrats et NFR ; inventaire SBB ; matrice de conformité ABB↔SBB ; matrice d'alternatives et coûts ; cas d'essai ; ADR ; dérogations temporaires et dates de révision.

## 9. Exercice corrigé
Proposition : remplacer IBM MQ par Kafka pour le transport des commandes. (A) approuver car plus récent, (B) évaluer les deux contre ABB/contrats/NFR et tests, (C) bloquer toute évolution.

**Correction : B.** Un bon SBB est celui qui démontre qu'il réalise l'ABB au coût et au risque acceptables. La réponse ne présume pas du vainqueur.

## 10. Question d'entretien
**« ABB ou SBB ? »** ABB formalise responsabilités et contrats ; SBB est la solution évaluée et gouvernée qui les réalise. Un remplacement n'est acceptable que si invariants, NFR et coût de transition sont pris en compte.

---

## Périmètre et intégrité pédagogique
Tous les exemples représentent un **SI bancaire fictif** et non l'architecture réelle d'un client. Les SLO, volumes, technologies et stratégies sont des hypothèses de conception ; les preuves de production ne sont pas revendiquées. Pour des paiements, un statut de transport n'est pas un règlement, un timeout ne démontre pas un échec, et une compensation applicative ne défait pas nécessairement un règlement irréversible. Les échéances métier et règles effectives du scheme doivent être validées.
