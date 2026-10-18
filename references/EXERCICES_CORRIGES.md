# Exercices corrigés — les 10 patterns sur un virement fictif de 500 €

**Consigne :** répondre avant de regarder la solution. Ces exercices reprennent les situations de compréhension de la formation ; les réponses sont pédagogiques et ne décrivent aucun système bancaire réel.

## 1 — Request / Response
**Question.** Une API de statut ne répond pas avant son timeout. Le client doit-il afficher « virement rejeté » ?
- A. Oui, le paiement n'existe pas.
- B. Non, le statut est indisponible et doit être vérifié.
- C. Oui, si le serveur est sur OpenShift.

**Réponse B.** Un délai dépassé prouve uniquement que la réponse n'est pas arrivée à temps. Une lecture peut être retentée de manière bornée ; une exécution exige davantage de précautions.

## 2 — Messaging / Queue
**Question.** Le consommateur est arrêté dix minutes. La queue durable contient trois messages.
- A. Le broker exécute automatiquement les paiements.
- B. Les messages restent conservés selon la configuration ; le consommateur les reprend après redémarrage.
- C. Les ordres sont toujours supprimés.

**Réponse B.** Mais, pour un SCT Inst, l'échéance de traitement peut rendre un ordre ancien **non admissible à une exécution tardive**. Le broker n'est pas l'autorité financière.

## 3 — Publish / Subscribe
**Question.** La notification tombe en panne, mais la comptabilité reste disponible. Doit-elle attendre ?
- A. Non, chaque abonnement fonctionne indépendamment.
- B. Oui, tous les abonnés sont bloqués.
- C. L'émetteur doit appeler synchroniquement chaque consommateur.

**Réponse A.** La capacité de reprise d'un abonnement dépend du broker et de ses politiques de rétention.

## 4 — Event-Driven Architecture
**Question.** Un événement \`FundsReserved\` déclenche un contrôle, qui publie \`RiskApproved\`, puis une étape d'exécution. Quel concept organise ce comportement ?
- A. REST simple.
- B. EDA.
- C. Une transaction SQL unique.

**Réponse B.** Le bus distribue les événements, mais **l'architecture** coordonne les réactions. Pour les commandes critiques, on peut utiliser une Saga durable.

## 5 — Event Streaming
**Question.** Le système doit analyser les transactions en continu et rejouer l'historique des 24 dernières heures.
- A. Un POST REST sans journal.
- B. Un flux de streaming avec rétention suffisante et moteur d'analyse.
- C. Des callbacks sans stockage.

**Réponse B.** Kafka offre journal partitionné, offsets et groupes indépendants ; le replay reste borné par la rétention. Il ne remplace pas l'autorité financière.

## 6 — API Gateway
**Question.** Exposer plusieurs API sécurisées, publier leurs versions et suivre les abonnements : quel ensemble ?
- A. Une Route seule.
- B. Une Gateway runtime plus une gouvernance API Management.
- C. Un token JWT suffit.

**Réponse B.** La Gateway protège les appels. La couche Management gouverne les contrats, consommateurs et versions. Le service vérifie **les droits métier**.

## 7 — Adapter / ACL
**Question.** Un legacy retourne \`A01 = reçu pour traitement\`. Que publier côté Java ?
- A. SETTLED.
- B. ACCEPTED_FOR_PROCESSING.
- C. REJECTED.

**Réponse B.** L'ACL traduit **le sens** et évite une fausse confirmation financière.

## 8 — Saga
**Question.** Le virement est réglé, puis la notification échoue. Que compenser ?
- A. Annuler automatiquement le règlement.
- B. Exécuter le virement une seconde fois.
- C. Reprendre uniquement la notification.

**Réponse C.** Un règlement final et irrévocable ne se défait pas par rollback applicatif. Une compensation de réservation est une opération distincte **avant** le pivot.

## 9 — Circuit Breaker
**Question.** Un circuit est OPEN après 12 erreurs techniques sur 20 appels. À quoi sert HALF_OPEN ?
- A. Exécuter tous les appels stockés.
- B. Autoriser un nombre limité de tests et réévaluer la santé.
- C. Annoncer les paiements rejetés.

**Réponse B.** Circuit Breaker ≠ queue. Timeout borne l'attente ; Retry retente parfois ; Bulkhead isole la concurrence.

## 10 — Retry / Timeout / Idempotency
**Question.** Le virement 500 € a été réglé, sa réponse a été perdue. Le canal retente avec \`PAY-001\`.
- A. Créer \`VIR-002\` pour 500 €.
- B. Retrouver le même ordre \`VIR-001\` et réconcilier la preuve.
- C. Considérer la première exécution annulée.

**Réponse B.** La même intention et les mêmes paramètres correspondent au **même ordre**. Le système exécutant doit lui aussi dédupliquer la référence financière.

## Cas transversal d'entretien

Le core bancaire débite 500 €. Le consommateur MQ tombe avant son ACK, le broker redélivre, le deuxième site reçoit la requête après failover et Kafka republie deux fois l'événement.

**Question : combien de débits financiers ?**

**Cible : un seul effet.** Justification attendue :
1. paymentId et référence de débit **stables** à travers toutes les tentatives ;
2. idempotence du core (pas seulement de l'API) ;
3. ownership/fencing avant reprise de la partition ;
4. Inbox pour les effets locaux, Outbox pour les événements ;
5. confirmation financière **réconciliée** avant \`PaymentSettled\` ;
6. aucun retry après deadline sans décision conforme au schéma.

**Le verdict ne peut être considéré prouvé qu'après des tests et un contrat du système autoritatif** ; une simulation de démonstration ne prouve pas la robustesse en production.
