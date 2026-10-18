# 05 — Event Streaming (Apache Kafka)

## Problème
Analyser des volumes importants de transactions en continu, les redistribuer à plusieurs applications et **rejouer** une période disponible dans la rétention : supervision, fraude, analytics et reconstruction de projections.

## Kafka : modèle logique
~~~mermaid
flowchart LR
  P1["Paiements carte"] --> T["Topic payments.events.v1<br/>P0 | P1 | P2"]
  P2["Virements"] --> T
  T --> F["Consumer group: fraude"]
  T --> R["Consumer group: reporting"]
  T --> O["Consumer group: observabilité"]
~~~

- **Topic** : journal logique ; **partition** : journal ordonné de records ; **offset** : position dans une partition.
- **Producer** : écrit ; **Consumer Group** : instances se répartissant les partitions ; un autre groupe reçoit le même flux logiquement.
- **Clé d'agrégat** : choisir paymentId pour garder la succession de statuts d'un paiement dans une même partition. Pas d'ordre global garanti entre partitions.
- **Rétention** : période/volume de conservation configurés, indépendante du fait d'avoir lu ; après expiration, replay impossible depuis le topic.
- **Lag** : retard d'un groupe sur les partitions ; doit être surveillé par service et adapté aux SLO.
- **Compaction** : option distincte de la rétention temporelle ; conserve typiquement la dernière valeur par clé suivant règles et configuration, ne remplace pas un historique financier complet.

## Détection d'anomalies : scénario
Une série de cinq transactions en 20 secondes est regroupée dans une fenêtre événementielle de 30 secondes pour détecter un comportement suspect. La fraude présumée appelle un contrôle et non une déclaration automatique de fraude prouvée. Si l'autorisation carte doit être bloquée **avant** le paiement, le chemin de décision synchrone/temps réel doit disposer d'un SLO et de contrôles dédiés : le reporting post-règlement ne suffit pas.

## Garanties de livraison
L'idempotence du producteur Kafka, ses transactions et l'exactly-once processing **dans le périmètre Kafka supporté** ne protègent pas automatiquement un système externe (DB, cœur bancaire, PSP). Prévoir déduplication métier à la destination. Si des transactions DB et Kafka doivent être coordonnées, étudier Outbox/CDC ; vérifier rejouabilité des consommateurs.

## Gouvernance et sécurité
- ACL des topics, chiffrement TLS, SASL/mTLS selon installation ; schémas enregistrés et versionnés.
- Separer topics de commande critique et événements dérivés ; classification des données et minimisation.
- Fixer partitions selon débit, parallélisme, coût et ordre par clé ; la hausse du nombre de partitions peut modifier l'affectation d'une clé.
- Configurer réplication, paramètres de durabilité/ACK, disponibilité, stockage et rétention ; tester perte de broker.
- Contrôler producer errors, under-replicated partitions, disk, ISR, consumer lag, rebalance, délais end-to-end.

## Kafka vs messagerie MQ
| Critère | Kafka | messagerie MQ |
|---|---|---|
| Modèle mis en valeur | Journal d'événements partitionné, plusieurs groupes | Files de travail, commandes et request/reply |
| Après consommation | Conserve selon rétention | Message généralement retiré après commit GET |
| Replay | Offsets sur données encore conservées | Redélivrance/reprise de messages non consommés ou républiés |
| Ordre | Dans une partition | Dépend des files, priorité, consommateurs et configuration |
| Exactly once externe | Non automatique | Non automatique |

Les deux savent transporter des messages et diffuser de l'information ; le choix dépend des exigences, pas d'un slogan.

## Pannes à tester
1. Perte de la connexion broker pendant publication.
2. Crash consommateur entre effet dans DB et commit d'offset.
3. Rebalance avec traitement en vol.
4. Désérialisation de schéma incompatible (parking, alerte, correction).
5. Lag dépassant la rétention et reconstruction par source autoritative.

## Questions / checklist
Pourquoi partitionner par paymentId ? Préserver l'ordre par paiement. Que signifie le lag ? Un retard de lecture et pas une preuve d'échec financier. Que faire si un topic n'a plus l'historique nécessaire ? Reconstituer depuis la source autoritative / snapshot validé.

Sources : [Kafka — partitionnement](https://kafka.apache.org/40/design/protocol/), [Kafka — offset tracking](https://kafka.apache.org/40/implementation/distribution/).
