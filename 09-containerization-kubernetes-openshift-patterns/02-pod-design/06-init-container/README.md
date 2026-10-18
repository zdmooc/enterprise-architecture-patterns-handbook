# 06 — Init Container

> **Famille : Pods Kubernetes.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Préparer une ressource avant démarrage sans incorporer le code de préparation à l'application.

## 2. Solution et fonctionnement

Un conteneur d'initialisation doit terminer avec succès avant de démarrer l'application principale.

~~~mermaid
flowchart LR
  N0["Pod"]
  N1["init checks"]
  N2["app container"]
  N3["ready"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Une API Java attend qu'un certificat interne monté soit validé; ne jamais faire de migration de schéma concurrente dans chaque Pod.

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
  - name: validate-config
    image: registry.example.invalid/base/busybox:stable
    command: ["sh", "-c", "test -r /config/app.properties"]
    volumeMounts:
      - name: config
        mountPath: /config
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Init repeatable et borné.
- image dédiée.
- éviter wait infinie.
- ne pas placer une migration SQL conflictuelle sur N replicas..

## 5. Invariant et critères de choix

**À démontrer :** Aucune instance ne sert du trafic avant ses préconditions locales.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Init bloqué | Alerte et logs explicites |
| Dépendance externe HS | Reprise contrôlée, timeout |
| Migration concurrente | Job singleton distinct |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Init Container » ? **Réponse :** Un conteneur d'initialisation doit terminer avec succès avant de démarrer l'application principale. **Preuve requise :** Aucune instance ne sert du trafic avant ses préconditions locales.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
