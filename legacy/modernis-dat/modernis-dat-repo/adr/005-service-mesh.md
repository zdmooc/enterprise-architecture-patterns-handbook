# ADR-005 — Service Mesh (Istio / OCP Service Mesh)
- **Statut** : Proposed
- **Date** : 2025-12-18
- **Contexte** : Besoin potentiel de mTLS, retries, traffic shaping, observabilité L7.
- **Décision** : Déployer un mesh uniquement si les exigences mTLS/observabilité L7 le justifient (sinon complexité inutile).
- **Conséquences** : Réduction complexité par défaut ; activation au besoin.
