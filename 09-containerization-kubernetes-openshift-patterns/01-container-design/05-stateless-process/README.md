# 05 — Stateless Container / Twelve-Factor

> **Famille : Conteneurisation.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Permettre remplacement et scaling des Pods sans perdre la session ou le travail en cours.

## 2. Solution et fonctionnement

Stocker l'état durable en base ou stockage externe; conserver l'état transitoire uniquement en mémoire ou /tmp.

~~~mermaid
flowchart LR
  N0["Client"]
  N1["Service"]
  N2["replicas interchangeables"]
  N3["DB externe"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Une application Java passe de 1 à 3 replicas; les requêtes ne dépendent pas d'un disque ou d'une session locale.

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
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: app
          image: registry.example.invalid/team/app@sha256:<DIGEST>
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Sessions distribuées lorsque requises.
- aucune écriture de référence dans image.
- connexions/pools dimensionnées..

## 5. Invariant et critères de choix

**À démontrer :** Un Pod peut disparaître sans perte des opérations confirmées.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Pod redémarré | État durable hors Pod |
| Session sticky non disponible | Jetons stateless ou session partagée |
| Deux Pods traitent même commande | Idempotence côté core |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Stateless Container / Twelve-Factor » ? **Réponse :** Stocker l'état durable en base ou stockage externe; conserver l'état transitoire uniquement en mémoire ou /tmp. **Preuve requise :** Un Pod peut disparaître sans perte des opérations confirmées.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
