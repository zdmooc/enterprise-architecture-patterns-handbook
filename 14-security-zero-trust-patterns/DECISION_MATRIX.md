# Matrice de décision — Sécurité

Question concrète → fiche nommée correctement → preuve minimale.

| Besoin | Pattern | Gate d'acceptation |
|---|---|---|
| Contrôler chaque demande sans confiance réseau implicite | [zero trust](01-zero-trust/README.md) | Test d'incident et contrôle négatif |
| Distinguer moteur de politique et point de refus | [policy decision enforcement](02-policy-decision-enforcement/README.md) | Test d'incident et contrôle négatif |
| Superposer contrôles indépendants | [defense in depth](03-defense-in-depth/README.md) | Test d'incident et contrôle négatif |
| Accepter identités entre domaines de confiance | [identity federation](04-identity-federation/README.md) | Test d'incident et contrôle négatif |
| Authentifier les workloads sans secrets fixes | [workload identity](05-workload-identity/README.md) | Test d'incident et contrôle négatif |
| Autoriser chaque objet par rôle et attribut | [rbac abac](06-rbac-abac/README.md) | Test d'incident et contrôle négatif |
| Gérer création, rotation, révocation des secrets | [secret lifecycle](07-secret-lifecycle/README.md) | Test d'incident et contrôle négatif |
| Authentifier les deux côtés du canal TLS | [mutual tls pki](08-mutual-tls-pki/README.md) | Test d'incident et contrôle négatif |
| Bloquer est-ouest sauf flux autorisés | [network microsegmentation](09-network-microsegmentation/README.md) | Test d'incident et contrôle négatif |
| Isoler clés, cycles de vie et politiques | [encryption key management](10-encryption-key-management/README.md) | Test d'incident et contrôle négatif |
| Vérifier SBOM, signatures et provenance | [software supply chain](11-software-supply-chain/README.md) | Test d'incident et contrôle négatif |
| Séparer approbation, déploiement et audit | [audit segregation duties](12-audit-segregation-duties/README.md) | Test d'incident et contrôle négatif |

## Gouvernance

Énoncer le risque, son propriétaire, l'alternative simple, les NFR, les coûts et l'effet d'une panne. Une politique déclarée n'est pas une preuve de son enforcement en runtime. Chaque dossier de décision doit préciser le périmètre testé et le risque résiduel.

[Retour](README.md) · [Guide](../references/GUIDE_ARCHITECTE_151_PATTERNS.md)
