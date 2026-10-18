# Matrice de panne, invariants et plan de tests

## Invariants P0
- INV-01 : pour une intention métier donnée, **au plus une exécution financière autoritative** (preuve au système qui exécute).
- INV-02 : un événement PaymentSettled n'est publié que si une confirmation autoritative est durablement enregistrée.
- INV-03 : un message arrivé après la deadline métier n'est pas aveuglément traité comme neuf.
- INV-04 : si l'issue est incertaine, l'état UNKNOWN/TO_RECONCILE est conservé et tracé, jamais converti sans preuve en REJECTED/SETTLED.
- INV-05 : la notification peut tomber en panne sans annuler ni rejouer l'effet financier.
- INV-06 : une même idempotency-key avec payload divergent est rejetée.

## Plan d'injection de pannes
| ID | Injection | Observation requise | Invariant |
|---|---|---|---|
| F01 | Double POST identique depuis 2 Pods | 1 intention/ordre, même paymentId | 01,06 |
| F02 | Réponse HTTP perdue après commit DB | Retry retourne ordre existant | 01 |
| F03 | Pod crash après commit DB avant MQ | Outbox récupérable | 01,04 |
| F04 | Relais crash après PUT MQ avant marqueur envoyé | Republication possible, 0 double effet | 01 |
| F05 | Consumer MQ crash après effet métier avant ACK | Redélivrance n'exécute pas de deuxième paiement | 01 |
| F06 | MQ indisponible au-delà deadline | Pas de soumission tardive aveugle | 03,04 |
| F07 | Réponse du cœur perdue après règlement | État UNKNOWN puis réconciliation | 04 |
| F08 | Kafka indisponible après SETTLED | Outbox retenue, diffusion ultérieure | 02 |
| F09 | Notifications KO | Etat financier inchangé | 05 |
| F10 | Message PaymentSettled dupliqué | Projection/notification sans double effet indésirable | 02,05 |
| F11 | Event vieux reçu après SETTLED | Pas de régression d'état | 02 |
| F12 | JWT autre client sur paymentId | 403/masquage prévu, aucune fuite | sécurité |
| F13 | Callback legacy nouveau code inconnu | Quarantaine + ticket + rapprochement | 04 |
| F14 | DB primary tombe pendant la TX | Commit déterminé ou ambigu traité par relecture | 01,04 |
| F15 | Circuit Breaker OPEN sur lecture du statut | Fallback « indisponible » non mensonger | 04 |
| F16 | Fin de rétention Kafka avant reprise abonné | Alerte + reconstruction par source autoritative | 02 |

## Mesures / seuils à définir
Le cahier de tests doit renseigner un **SLO chiffré et une méthode de mesure** pour : latence p95/p99 par étape, écart deadline SCT Inst, outbox age, MQ oldest message age, consumer lag, taux de UNKNOWN, âge des ordres TO_RECONCILE, doubles effets détectés, temps de recouvrement, RTO/RPO. Ne pas publier des valeurs fictives comme objectifs contractuels.

## Runbook simplifié TO_RECONCILE
1. Geler les retries pouvant provoquer un nouvel effet financier pour cet identifiant.
2. Vérifier les traces d'émission et le statut chez la source autoritative, avec référence d'origine.
3. Rapprocher confirmations et états persistés ; documenter heure et preuve.
4. Appliquer transition légale/métier autorisée ; publier événement correspondant une seule fois logiquement.
5. En cas de doute persistant, escalader au support paiement habilité sans fabrication d'état.

## Critère de sortie du POC
Toutes les pannes P0 ont une exécution reproductible, un résultat attendu vérifié et une preuve conservée. **Ne pas déclarer « exactly-once end-to-end » sans démonstration sur le système externe d'exécution.**
