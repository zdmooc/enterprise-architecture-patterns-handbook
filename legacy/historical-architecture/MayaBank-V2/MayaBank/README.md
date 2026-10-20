# MayaBank

MayaBank est un **dépôt de référence d’architecture, de gouvernance, de lab semi-exécutable et de pilotage FinOps** pour une **banque d’investissement fictive** spécialisée dans les **produits dérivés financiers**.

Le dépôt est construit pour servir quatre usages en parallèle :

1. **apprendre** le socle Kubernetes / OKD et raisonner comme un architecte plateforme ;
2. **structurer** un dossier d’architecture crédible pour un contexte banque / marchés ;
3. **démontrer** une trajectoire vers un niveau **Architecte OpenShift Senior** ;
4. **reprendre le chantier plus tard** sans perdre le fil grâce à une documentation ordonnée.

---

## 1. Ce que MayaBank est, et ce que MayaBank n’est pas

### 1.1 MayaBank est
- un dépôt **documentaire + architecture** ;
- un support de **gouvernance** ;
- un **lab semi-exécutable** ;
- un support de **runbooks** ;
- un cadre de **FinOps avancé** ;
- un support d’**entretien, de comité d’architecture et de démonstration**.

### 1.2 MayaBank n’est pas
- une vraie plateforme de production bancaire ;
- un produit applicatif prêt à déployer tel quel ;
- un simple dépôt YAML sans vision d’architecture ;
- un TP Kubernetes isolé des sujets de sécurité, de coûts et d’exploitation.

---

## 2. Positionnement technique général

### 2.1 Base technique retenue
La base de construction et d’apprentissage est :
- **OKD / Kubernetes open source** ;
- **on-prem + AWS + Azure** ;
- un **niveau B semi-exécutable**, volontairement plus réaliste qu’un pur document, mais moins ambitieux qu’une vraie plateforme d’entreprise.

### 2.2 Cible conceptuelle à maîtriser
La cible de raisonnement, d’entretien et de maturité visée reste :
- **OpenShift enterprise** ;
- gouvernance de plateforme ;
- GitOps ;
- sécurité renforcée ;
- observabilité structurée ;
- workloads stateful ;
- contraintes d’audit, de résilience et de pilotage des coûts.

### 2.3 Pourquoi ce choix
Ce choix permet de :
- rester **100 % open source** sur la base du dépôt ;
- comprendre **le socle réel** sous la plateforme ;
- construire une trajectoire crédible vers une **lecture OpenShift enterprise** ;
- éviter de dépendre trop tôt de composants propriétaires ou trop complexes.

---

## 3. Domaine métier simulé

MayaBank représente une **banque d’investissement** orientée :
- pricing de produits dérivés ;
- trade booking ;
- workflows d’approbation ;
- decisioning / risk scoring ;
- reporting réglementaire ;
- batch de fin de journée ;
- exposition API ;
- portail client institutionnel ;
- analytics, data platform et montée vers data/IA.

---

## 4. Domaines d’architecture couverts

Le dépôt est structuré autour de **cinq domaines majeurs** :

1. **platform**
   - cluster baseline
   - namespaces / quotas / policies
   - ingress / exposition
   - topologie multi-environnements

2. **shared-services**
   - Keycloak
   - Kong
   - Kafka
   - observability
   - patterns secrets / identité / intégration

3. **business workloads**
   - IBM ODM
   - PegaSystems
   - portals
   - batch / CronJobs
   - APIs métiers

4. **data-ai**
   - PostgreSQL
   - MongoDB
   - data pipelines
   - vector database patterns
   - ML serving patterns
   - RAG / retrieval patterns
   - gouvernance Data/IA et coûts associés

5. **governance / operations / FinOps**
   - ADR
   - HLD / LLD
   - runbooks
   - sécurité
   - showback / chargeback
   - capacity planning
   - quality gates

---

## 5. Workloads couverts

### 5.1 Workloads métier et plateforme
- **IBM ODM** pour le decisioning ;
- **PegaSystems** pour le workflow et le case management ;
- **Kafka** pour l’event backbone ;
- **Kong API Gateway** pour l’exposition et la gouvernance API ;
- **observability stack** pour métriques, logs et supervision ;
- **client-portal-web** en mode stateless ;
- **client-portal-session** en mode stateful ;
- **PostgreSQL** pour les données relationnelles ;
- **MongoDB** pour les données orientées document ;
- **Keycloak** pour IAM/SSO ;
- **batch / CronJob** pour les traitements périodiques.

### 5.2 Workloads Data/IA ajoutés à la V1.1 du dépôt
- **data-pipelines** pour ingestion, transformation et enrichissement ;
- **vector-database** pour cas d’usage retrieval / knowledge / similarity search ;
- **ml-serving** pour exposition d’inférence ;
- **rag-patterns** pour recherche augmentée interne ;
- **analytics workers** pour calculs, scoring et génération de vues enrichies.

---

## 6. Pourquoi le domaine Data/IA est dans le même dépôt

Le domaine **Data/IA** n’est pas traité comme un autre dépôt pour trois raisons :

- une banque d’investissement moderne n’isole pas complètement data, IA, intégration, IAM, observabilité et coûts ;
- l’objectif du dépôt est d’apprendre à **raisonner plateforme de bout en bout** ;
- le volet Data/IA modifie profondément les décisions de **capacity planning, observability, stockage, sécurité et FinOps**.

Le domaine Data/IA est donc un **quatrième pilier technique** du dépôt, au même titre que platform, shared-services et business workloads.

---

## 7. Arborescence logique du dépôt

Le dépôt est structuré de manière à pouvoir être lu, enrichi et rejoué progressivement.

### 7.1 Documents principaux
- `docs/vision/` : vision métier et principes d’architecture
- `docs/hld/` : High Level Design
- `docs/lld/` : Low Level Design
- `docs/adr/` : Architecture Decision Records
- `docs/security/` : sécurité, IAM, OIDC, compliance
- `docs/finops/` : cadre FinOps
- `docs/runbooks/` : exploitation
- `docs/governance/` : revue d’architecture, quality gates, risk register
- `docs/roadmap/` : trajectoire produit, plateforme, sécurité et sprints

### 7.2 Partes lab / plateforme
- `lab/` : topologies et exemples rejouables
- `platform/` : structuration logique des services et overlays
- `infra/` : terraform, ansible, scripts
- `gitops/` : Argo CD, Helm, Kustomize
- `cicd/` : Jenkins, quality gates, validation
- `finops/` : modèles, rapports, dashboards
- `evidence/` : preuves, logs, screenshots, smoke tests
- `risks/` : assumptions, debt, issues, RAID log

---

## 8. Ordre de lecture recommandé

Si tu reviens sur le dépôt après une interruption, lis dans cet ordre :

1. `README.md`
2. `docs/vision/Mayabank-Vision.md`
3. `docs/hld/HLD-MayaBank.md`
4. `docs/hld/HLD-Platform.md`
5. `docs/hld/HLD-Data-AI-Platform.md`
6. `docs/hld/HLD-Security.md`
7. `docs/hld/HLD-FinOps.md`
8. `docs/lld/LLD-global.md`
9. `docs/lld/onprem.md`, `docs/lld/aws.md`, `docs/lld/azure.md`
10. `docs/roadmap/Product-Roadmap.md`
11. `docs/roadmap/Sprint-Plan.md`
12. les ADR de cadrage

---

## 9. Ordre de construction recommandé

L’ordre de construction officiel du dépôt est le suivant :

1. README / vision / HLD principal
2. LLD global + providers
3. shared-services
4. workloads métier
5. data & stateful
6. data/IA platform
7. sécurité / IAM / OIDC / secrets
8. GitOps / CI/CD / quality gates
9. FinOps avancé
10. gouvernance / design authority
11. lab semi-exécutable / evidence

---

## 10. Roadmap de maturité

### V1 — socle crédible
- dépôt structuré
- vision et HLD
- LLD global et providers
- premiers workloads
- FinOps et gouvernance fondatrice
- Data/IA cadrée architecturalement

### V2 — industrialisation initiale
- observabilité baseline
- ansible / pipelines documentés
- runbooks enrichis
- quotas / network policies / sécurité de base
- premiers patterns data pipelines et ML serving

### V3 — plateforme avancée
- GitOps
- stateful renforcé
- DR / backup
- showback / chargeback outillés
- vector database patterns et cost controls Data/IA

### V4 — enterprise-ready
- hardening
- conformité
- IAM mature
- audit logging
- mapping complet OKD → OpenShift enterprise
- gouvernance d’architecture consolidée

---

## 11. Ce que le dépôt doit prouver à la fin

À la fin, MayaBank doit démontrer que son auteur sait :
- structurer une plateforme cible cohérente ;
- relier architecture, exploitation et coût ;
- raisonner stateful / stateless / data / IA ;
- intégrer IAM/SSO, observability, API management, eventing ;
- documenter des décisions d’architecture ;
- comparer on-prem, AWS et Azure sans perdre le modèle commun ;
- traduire une base open source vers une cible OpenShift enterprise.

---

## 12. Mode de travail strictement interactif

Le dépôt est conçu pour être construit **sprint par sprint**.

Chaque sprint doit produire :
- un objectif ;
- un périmètre ;
- des livrables visibles ;
- une charge estimative ;
- des critères de validation ;
- une dette restante.

Aucune étape ne doit mélanger :
- ce qui est **documenté** ;
- ce qui est **semi-exécutable** ;
- ce qui est **cible future**.

---

## 13. Où regarder si le chantier s’arrête

Si le projet s’interrompt, la reprise doit repartir de :
- `README.md`
- `docs/roadmap/Sprint-Plan.md`
- `docs/roadmap/Product-Roadmap.md`
- `docs/governance/Decision-Log.md`
- `risks/Open-Issues.md`
- `risks/Technical-Debt.md`

Ces documents doivent toujours être tenus à jour en priorité.

---

## 14. Références internes les plus importantes

- `docs/hld/HLD-MayaBank.md`
- `docs/hld/HLD-Platform.md`
- `docs/hld/HLD-Data-AI-Platform.md`
- `docs/hld/HLD-Security.md`
- `docs/hld/HLD-FinOps.md`
- `docs/lld/LLD-global.md`
- `docs/adr/ADR-0011-okd-to-openshift-enterprise-mapping.md`
- `docs/finops/Capacity-and-Cost-Model.md`
- `docs/security/OIDC-SSO-Model.md`
- `docs/roadmap/Sprint-Plan.md`
