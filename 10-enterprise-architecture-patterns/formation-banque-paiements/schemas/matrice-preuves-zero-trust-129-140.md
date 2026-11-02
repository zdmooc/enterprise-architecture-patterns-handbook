# Matrice exigences → preuves — Sécurité Zero Trust 129–140

> Cette matrice est un **plan de preuves à collecter**, pas une déclaration de conformité technique déjà atteinte.

| Cours | Contrôle / décision | Test négatif à réaliser | Preuve requise |
|---:|---|---|---|
| 129 | Zero Trust / Never Trust by Network | Appel interne sans identité valide ou sans droit objet | Logs expurgés + contrat/policy + résultat de test reproductible |
| 130 | PDP / PEP | Bypass de Gateway refusé au service métier | Logs expurgés + contrat/policy + résultat de test reproductible |
| 131 | Defense in Depth | Contournement d'une barrière ne donne pas accès à la donnée | Logs expurgés + contrat/policy + résultat de test reproductible |
| 132 | Identity Federation / OIDC | Jeton pour une autre audience ou expiré refusé | Logs expurgés + contrat/policy + résultat de test reproductible |
| 133 | Workload Identity | ServiceAccount d'un autre workload non autorisé | Logs expurgés + contrat/policy + résultat de test reproductible |
| 134 | RBAC / ABAC / BOLA | Client B ne peut lire l'ordre du client A | Logs expurgés + contrat/policy + résultat de test reproductible |
| 135 | Secret Lifecycle | Secret révoqué refusé après rotation dans la fenêtre spécifiée | Logs expurgés + contrat/policy + résultat de test reproductible |
| 136 | Mutual TLS / PKI | Certificat expiré ou CA inconnue refusé | Logs expurgés + contrat/policy + résultat de test reproductible |
| 137 | Network Micro-Segmentation | Pod reporting ne peut joindre DB paiements | Logs expurgés + contrat/policy + résultat de test reproductible |
| 138 | Encryption at Rest / KMS | Identité non autorisée ne déchiffre pas via KMS | Logs expurgés + contrat/policy + résultat de test reproductible |
| 139 | Software Supply Chain | Image au digest non signé non admise dans OpenShift | Logs expurgés + contrat/policy + résultat de test reproductible |
| 140 | Audit Trail / Segregation of Duties | Demandeur ne peut approuver sa propre correction | Logs expurgés + contrat/policy + résultat de test reproductible |

## Gates d'architecture
- **M0 — Cadrage** : diagramme des actifs, propriétaires, flux, menaces et classification.
- **M1 — Identités** : signatures OIDC, audiences, workload identity, CA et rotation de secrets/certificats.
- **M2 — Application** : autorisation ressource/tenant au service, tests BOLA, refus à défaut et pas de chemin de bypass.
- **M3 — Plateforme** : NetworkPolicy ingress/egress, KMS, coffre, rétention, règles par namespace et droits IAM minimaux.
- **M4 — Supply chain** : une image unique identifiée par digest, SBOM, signatures, provenance et admission Kyverno.
- **M5 — Audit** : séparation demande/approuve/exécute, traçabilité et test de tentative de suppression d'une preuve.
- **M6 — Résilience** : indisponibilité de la sécurité, expirations, révocations et objectifs SLO testés.

## Niveaux de qualification
1. **Documenté** : contrat et risque identifiés.
2. **Simulé** : tests en CI ou dans un laboratoire isolé.
3. **Démontré** : preuve runtime vérifiée, commit, configuration et versions des contrôles consignés.
4. **Accepté** : propriétaire métier/sécurité valide la politique et le risque résiduel.

Ne pas déclarer un gate validé simplement parce qu'une fiche de cours ou un manifeste YAML existe.

[Programme 129–140](../README.md) · [Architecture de synthèse](zero-trust-129-140.md)
