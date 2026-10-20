# Gestion des secrets (approche)

## Principes
- Aucun secret en clair dans Git.
- Séparer données sensibles (secrets) des configs non sensibles (ConfigMaps).
- Rotation et révocation documentées.

## Options
1) Vault (recommandé si standard entreprise)
2) SealedSecrets (GitOps-friendly)
3) External Secrets Operator + KMS

## Exemples
Voir `k8s/security/`.
