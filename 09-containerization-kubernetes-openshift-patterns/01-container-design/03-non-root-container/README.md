# 03 — Non-Root / Arbitrary UID

> **Famille : Conteneurisation.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Lancer des applications sans privilèges root et compatibles avec UID attribués dynamiquement.

## 2. Solution et fonctionnement

Éviter runAsUser fixe si non validé par l'allocation de namespace; préparer les chemins nécessaires pour un UID arbitraire.

~~~mermaid
flowchart LR
  N0["Image compatible UID arbitraire"]
  N1["SCC restrictive"]
  N2["Pod non-root"]
  N3["accès /tmp uniquement"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Une application Java écoute sur 8080, utilise /tmp pour fichiers temporaires, et n'écrit pas sous /opt/app.

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
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Pas de chmod 777.
- écrire seulement sur mounts prévus.
- cap drop ALL, seccomp runtime default, allowPrivilegeEscalation false..

## 5. Invariant et critères de choix

**À démontrer :** Le Pod démarre sous un UID arbitraire autorisé, sans privilège élevé.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Répertoire non accessible | Préparer droits groupe/volume adaptés |
| Port 80 privilégié | Écouter 8080 derrière Service |
| Application exige root | Reconcevoir ou documenter exception, pas anyuid par défaut |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Non-Root / Arbitrary UID » ? **Réponse :** Éviter runAsUser fixe si non validé par l'allocation de namespace; préparer les chemins nécessaires pour un UID arbitraire. **Preuve requise :** Le Pod démarre sous un UID arbitraire autorisé, sans privilège élevé.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
