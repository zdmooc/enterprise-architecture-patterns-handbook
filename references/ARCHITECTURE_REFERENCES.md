# Bibliographie de référence — entreprise, application, données et résilience

**Note :** références aux standards, pratiques et documentations publiques. Aucun client, entreprise de projet ou déploiement particulier n'est identifié. Les spécifications, éditions et règles de conformité doivent être vérifiées à leur date d'application.

## Architecture d'entreprise et représentation
- [TOGAF Standard](https://www.opengroup.org/togaf) : méthode d'architecture d'entreprise, état courant/cible et trajectoires.
- [ArchiMate Specification](https://www.opengroup.org/archimate-forum/archimate-overview) : langage de représentation des couches métier, applicatives et technologiques.
- [C4 Model](https://c4model.com/) : context, containers, components, code pour documenter une solution.
- [Architecture Decision Records](https://adr.github.io/) : archivage des décisions d'architecture et de leurs alternatives.

## Architecture applicative, sécurité des APIs et intégration
- [Domain-Driven Design Reference](https://domainlanguage.com/ddd/reference/) : domaines, bounded contexts, agrégats et langage partagé.
- [CNCF Cloud Native Glossary](https://glossary.cncf.io/) : vocabulaire commun sur les applications et services cloud native.
- [Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html) : transaction locale et publication avec redélivrance possible.
- [Idempotent Consumer](https://microservices.io/patterns/communication-style/idempotent-consumer.html) : contrôle des répétitions de messages.
- [OWASP API Security](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) : autorisation objet et autres risques d'API.

## Données
- [OpenLineage Specification](https://openlineage.io/docs/spec/) : représentation des sources, transformations et exécutions.
- [CloudEvents](https://cloudevents.io/) : format commun de métadonnées événementielles ; ne garantit pas exactement un effet métier.

## Kubernetes, résilience et exploitation
- [Kubernetes concepts](https://kubernetes.io/docs/concepts/) : contrôleurs, stockage, networking, security, workloads.
- [Kubernetes disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) : politique d'évictions volontaires, limites des PDB.
- [Kubernetes Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) : contrôleurs de réconciliation.
- [OpenTelemetry](https://opentelemetry.io/docs/) : traces, métriques, logs et propagation de contexte.
- [Site Reliability Engineering book](https://sre.google/sre-book/table-of-contents/) : SLI/SLO, alerting, incidents, capacity planning et error budgets.

## Usage responsable
Ces liens décrivent les **concepts généraux**. Un cahier des charges réel nécessite relevés AS-IS, exigences signées, versions supportées, évaluations de sécurité, tests de charge et de reprise, ainsi que décisions ADR approuvées.
