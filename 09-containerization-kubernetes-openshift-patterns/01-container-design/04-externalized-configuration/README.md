# 04 — Externalized Configuration

> **Famille : Conteneurisation.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Éviter de reconstruire un WAR/JAR pour changer les endpoints, secrets et paramètres d'environnement.

## 2. Solution et fonctionnement

Image immuable + ConfigMap non sensible + Secret/external secret pour identifiants + paramètres validés.

~~~mermaid
flowchart LR
  N0["Image commune"]
  N1["ConfigMap + Secrets"]
  N2["Environment"]
  N3["Application"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Le même JAR Java fonctionne dans dev et preprod avec une URL de dépendance différente.

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
env:
  - name: DOWNSTREAM_URL
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: downstreamUrl
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-credentials
        key: password
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Ne pas mettre secret dans ConfigMap.
- données de configuration versionnées.
- détection de changements et restart explicite si env vars..

## 5. Invariant et critères de choix

**À démontrer :** La promotion ne nécessite aucune recompilation.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| ConfigMap absente | Refus readiness avec message générique |
| Configuration erronée | Tests et validation avant rollout |
| Secret rotaté | Redémarrage ou reload contrôlé |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Externalized Configuration » ? **Réponse :** Image immuable + ConfigMap non sensible + Secret/external secret pour identifiants + paramètres validés. **Preuve requise :** La promotion ne nécessite aucune recompilation.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
