# Threat model (très synthétique)

## Menaces principales
- Accès non autorisé (authn/authz)
- Exfiltration via egress non contrôlé
- Fuite de secrets (CI/CD, manifests)
- Déni de service (API gateway, quotas)
- Compromission image (supply chain)

## Mesures
- OIDC + RBAC + least privilege
- NetworkPolicies + egress control
- Secrets via Vault/SealedSecrets
- Rate limit / quotas / WAF
- Scans + signature + policies admission
