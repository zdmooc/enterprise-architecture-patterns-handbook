# Structure du dépôt

Ce dépôt contient un **Dossier d’Architecture Technique (DAT)** complet (fictif mais réaliste) aligné sur la mission :
- Conception et architecture
- Accompagnement des projets (NFR, fiches sécurité, matrices de flux, bascules)
- Suivi / conformité / RUN (audit prod, cellule de crise, DRP/DRCP)
- Contribution transverse (cahiers des charges, appels d’offres, gouvernance)

Le cœur du livrable est : `docs/DAT.md`.


## Dossiers principaux
- `docs/` : DAT + annexes (RACI, hypothèses, risques, etc.)
- `diagrams/` : diagrammes Mermaid (texte) + export éventuel
- `matrices/` : matrices de flux (CSV + Markdown)
- `security/` : fiche sécurité, checklist conformité SSI, threat model
- `nfr/` : catalogue NFR, SLO/SLI, plan de test perf, capacité
- `adr/` : décisions d’architecture (traceabilité et arbitrages)
- `runbooks/` : procédures RUN / crise / DRP / rollback
- `rfp/` : cahiers des charges / gabarits d’appel d’offres
- `k8s/` : exemples manifests OpenShift (quotas, policies, GitOps)
- `governance/` : gabarits comités, CR, checklists de validation
- `evidence/` : preuves (captures, outputs, logs) — vide par défaut
- `scripts/` : scripts utilitaires (validation, export, build PDF)
