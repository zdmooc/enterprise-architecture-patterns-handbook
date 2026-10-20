# Dossier d’Architecture Technique (DAT)
## ModernIS — Modernisation du SI Interne Entreprises

- **Architecte** : Zidane Djamal  
- **Version** : 1.0  
- **Date** : 2025-12-18  
- **Statut** : Draft (fictif, prêt comité)  

---

## 0. Synthèse exécutive
### 0.1 Résumé
Le projet **ModernIS** vise à moderniser le **SI Interne** du domaine Entreprises en :
- migrant des applications Java (portail RH, CRM interne, ERP Finance) vers une plateforme **Red Hat OpenShift** ;
- mettant en place un **socle d’API Management** (publication, sécurité, gouvernance) ;
- renforçant la **sécurité des flux** (matrice DMZ/App/Data, chiffrement, RBAC, traçabilité) ;
- industrialisant l’exploitation (supervision, alerting, RUN, DRP/DRCP).

### 0.2 Décisions clés (extrait)
Voir `adr/` pour le détail.
- Plateforme d’exécution : **OpenShift 4.x** (clusters HA, segmentation par environnements/namespace).
- Exposition des services : **API Gateway / API Management** (policies, auth, quotas, observabilité).
- IAM/SSO : **OIDC** (Keycloak ou IAM entreprise) + RBAC + groupes.
- Données : **Oracle** (existante) + **S3** (stockage objet : documents/exports).
- Observabilité : métriques + logs + traces (selon contraintes coût).

### 0.3 Périmètre
- Applications : Portail RH, CRM Interne, ERP Finance (interfaces REST).
- Infrastructures : DMZ / Zone Applicative / Zone Data.
- Transverse : API Management, SSO, sécurité, DRP/DRCP, RUN.

### 0.4 Hors périmètre (à adapter)
- Réécriture fonctionnelle des applications.
- Remplacement de l’ERP Finance.
- Refonte de la gouvernance IAM globale entreprise.

---

## 1. Contexte, enjeux, objectifs
### 1.1 Contexte
Le SI interne historique repose sur des serveurs applicatifs Java (Apache/JBoss), déploiements manuels, et des flux partiellement documentés. Les délais de mise en production et la conformité SSI sont devenus des points de friction.

### 1.2 Enjeux métier & IT
- Réduire le cycle de delivery (industrialisation CI/CD + GitOps).
- Sécuriser et tracer les flux inter-SI (matrice de flux, politiques, logs).
- Améliorer la résilience (HA, DRP/DRCP, bascule maîtrisée).
- Améliorer la capacité d’évolution (scalabilité horizontale).

### 1.3 Objectifs mesurables (exemples)
- **Disponibilité** : 99,9% mensuel sur les services critiques.
- **MTTR** : < 60 min sur incidents P1 (RUN + runbooks).
- **Conformité** : 100% des flux documentés et validés sécurité avant mise en prod.
- **Lead time** : réduction de 30% sur 2 releases consécutives (mesuré).

---

## 2. Parties prenantes & gouvernance
Voir `docs/STAKEHOLDERS_RACI.md` et `governance/`.
- Comités : Comité Architecture, Comité Sécurité, CAB / Mise en production.
- Instances RUN : cellules de crise, post-mortems (RCA).

---

## 3. Exigences (NFR) & contraintes
### 3.1 Catalogue NFR
Voir `nfr/NFR_CATALOG.md`.

### 3.2 Hypothèses et contraintes
Voir `docs/HYPOTHESES_CONSTRAINTS.md`.
- Contraintes sécurité : segmentation réseau, egress contrôlé, chiffrement TLS.
- Contraintes exploitation : fenêtres de déploiement, procédures de rollback, supervision.
- Contraintes coûts : traces activées selon criticité (à cadrer).

---

## 4. Architecture existante (AS-IS)
### 4.1 Cartographie applicative (AS-IS)
- Portail RH : appli web + services Java.
- CRM interne : services Java EE.
- ERP Finance : interfaces + batchs.
- Échanges : REST, JDBC, transferts fichiers (à rationaliser).

### 4.2 Pain points
- Déploiements hétérogènes et manuels.
- Manque de visibilité (metrics/traces/logs incomplets).
- Flux parfois non alignés SSI (ports/protocoles non justifiés).

---

## 5. Architecture cible (TO-BE)
### 5.1 Vue d’ensemble
- **OpenShift** : cluster HA, nodes workers, multi-namespace par environnement.
- **Socle API Management** : gateway + portail développeur + policies.
- **SSO** : OIDC + RBAC (groupes) + gestion des secrets.
- **Data** : Oracle + S3 (stockage objet) + mécanismes de backup/restore.

### 5.2 Vues ArchiMate attendues
Références : `docs/ARCHIMATE_GUIDE.md` + diagrammes `diagrams/`.
- Motivation : drivers, exigences, objectifs.
- Métier : processus RH/CRM/Finance (haut niveau).
- Applicative : composants, interfaces, contrats.
- Technologique : nodes, réseau, plateformes, zones.

### 5.3 Diagrammes
- Vue contexte : `diagrams/context.mmd`
- Vue applicative : `diagrams/application.mmd`
- Vue déploiement : `diagrams/deployment.mmd`
- Vue réseau/zones : `diagrams/network-zones.mmd`
- DRP/DRCP : `diagrams/drp.mmd`

---

## 6. Sécurité & réseau
### 6.1 Fiche sécurité
Voir `security/SECURITY_SHEET.md`.

### 6.2 Matrice de flux (référence)
Voir `matrices/flow-matrix.csv` et `matrices/flow-matrix.md`.
- Source/Destination, zone, protocole, port, authn/authz, chiffrement, justification, owner.

### 6.3 Contrôles techniques (exemples)
- RBAC OpenShift : rôles minimalistes, service accounts dédiés.
- NetworkPolicies : default-deny + allow-lists.
- Egress control : proxy/egress gateway selon contexte.
- Secrets : intégration Vault / SealedSecrets / KMS (selon politique).

---

## 7. Dimensionnement & performance
### 7.1 Méthode de dimensionnement (à présenter)
- Baseline production (CPU/RAM, RPS, batch windows, connexions DB).
- Marges : pics, croissance, incident (N+1), maintenance.
- Objectifs : P95, throughput, saturation, file d’attente.
Voir `nfr/CAPACITY_MODEL.md` et `nfr/PERFORMANCE_TEST_PLAN.md`.

### 7.2 Plages recommandées (exemple)
- **Nominal** : 30–60 vCPU / 120–240 Go (zone app) — à affiner par mesures
- **Pic** : +50% (autoscaling) + réserves cluster
- **Stockage objet** : 5–15 To selon rétention et volumétrie documentaire

---

## 8. Exploitation, RUN, DRP/DRCP
### 8.1 Exploitation
Voir `runbooks/`.
- Monitoring/alerting : SLO/SLI (`nfr/SLO_SLI.md`)
- Procédures : incident, rollback, escalade, post-mortem (RCA).

### 8.2 DRP/DRCP
- Objectifs : RTO/RPO et scénarios de bascule.
- Tests : exercices planifiés + preuves.
Voir `runbooks/RUNBOOK_DRP_TEST.md` + `diagrams/drp.mmd`.

---

## 9. Plan de mise en œuvre & accompagnement projets
### 9.1 Phasage
- Vague 0 : cadrage + socles (API Mgmt, IAM, obs)
- Vague 1 : appli pilote (RH)
- Vague 2 : CRM + interfaces ERP
- Vague 3 : généralisation + durcissement + DRP

### 9.2 Livrables par jalon
- DAT mis à jour + ADR
- Matrice de flux validée SSI
- NFR + plan de tests (perf, sécurité)
- Dossiers de MEP : plan bascule + retour arrière + runbooks

---

## 10. Conformité, audit prod, ajustements
Voir `security/COMPLIANCE_CHECKLIST.md` et `governance/PROD_ARCH_REVIEW.md`.
- Revue d’implémentation vs DAT.
- Écarts, décisions, remédiations.
- Boucle d’amélioration continue.

---

## Annexes
- Glossaire : `docs/GLOSSARY.md`
- Risques : `docs/RISKS.md`
- Templates : `governance/` + `adr/000-template.md`
