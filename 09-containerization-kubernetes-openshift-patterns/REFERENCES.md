# Références techniques — conteneurisation, Kubernetes et OpenShift

**Noms de technologies et standards uniquement.** Les références officielles ne prouvent ni que l'utilisateur ni qu'un établissement emploie une technologie précise. Fixer les versions Kubernetes/OpenShift et produit sur chaque dossier cible.

## Conteneurs OCI et compilation
- [OCI Image Specification](https://github.com/opencontainers/image-spec) : couches, manifests, digests.
- [Docker — Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/) : compilation séparée du runtime.
- [Kubernetes — Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/).

## Pods, contrôleurs et persistance
- [Kubernetes — Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/).
- [Kubernetes — Sidecar Containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/) : sidecars natifs via \`initContainers\` avec \`restartPolicy: Always\` dans les versions compatibles.
- [Kubernetes — Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
- [Kubernetes — StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).
- [Kubernetes — Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/).
- [Kubernetes — CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).
- [Kubernetes — Operator Pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

## Résilience, réseau et scale
- [Kubernetes — Liveness, Readiness, Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/).
- [Kubernetes — Pod Termination](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination).
- [Kubernetes — Pod Disruption Budgets](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/).
- [Kubernetes — Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
- [Kubernetes — Pod Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/).
- [Kubernetes — Service](https://kubernetes.io/docs/concepts/services-networking/service/).
- [Kubernetes — Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
- [Kubernetes — Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/).

## OpenShift / delivery
- [OpenShift Container Platform — Documentation](https://docs.redhat.com/en/documentation/openshift_container_platform).
- [OpenShift — SCC et politique restricted-v2 (documentation versionnée)](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/managing-pod-security-policies).
- [OpenShift GitOps — documentation versionnée](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/).
- [Kubernetes — Canary Deployment](https://kubernetes.io/docs/tutorials/stateless-application/canary-deployment/).
- [Kubernetes — Gateway API](https://gateway-api.sigs.k8s.io/) (implémentation et support à vérifier).

## Architecture et responsabilités
- [Patterns d'intégration du présent handbook](../01-integration-patterns/).
- [Patterns IA du présent handbook](../08-ai-architecture-patterns/).
- [Architecture consolidée de paiement fictif](../07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md).

**Note :** l'adresse des sources appartient à leur documentation technique. Les noms commerciaux dans l'URL n'identifient aucun client, ne sont pas présentés comme fournisseurs de l'architecture cible et n'impliquent aucune affiliation.
