# 08 — Golden Signals / Distributed Tracing

> **Famille : Performance et SRE** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

## 1. Problème et contexte

Les incidents restent invisibles derrière un statut Pod Running.

**Pattern retenu :** Mesurer latency, traffic, errors, saturation, corréler traces et métriques métier.

## 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Instrumentation services"] --> B["Logs / metrics / traces"] --> C["Diagnostic de cause"]
~~~

**Exemple de conception :** Une augmentation du p99 est liée au pool DB saturé via traceId.

## 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
  actor Sponsor as Responsable de capacité
  participant A as Instrumentation services
  participant B as Logs / metrics / traces
  participant C as Diagnostic de cause
  Sponsor->>A: Demande / événement métier
  A->>B: Contrat, identité et budget
  B->>C: Traitement conditionnel
  C-->>B: Résultat confirmé / résultat incertain
  B-->>A: État + preuve ou erreur explicite
  A-->>Sponsor: Résultat avec limites
~~~

## 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **instrumentation services**, **logs / metrics / traces** et **diagnostic de cause**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

## 5. Alternatives et décisions de design

- **Utilité :** Les incidents restent invisibles derrière un statut Pod Running.
- **Règle structurante :** Mesurer latency, traffic, errors, saturation, corréler traces et métriques métier.
- **Danger :** Tracer des données sensibles complètes est interdit.
- **À comparer :** statu quo surveillé, service managé conforme, capacité monolithique, séparation progressive et coûts réels.
- **Responsabilité :** le propriétaire métier signe les invariants ; l'exploitation certifie les procédures de reprise ; la Design Authority approuve les écarts.

## 6. Matrice de pannes / contrôles

| Incident | Réaction attendue |
|---|---|
| Dépendance inaccessible avant traitement | Refuser/attendre selon contrat et durée maximale, sans succès fictif |
| Réponse réseau perdue après un commit | Retrouver la référence et l'état autoritatif sans répéter l'effet |
| Charge ou coûts dépassent le budget | Admission/régulation mesurable, alerte, maintien des requêtes déjà acquittées |
| Bascule/rollback sous données incompatibles | Bloquer opération et ouvrir runbook de reprise contrôlée |

## 7. Expériences de qualification

1. **Critère central :** L'incident peut être isolé jusqu'à sa dépendance causale.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

## 8. Question d'entretien

**Quelles garanties le pattern « Golden Signals / Distributed Tracing » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Mesurer latency, traffic, errors, saturation, corréler traces et métriques métier. Il ne dispense pas des tests : l'incident peut être isolé jusqu'à sa dépendance causale. Le principal piège reste : tracer des données sensibles complètes est interdit.

## 9. Voir aussi

- [Index de la famille](../README.md)
- [Cas d'étude détaillé](../CASE_STUDY.md)
- [Matrice de sélection](../DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](../../09-containerization-kubernetes-openshift-patterns/README.md)
