# Patterns Platform Engineering — 5 extensions

Ils complètent les 30 patterns Kubernetes/OpenShift (pods, workloads, réseau, GitOps) par la gouvernance d'une plateforme multi-équipes.

| Fiche | Déclencheur |
|---|---|
| [Control Plane / Data Plane Separation](01-control-plane-data-plane/README.md) | Le plan de gouvernance et la requête métier ont des disponibilités et droits différents. |
| [Golden Path / Paved Road](02-golden-path/README.md) | Chaque équipe recode sécurité, observabilité, pipeline et manifests différemment. |
| [Multi-Tenant Isolation / Noisy Neighbor](03-multi-tenant-isolation/README.md) | Des équipes partagent un cluster et peuvent consommer les ressources ou données des autres. |
| [Policy as Code / Admission Guardrails](04-policy-as-code/README.md) | Des règles d'architecture sont écrites mais ne bloquent aucun déploiement risqué. |
| [Cell-Based Architecture / Fault Containment](05-cell-based-architecture/README.md) | Une plateforme partagée possède un blast radius trop grand. |

## Parcours de revue

Plateforme en tant que produit → Golden Path → politiques automatisées → isolation mesurée → séparation Control/Data Plane → containment par cell si les NFR l'exigent. Les preuves d'admission et d'exécution doivent être distinctes.
