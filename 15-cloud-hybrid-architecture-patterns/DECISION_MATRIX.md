# Matrice de décision — Cloud hybride

Question concrète → fiche nommée correctement → preuve minimale.

| Besoin | Pattern | Gate d'acceptation |
|---|---|---|
| Bâtir environnement cloud contrôlé | [landing zone](01-landing-zone/README.md) | Test d'incident et contrôle négatif |
| Séparer sous-réseaux autour d'un point de transit | [hub spoke](02-hub-spoke/README.md) | Test d'incident et contrôle négatif |
| Relier domaines réseaux sous contrôle | [transit connectivity](03-transit-connectivity/README.md) | Test d'incident et contrôle négatif |
| Isoler échanges réseau sensibles | [private connectivity](04-private-connectivity/README.md) | Test d'incident et contrôle négatif |
| Limiter blast radius entre comptes | [multi account governance](05-multi-account-governance/README.md) | Test d'incident et contrôle négatif |
| Définir placement selon résidence et PRA | [multi region strategy](06-multi-region-strategy/README.md) | Test d'incident et contrôle négatif |
| Arbitrer proximité des données et latence | [hybrid workload placement](07-hybrid-workload-placement/README.md) | Test d'incident et contrôle négatif |
| Consommer capacité élastique temporaire | [cloud bursting](08-cloud-bursting/README.md) | Test d'incident et contrôle négatif |
| Versionner créations et changements d'infra | [infrastructure as code](09-infrastructure-as-code/README.md) | Test d'incident et contrôle négatif |
| Tester sortie fournisseur et portabilité | [cloud exit portability](10-cloud-exit-portability/README.md) | Test d'incident et contrôle négatif |

## Gouvernance

Énoncer le risque, son propriétaire, l'alternative simple, les NFR, les coûts et l'effet d'une panne. Une politique déclarée n'est pas une preuve de son enforcement en runtime. Chaque dossier de décision doit préciser le périmètre testé et le risque résiduel.

[Retour](README.md) · [Guide](../references/GUIDE_ARCHITECTE_151_PATTERNS.md)
