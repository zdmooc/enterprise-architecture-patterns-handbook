# ADR — Arbitrages d'architecture (propositions, non décisions CAPS)

## ADR-001 — L'API crée une intention durable
- **Contexte** : le client peut subir un timeout après requête de paiement.
- **Décision candidate** : identifier l'intention par une idempotency-key scoped et enregistrer ordre+Outbox atomiquement.
- **Conséquences** : DB transactionnelle critique ; unicité concurrente ; réponse GET fiable.
- **Alternatives** : transactions coordonnées/plateforme existante avec garantie équivalente.
- **Test décisif** : 2 POST simultanés = 1 ordre.

## ADR-002 — MQ transporte les commandes vers le legacy
- **Contexte** : système bancaire historique et dépendances temporelles.
- **Décision candidate** : IBM MQ persistent/syncpoint, corrélation, BOQ/DLQ correctement gérées.
- **Conséquences** : gestion d'échéance métier et redélivrance nécessaire.
- **Alternative** : API synchrone, autre broker ou bus d'entreprise selon le SI réel.
- **Test** : arrêt consommateur puis reprise sans nouveau paiement.

## ADR-003 — Kafka diffuse les faits métier
- **Contexte** : notification, reporting, observabilité et analytics souhaitent les résultats.
- **Décision candidate** : topics versionnés et groupes indépendants ; Outbox après changement d'état confirmé.
- **Conséquences** : rétention, schéma, partitions/offsets, lag et PII à gouverner.
- **Alternative** : MQ Pub/Sub, intégration applicative existante.
- **Test** : notification down sans blocage du règlement.

## ADR-004 — Saga orchestrée
- **Contexte** : contrôles, réservation, soumission, compensation et réconciliation.
- **Décision candidate** : état de Saga durable et transitions protégées.
- **Conséquences** : composant orchestration à rendre HA, débogage et observabilité.
- **Alternative** : chorégraphie si parcours simple et ownership des réactions maîtrisé.
- **Test** : arrêt de l'orchestrateur entre réservation et refus.

## ADR-005 — Source financière autoritative hors plateforme
- **Contexte** : prévention des vues contradictoires de règlement.
- **Décision candidate** : l'état SETTLED doit être confirmé par le cœur/rail autoritatif.
- **Conséquences** : état UNKNOWN et rapprochement obligatoire.
- **Test** : exécution réelle + réponse perdue.

## ADR-006 — Stratégie résilience
- **Contexte** : pannes de dépendances et risque de tempête de Retry.
- **Décision candidate** : timeout explicite, backoff/jitter borné, Circuit Breaker et Bulkhead par dépendance, aucune soumission après échéance sans contrôle.
- **Conséquences** : erreurs techniques distinctes des rejets métier, SLO commun.
- **Test** : service amont 503 puis retour sans double exécution.

## Modèle de validation Design Authority
Chaque ADR doit inclure : sponsor métier, owner technique, options chiffrées, coût/licences, exigences réglementaires vérifiées, contraintes non fonctionnelles, risques résiduels, décisions de sécurité/production, preuves d'essais et date d'approbation.
