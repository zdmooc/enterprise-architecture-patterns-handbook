# 01 — Multi-Stage Build

> **Famille : Conteneurisation.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Compiler sans embarquer les outils de compilation dans l'image d'exécution.

## 2. Solution et fonctionnement

Séparer le stage de compilation et le runtime, puis copier uniquement l'artefact et ses ressources nécessaires.

~~~mermaid
flowchart LR
  N0["Sources"]
  N1["Build JDK"]
  N2["artefact JAR"]
  N3["Runtime JRE"]
  N4["Registry"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
~~~

**Exemple métier :** Une application Java est compilée en JAR dans une image JDK, puis exécutée avec un JRE minimal.

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

## 3. Implémentation indicative (dockerfile)

~~~dockerfile
FROM eclipse-temurin:21-jdk AS build
WORKDIR /src
COPY src/ ./src/
RUN javac -d /out src/ExampleServer.java

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /out/ /app/
EXPOSE 8080
CMD ["java", "ExampleServer"]
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Maven/JDK et runtime JRE sont versionnés indépendamment.
- privilégier les digests d'images approuvés.
- pipeline signé et SBOM..

## 5. Invariant et critères de choix

**À démontrer :** Le compilateur et les outils de build ne sont pas livrés en production.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Dépendances de compilation compromises | Construire sur images et dépôts approuvés |
| Image produite non conforme | Exécuter scans et tests de compatibilité |
| Artefact manquant | Arrêter la construction avant publication |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Multi-Stage Build » ? **Réponse :** Séparer le stage de compilation et le runtime, puis copier uniquement l'artefact et ses ressources nécessaires. **Preuve requise :** Le compilateur et les outils de build ne sont pas livrés en production.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
