# 07 — Sidecar (Native et classique)

> **Famille : Pods Kubernetes.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Ajouter une capacité technique locale sans modifier les binaires métier.

## 2. Solution et fonctionnement

Un conteneur auxiliaire partage le réseau et éventuellement un volume avec le conteneur principal.

~~~mermaid
flowchart LR
  N0["App"]
  N1["volume partagé"]
  N2["sidecar télémétrie"]
  N3["collector externe"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Un agent de télémétrie lit un volume de logs de l'application; il ne devient pas un service métier obligatoire si l'on peut utiliser collecte node-level.

### Séquence de mise en place

~~~mermaid
sequenceDiagram
  actor A as Architecte / Exploitant
  participant G as Plateforme
  participant W as Workload
  A->>G: Déclarer la configuration du pattern
  G->>W: Réconcilier et démarrer
  W-->>G: Etat de readiness / observation
  G-->>A: Indicateur ou anomalie à corriger
~~~

## 3. Implémentation indicative (yaml)

~~~yaml
initContainers:
  - name: log-agent
    image: registry.example.invalid/tools/agent:stable
    restartPolicy: Always
    volumeMounts:
      - name: logs
        mountPath: /logs
  # Fonction « native sidecar » sur versions Kubernetes compatibles.
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Sidecars natifs via initContainers restartPolicy Always sur K8s compatibles.
- classiques comme conteneur parallèle.
- réserver CPU/RAM..

## 5. Invariant et critères de choix

**À démontrer :** La panne de télémétrie n'altère pas les invariants métier.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Sidecar saturé | Quotas spécifiques |
| Ordre de stop incorrect | Choisir sidecar natif et tester termination |
| Volume partagé trop large | Limiter chemins et droits |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Sidecar (Native et classique) » ? **Réponse :** Un conteneur auxiliaire partage le réseau et éventuellement un volume avec le conteneur principal. **Preuve requise :** La panne de télémétrie n'altère pas les invariants métier.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
