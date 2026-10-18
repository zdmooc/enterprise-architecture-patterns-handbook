# Catalogue de travaux pratiques (10 patterns)

Cette liste donne, pour chaque pattern, le banc d'essai minimal et la **preuve** à produire. Les scénarios nécessitant MQ, Kafka ou OpenShift sont des exercices de conception/implantation proposés ; **seul le lab d'idempotence SQLite est implémenté et testé dans cette version.**

| # | Pattern | Exercice | Preuve attendue |
|---|---|---|---|
| 01 | Request/Response | API GET statut + injection de 503 / timeout | Contrat HTTP, p95 et réponse métier non inventée |
| 02 | Messaging / Queue | Stop/start consumer MQ, message persistant | Message conservé et consommé après reprise |
| 03 | Pub/Sub | Un événement, deux groupes abonnés | Deux traitements indépendants, pas d'appel direct |
| 04 | EDA | Machine à états + événement dupliqué/hors ordre | Aucune régression de statut |
| 05 | Event Streaming | Topic partitions par paymentId, replay | Ordre par paiement, mesure du lag et rejeu |
| 06 | API Gateway | JWT faux, scope absent, rate limit | Codes 401/403/429 et audit non sensible |
| 07 | ACL | Mapper codes legacy « accepté » et « réglé » | Tests de mapping et cas inconnu |
| 08 | Saga | Rejet antifraude après réservation | Compensation idempotente et trace du parcours |
| 09 | Circuit Breaker | Seuil erreurs, OPEN → HALF_OPEN → CLOSED | Rejets rapides, métriques transitions |
| 10 | Retry/Timeout/Idempotency | [Lab SQLite exécutable](idempotency/README.md) | 4 tests automatisés, 1 intention/Outbox |

## Conventions
- Tous les identifiants, montants et codes fictifs.
- Les résultats des tests doivent inclure date, environnement, version, commande, état avant/après et conclusion.
- Un exercice Java/OpenShift qui couvre l'exécution bancaire doit se faire contre un **simulateur**, jamais sur un compte ou un système réel.
- Les modes d'échec à couvrir sont détaillés dans [la matrice](../07-case-studies/banking-payments-reference/failure-matrix.md).

## Nouveau laboratoire — architectures IA

- **[RAG ACL + Tool Gateway + validation humaine (Python standard library)](ai-rag-guardrails/README.md)** : démonstrateur local fictif, sans réseau ni LLM, avec tests de confidentialité tenant/rôle, prompt injection comme donnée, outils en lecture seule, approbation immuable et action simulée idempotente.
- Commande : `python -m unittest discover -s labs/ai-rag-guardrails -v` depuis la racine du dépôt.
- Ce laboratoire n'est **pas** un banc de preuve de sécurité en production ; le store de décision et les approvals sont en mémoire.
