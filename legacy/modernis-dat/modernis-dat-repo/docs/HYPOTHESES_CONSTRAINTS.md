# Hypothèses & contraintes

## Hypothèses (à confirmer)
- Existence d’un IAM compatible OIDC (ou Keycloak dédié projet).
- Oracle conservé (référentiel finance) avec accès réseau cadré.
- Approche GitOps retenue pour OpenShift (Argo CD / équivalent).
- Segmentation réseau (DMZ / App / Data) avec contrôle egress.

## Contraintes
- Fenêtres de mise en production (horaires / blackout).
- Restrictions d’accès Internet des clusters (proxy / allow-list).
- Politique SSI : chiffrement TLS, secrets, durcissement images, scans.
- Contraintes FinOps : activation des traces selon criticité (budget).
