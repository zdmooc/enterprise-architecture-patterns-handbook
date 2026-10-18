# 09 — Adapter / Log Format Normalization

> **Famille : Pods Kubernetes.** Cas d'application Java/JEE fictif et anonymisé. Les noms d'images `registry.example.invalid` sont des exemples non déployables sans remplacement et validation.

## 1. Problème d'architecture

Normaliser télémétrie ou formats périphériques sans réécrire le service principal.

## 2. Solution et fonctionnement

Un sidecar lit une sortie locale, convertit le format et transmet à un collecteur.

~~~mermaid
flowchart LR
  N0["Application logs"]
  N1["Adapter sidecar"]
  N2["schéma commun"]
  N3["Observabilité"]
  N0 --> N1
  N1 --> N2
  N2 --> N3
~~~

**Exemple métier :** Un serveur Java écrit des logs applicatifs structurés; un adapter ancien convertit les champs pour l'outil d'exploitation.

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
volumes:
  - name: telemetry-buffer
    emptyDir:
      sizeLimit: 100Mi
# Si un adapter est justifié, limiter les permissions et la taille.
~~~

**Important :** extrait de principe, non manifeste complet. Pour les workloads complets, utiliser le cas d'étude et ses manifestes validables. Adapter versions de runtime, images, limites et SCC à la plateforme visée.

## 4. Principaux arbitrages

- Éviter traitement de données personnelles hors contrat.
- préférer stdout+collector si possible.
- tampon borné et pas de blocage..

## 5. Invariant et critères de choix

**À démontrer :** Un échec de normalisation de logs ne doit pas bloquer le paiement.

Sélectionner ce pattern uniquement si le problème est présent : mesurer latence, nombre de replicas, empreinte d'image, isolation, charge, sécurité et reprise. Comparer à une option plus simple avant d'ajouter un sidecar, un contrôleur ou un cluster.

## 6. Scénarios de panne

| Injection | Réaction attendue |
|---|---|
| Fichier mal formé | Quarantaine des lignes |
| Disque plein | Buffer borné / rotation |
| Données sensibles | Masquage et minimisation |

### Tests de qualification

1. Déployer le manifeste avec admission restrictive et vérifier le démarrage sans accès root ni secrets en clair.
2. Injecter une panne locale du Pod ou d'une dépendance et vérifier le comportement décrit dans la matrice.
3. Vérifier les logs et métriques : latence, redémarrages, ressources, erreurs, temps de reprise et perte éventuelle de données.
4. Déployer/rollback une nouvelle image et confirmer l'absence de changement métier non autorisé.

## 7. Critères Design Authority / entretien

**Question :** pourquoi adopter « Adapter / Log Format Normalization » ? **Réponse :** Un sidecar lit une sortie locale, convertit le format et transmet à un collecteur. **Preuve requise :** Un échec de normalisation de logs ne doit pas bloquer le paiement.

À documenter avant production : objectifs SLO, modèle de menace, ownership de la configuration, versions et compatibilité Kubernetes/OpenShift, procédures de reprise, coûts/licences, validation de l'équipe d'exploitation.

**Voir :** [architecture Java/JEE complète](../../09-case-study-java-jee-openshift/README.md) · [index des 30 patterns](../../README.md) · [références officielles](../../REFERENCES.md).
