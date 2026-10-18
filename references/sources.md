# Références publiques et méthode de vérification

**Date de vérification documentaire : 18 octobre 2026.** Sources sélectionnées pour comprendre les patterns ; elles ne prouvent rien sur l'architecture interne d'un client.

## Schéma SEPA et règles financières
- [European Payments Council — SCT Inst Rulebook (page officielle)](https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-schemes/sepa-instant-credit-transfer-sct-inst/sepa-instant-credit-transfer). En octobre 2026 : 2025 Rulebook v1.2, publication 30/09/2026 ; exigences de délai, restauration et notification.
- [EPC — Customer-to-PSP SCT Inst Implementation Guidelines](https://www.europeanpaymentscouncil.eu/document-library/implementation-guidelines/sepa-instant-credit-transfer-customer-psp-2).

## Messaging, streaming et intégration
- Pour la persistance MQ, les unités de travail, les files de quarantaine et les canaux, utiliser la documentation officielle du **middleware choisi**, à versionner lors du cadrage d'architecture.
- [Apache Kafka — Partitioning](https://kafka.apache.org/40/design/protocol/).
- [Apache Kafka — Consumer offset tracking](https://kafka.apache.org/40/implementation/distribution/).

## Patterns de conception et sécurité
- Référence conceptuelle : Anti-Corruption Layer (DDD).
- [microservices.io — Saga](https://microservices.io/patterns/data/saga.html).
- [microservices.io — Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html).
- [microservices.io — Idempotent Consumer](https://microservices.io/patterns/communication-style/idempotent-consumer.html).
- [Resilience4j — Circuit Breaker](https://resilience4j.readme.io/docs/circuitbreaker).
- [OpenID Foundation — OIDC Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html).
- [OWASP — API Security Top 10](https://api-security.owasp.org/editions/2023/en/0x11-t10/).

## Limites
- Des pages en ligne peuvent évoluer ; figer la version d'une spécification dans chaque dossier d'architecture client.
- Les valeurs de timeout, quotas, backoff, coûts, topologie HA, responsabilités légales et technologies effectives sont **des paramètres à mesurer et approuver**, non des postulats.
- Aucun extrait confidentiel d'un cahier des charges client ni schéma interne non public n'est publié. Les scénarios sont pédagogiques.
