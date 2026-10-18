# 14 — Startup / Readiness / Liveness Probes

> **Famille : Workloads, résilience et capacité Cloud Native.** Exemple générique anonymisé. Extraits de configuration à contextualiser ; les noms de registry sont fictifs.

## 1. Problème

Confondre délai de démarrage Java, panne interne et dépendance externe peut provoquer un redémarrage en boucle.

## 2. Pattern et fonctionnement

Startup limite les redémarrages précoces, readiness retire du trafic, liveness détecte un processus bloqué ; ne pas attacher liveness à la disponibilité du core.

~~~mermaid
flowchart LR
    S0["Démarrage"]
    S1["startup OK"]
    S2["readiness OK"]
    S3["Service endpoints"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
~~~

**Exemple concret :** Une application Java met 45 secondes à charger ses classes : startup l'attend ; readiness échoue si elle ne peut plus servir ; liveness reste locale.

## 3. Séquence opérationnelle illustrée

~~~mermaid
sequenceDiagram
  actor O as Operateur
  participant K as API Kubernetes
  participant W as Workload
  O->>K: Pod démarre, startupProbe échoue transitoirement
  K->>W: Application termine son démarrage
  O->>K: Readiness valide le service
  K->>W: En cas d'indisponibilité, retirer endpoint sans redémarrer arbitrairement
  W-->>O: Etat observé, décision de validation
~~~

## 4. Exemple YAML

~~~yaml
startupProbe:
  httpGet: {path: /health/startup, port: 8080}
  failureThreshold: 30
  periodSeconds: 2
readinessProbe:
  httpGet: {path: /health/ready, port: 8080}
  periodSeconds: 5
livenessProbe:
  httpGet: {path: /health/live, port: 8080}
  periodSeconds: 10
~~~

> Extrait non nécessairement autonome ; le manifeste du cas d'étude contient les ressources et la combinaison des patterns pour une application Java. `registry.example.invalid` est un placeholder. Les contrôleurs optionnels nécessitent leur CRD et installation propres.

## 5. Choix et contraintes d'architecture

- Seuils et periodSeconds mesurés en charge réelle.
- Readiness adaptée aux capacités réellement nécessaires.
- Liveness ne doit pas redémarrer sur panne partagée d'une dépendance externe.

**Principale garantie :** Startup limite les redémarrages précoces, readiness retire du trafic, liveness détecte un processus bloqué ; ne pas attacher liveness à la disponibilité du core.

## 6. Modes de panne et remèdes

| Injection de panne | Réponse correcte |
|---|---|
| Probe trop agressive | CrashLoopBackOff : relever thresholds après mesure |
| Dépendance DB HS | Readiness ou dégradation métier, pas cascade liveness |
| Port probe non exposé | Tests de contrat/URL |

## 7. Tests de qualification et critères de revue

1. Soumettre le manifeste à une validation de schéma selon la **version du cluster cible** et vérifier son admission sans privilèges exceptionnels.
2. Vérifier comportement nominal, redémarrages, conditions de readiness, consommation et métriques p95/p99.
3. Injecter les pannes du tableau ; prouver absence de perte/double effet métier dans le domaine concerné.
4. Tester rollout/rollback et documenter les cas nécessitant intervention manuelle.
5. Mesurer les coûts, quotas, overhead CPU/RAM et limites d'auto-réparation ; vérifier la compatibilité OpenShift/SCC.

## 8. Question d'entretien d'architecte

**Que garantit réellement « Startup / Readiness / Liveness Probes » ?** Startup limite les redémarrages précoces, readiness retire du trafic, liveness détecte un processus bloqué ; ne pas attacher liveness à la disponibilité du core. Il ne suffit pas à assurer, seul, la disponibilité et la cohérence financière.

**Ressources complémentaires :** [architecture cible Java/JEE](../../09-case-study-java-jee-openshift/README.md) · [matrice de décision](../../DECISION_MATRIX.md) · [références](../../REFERENCES.md).
