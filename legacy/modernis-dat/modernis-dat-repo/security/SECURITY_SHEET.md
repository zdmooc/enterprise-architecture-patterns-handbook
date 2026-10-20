# Fiche sécurité — ModernIS (exemple)

## Classification & données
- Données RH : sensibles (PII) — RGPD
- Données CRM : sensibles
- Données Finance : critiques (intégrité)

## Authentification / Autorisation
- SSO : OIDC (IAM entreprise / Keycloak)
- Autorisation : RBAC OpenShift + rôles applicatifs (groupes)

## Chiffrement
- En transit : TLS (ingress + inter-services si besoin)
- Au repos : chiffrement volumes (selon stockage) + TDE Oracle (si applicable)

## Réseau
- Segmentation : DMZ / App / Data
- Matrice de flux : obligatoire avant MEP (voir `matrices/`)
- Egress : contrôlé (allow-list) + proxy si requis

## Secrets
- Interdiction secrets en clair Git
- Solutions : Vault / SealedSecrets / KMS (selon standard)

## Journalisation / traçabilité
- Logs : centralisés + rétention définie
- Audit : accès admin, changements RBAC, opérations sensibles

## Vulnérabilités / durcissement
- Scans images (CI) + policies admission (ex Kyverno)
- Base images approuvées, patching régulier

## Tests SSI
- Revue configuration + tests d’intrusion cadrés
- Critères Go/NoGo documentés
