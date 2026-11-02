# Matrice finale de qualification — 40 cours 186 à 225

> **Plan documentaire de preuves, non exécution de tests**. Les lignes décrivent les expériences à réaliser avant toute acceptation Design Authority.

| Cours | Catégorie | Pattern | Invariant de contrôle | Preuve à collecter |
|---:|---|---|---|---|
| 186 | Cloud hybride / Multicloud | [Landing Zone](../186-landing-zone.md) | Gouvernance IAM/réseau/audit avant workload | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 187 | Cloud hybride / Multicloud | [Hub-and-Spoke](../187-hub-spoke.md) | Flux interspokes autorisés et centralisés | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 188 | Cloud hybride / Multicloud | [Transit Connectivity](../188-transit-connectivity.md) | Routage hybride sans fuite et sans conflit CIDR | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 189 | Cloud hybride / Multicloud | [Private Connectivity](../189-private-connectivity.md) | Aucun fallback public implicite pour données sensibles | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 190 | Cloud hybride / Multicloud | [Multi-Account Governance](../190-multi-account-governance.md) | Projets séparés avec policies communs | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 191 | Cloud hybride / Multicloud | [Multi-Region Strategy](../191-multi-region-strategy.md) | Un seul writer par clé lors de bascule | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 192 | Cloud hybride / Multicloud | [Hybrid Workload Placement](../192-hybrid-workload-placement.md) | Placement guidé par résidence, latence, SLA et coût | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 193 | Cloud hybride / Multicloud | [Cloud Bursting](../193-cloud-bursting.md) | Bursting seulement pour workload et données autorisés | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 194 | Cloud hybride / Multicloud | [Infrastructure as Code](../194-infrastructure-as-code.md) | Plan/review/drift et secrets protégés | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 195 | Cloud hybride / Multicloud | [Cloud Exit & Portability](../195-cloud-exit-portability.md) | Restitution des données et redéploiement vérifiable | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 196 | Performance / SRE | [Caching Patterns](../196-caching-patterns.md) | Cache sous droits et fraîcheur, non source financière | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 197 | Performance / SRE | [Load Balancing](../197-load-balancing.md) | Balancer uniquement les pods Ready | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 198 | Performance / SRE | [Sharding](../198-sharding.md) | Un owner autoritatif par paymentId | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 199 | Performance / SRE | [Connection Pooling](../199-connection-pooling.md) | Connexions bornées selon capacité aval | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 200 | Performance / SRE | [Async Offload](../200-async-offload.md) | Tâches différées suivies durablement | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 201 | Performance / SRE | [Rate Limiting](../201-rate-limiting.md) | Refus avant effet et quotas cohérents | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 202 | Performance / SRE | [Latency Budget](../202-latency-budget.md) | Budget end-to-end et deadline métier | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 203 | Performance / SRE | [Golden Signals](../203-golden-signals.md) | Latence, trafic, erreurs et saturation visibles | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 204 | Performance / SRE | [SLI / SLO / Error Budget](../204-sli-slo-error-budget.md) | SLO basé sur expérience et exactitude métier | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 205 | Performance / SRE | [Capacity Planning](../205-capacity-planning.md) | Dimensionnement incluant aval, mémoire et MQ | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 206 | Modernisation Legacy | [Rehost](../206-rehost.md) | Runtime et contrats identiques ou écarts expliqués | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 207 | Modernisation Legacy | [Replatform](../207-replatform.md) | Compatibilité EJB/JTA/JMS et support éditeur qualifiés | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 208 | Modernisation Legacy | [Refactor](../208-refactor.md) | Règles métier et effets inchangés | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 209 | Modernisation Legacy | [Replace](../209-replace.md) | Historique et contrats repris sans perte | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 210 | Modernisation Legacy | [Retire](../210-retire.md) | Zéro consommateur actif et rétention préservée | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 211 | Modernisation Legacy | [Retain](../211-retain.md) | Legacy conservé sous contrôle et roadmap | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 212 | Modernisation Legacy | [Strangler Fig Migration](../212-strangler-fig-migration.md) | Un seul exécuteur autoritatif à la fois | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 213 | Modernisation Legacy | [Parallel Run / Shadow](../213-parallel-run-shadow.md) | Shadow sans effet métier externe | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 214 | Modernisation Legacy | [Expand–Contract Database](../214-expand-contract-db.md) | Coexistence versions API et schémas | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 215 | Modernisation Legacy | [Cutover / Rollback](../215-cutover-rollback.md) | Bascule exclusive et rapprochement financier | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 216 | Platform Engineering | [Control Plane / Data Plane Separation](../216-control-plane-data-plane.md) | Panne du contrôle sans nouveau privilège data plane | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 217 | Platform Engineering | [Golden Path / Paved Road](../217-golden-path.md) | Template non-root, SBOM, probes et admission | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 218 | Platform Engineering | [Multi-Tenant Isolation / Noisy Neighbor](../218-multi-tenant-isolation.md) | Secret et quotas de A isolés de B | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 219 | Platform Engineering | [Policy as Code / Admission Guardrails](../219-policy-as-code.md) | CI et admission appliquent policy versionnée | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 220 | Platform Engineering | [Cell-Based Architecture / Fault Containment](../220-cell-based-architecture.md) | Panne cell A n'affecte pas B et pas de double writer | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 221 | Architecture décisionnelle / ODM | [Decision Service Boundary](../221-decision-service-boundary.md) | Contrat versionné et provenance décisionnelle | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 222 | Architecture décisionnelle / ODM | [Rule Engine Adapter](../222-rule-engine-adapter.md) | Domaine découplé du moteur / éditeur | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 223 | Architecture décisionnelle / ODM | [Rule Version Pinning / Promotion](../223-rule-version-pinning.md) | Version hash règles, moteur et input retraçables | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 224 | Architecture décisionnelle / ODM | [Shadow Decision Evaluation](../224-shadow-decision-evaluation.md) | Moteur shadow sans effet ni décision effective | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |
| 225 | Architecture décisionnelle / ODM | [Decision Audit & Human Review](../225-decision-audit-human-review.md) | Audit et approbation sur payload/version exacts | Cas positif/négatif, configuration versionnée, mesure et sortie horodatée |

## Gates d'acceptation multi-domaines
- **G0 — Cadrage** : patrimoine applicatif, statut métier, ownership, menaces et dépendances.
- **G1 — Architecture** : HLD, LLD, modèles de données, API/AsyncAPI, flux, IAM et choix ADR.
- **G2 — Sécurité** : accès objets, réseau, secrets, conformité et anti-contournement, avec tests négatifs.
- **G3 — Exploitabilité** : SLI/SLO, coûts, métriques, alertes, processus d'astreinte et plan de restauration.
- **G4 — Résilience** : timeout, réponse perdue, duplication, rollback, RPO/RTO et absence de double writer.
- **G5 — Compatibilité** : tests Java/JEE, JMS/JTA/XA, contrats legacy, schémas DB et déploiements sans double effet.
- **G6 — Décision** : version de règles, raison de la décision, shadow sans effet, approbation et audit.
- **G7 — Production readiness** : preuves réelles, licence/support éditeur, responsable et GO/NO-GO signé.

## Classification honnête des résultats
- **Documenté** : scénario et test écrits.
- **Simulé** : test avec jeu fictif dans un environnement isolé.
- **Démontré** : exécution enregistrée avec versions et preuve runtime.
- **Accepté** : revue par les responsables compétents et risques résiduels arbitrés.

L'achèvement de la formation **n'est pas** une certification OpenShift, IBM ODM ou preuve d'exploitation de banque.

[Retour aux 225 cours](../README.md)
