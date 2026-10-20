# Matrice de décision — Architecture d'entreprise

**Version corrigée :** chaque besoin renvoie au pattern portant réellement ce nom. Aucun résultat d'un POC n'est implicitement validé.

| Besoin réel | Pattern | Preuve à fournir |
|---|---|---|
| Aligner applications et capacités métier | [business capability mapping](01-business-capability-mapping/README.md) | Contrat, cas négatif, test de panne, ADR |
| Réduire les délais et ruptures du parcours métier | [value stream mapping](02-value-stream-mapping/README.md) | Contrat, cas négatif, test de panne, ADR |
| Délimiter responsabilités entre domaines | [business domain architecture](03-business-domain-architecture/README.md) | Contrat, cas négatif, test de panne, ADR |
| Visualiser applications et interdépendances | [application landscape](04-application-landscape/README.md) | Contrat, cas négatif, test de panne, ADR |
| Tracer échanges et dépendances inter-SI | [enterprise flow mapping](05-enterprise-flow-mapping/README.md) | Contrat, cas négatif, test de panne, ADR |
| Décider conserver, refondre ou retirer | [application portfolio rationalization](06-application-portfolio-rationalization/README.md) | Contrat, cas négatif, test de panne, ADR |
| Formaliser architecture cible et NFR | [target architecture blueprint](07-target-architecture-blueprint/README.md) | Contrat, cas négatif, test de panne, ADR |
| Concevoir états de transition exploitables | [transition architecture](08-transition-architecture/README.md) | Contrat, cas négatif, test de panne, ADR |
| Planifier les vagues et risques | [transformation roadmap](09-transformation-roadmap/README.md) | Contrat, cas négatif, test de panne, ADR |
| Mutualiser briques contractuelles | [architecture building blocks](10-architecture-building-blocks/README.md) | Contrat, cas négatif, test de panne, ADR |
| Documenter décisions et dérogations | [architecture governance adr](11-architecture-governance-adr/README.md) | Contrat, cas négatif, test de panne, ADR |
| Tester conformité cible aux exigences | [architecture compliance nfr](12-architecture-compliance-nfr/README.md) | Contrat, cas négatif, test de panne, ADR |

## Méthode

1. Définir contexte métier, propriétaire de données, NFR et contraintes de licences.
2. Comparer le minimum viable avec l'option utilisant ce pattern, risques et coûts inclus.
3. Tester nominal + anomalie + reprise ; expliciter ce qui n'est pas prouvé.
4. Formaliser décision, responsable, date de revue et conditions de retour arrière.

[Sommaire famille](README.md) · [Guide de sélection](../references/GUIDE_ARCHITECTE_151_PATTERNS.md)
