# Lab — Idempotence d'une intention de paiement (Python + SQLite)

Ce laboratoire **ne réalise aucun virement**. Il illustre la protection côté API : unicité d'une intention par (clientId, idempotencyKey), empreinte de payload, écriture atomique de l'intention et de son événement Outbox. SQLite est choisi pour ne nécessiter aucun serveur. **Ce n'est pas un modèle complet de règlement bancaire ni une équivalence à PostgreSQL en production**.

## Prérequis
Python 3.10+ (bibliothèque standard), dans la racine du dépôt.

~~~bash
python labs/idempotency/payment_demo.py
python -m unittest discover -s labs/idempotency -v
~~~

## Ce que prouvent les 4 tests
1. Deux requêtes identiques produisent un seul paymentId et un seul enregistrement Outbox.
2. Même clé, montant modifié : conflit explicite, pas de modification de l'ordre existant.
3. Une même clé peut appartenir à deux clients distincts (scope).
4. Douze appels concurrents sur plusieurs connexions SQLite : un seul ordre et un seul événement.

## Limites pédagogiques
- Unicité **au niveau de l'intention API**, pas la garantie d'absence de double effet au cœur financier.
- Aucun transport MQ, CDC, broker Kafka ni job de publication.
- Pas d'authentification réelle, de validation de bénéficiaire, de deadline SCT Inst ou de conservation réglementaire.
- La base de production devrait avoir HA, sauvegardes, contrôles de sécurité, suivi du cycle de vie et une implémentation de déduplication autoritative à l'exécution.

## Exercices complémentaires
- Arrêter le programme entre la transaction DB et la publication externe, puis vérifier que l'événement Outbox attend toujours.
- Simuler un relais qui publie un événement deux fois : écrire un Idempotent Consumer.
- Ajouter à chaque paiement une deadline et refuser toute soumission irréversible une fois expirée, conformément aux règles métier applicables.
- Ajouter une machine à états versionnée (aucun retour SETTLED → PROCESSING).

Voir [pattern 10](../../01-integration-patterns/10-retry-timeout-idempotency/README.md).
