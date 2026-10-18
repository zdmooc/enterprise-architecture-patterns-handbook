# 08 — Ambassador / Local Proxy

> **Famille : Pods Kubernetes.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Découpler le protocole externe de l'application sans contaminer son code.

## 2. Solution et fonctionnement

Un proxy local dans le Pod gère TLS, retries de connexion autorisés ou adaptation au protocole externe.

~~~mermaid
flowchart LR
  N0["Java"]
  N1["localhost ambassador"]
  N2["mTLS"]
  N3["service externe"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Le Java ne voit que localhost:15001; le proxy se connecte à un service externe authentifié. Les retries de mutations financières restent interdits sans idempotence.

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
containers:
  - name: legacy-proxy
    image: registry.example.invalid/tools/proxy:stable
    ports:
      - containerPort: 15001
    resources:
      requests: {cpu: 50m, memory: 64Mi}
      limits: {memory: 128Mi}
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Confirmer nécessité réelle du sidecar contre service mesh/gateway.
- gérer certificats, ports, timeout, observabilité et erreurs..

## 5. Invariant et critères de choix

**À démontrer :** Le proxy n'invente pas de statut métier en cas de timeout.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Certificat expiré | Rotation et alerte |
| Proxy répond 503 | Le service métier ne conclut pas à rejet |
| Retry dangereux | Désactiver sur opérations à effet sans idempotence |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Ambassador / Local Proxy » ? **Réponse :** Un proxy local dans le Pod gère TLS, retries de connexion autorisés ou adaptation au protocole externe. **Preuve requise :** Le proxy n'invente pas de statut métier en cas de timeout.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
