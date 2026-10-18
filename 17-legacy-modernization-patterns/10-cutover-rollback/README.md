# 10 — Controlled Cutover / Rollback and Failback

> **Famille : Modernisation du SI historique** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

## 1. Problème et contexte

La bascule de flux vers une nouvelle plateforme peut laisser des commandes en vol et état incohérent.

**Pattern retenu :** Geler admission, drainer, réconcilier, transférer ownership, rouvrir avec canary, rollback sous conditions.

## 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Geler et drainer"] --> B["Transfert d'autorité"] --> C["Validation / failback"]
~~~

**Exemple de conception :** Le trafic d'un service fictif passe à une nouvelle API après reprise des messages non confirmés.

## 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
  actor Sponsor as Responsable de capacité
  participant A as Geler et drainer
  participant B as Transfert d'autorité
  participant C as Validation / failback
  Sponsor->>A: Demande / événement métier
  A->>B: Contrat, identité et budget
  B->>C: Traitement conditionnel
  C-->>B: Résultat confirmé / résultat incertain
  B-->>A: État + preuve ou erreur explicite
  A-->>Sponsor: Résultat avec limites
~~~

## 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **geler et drainer**, **transfert d'autorité** et **validation / failback**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

## 5. Alternatives et décisions de design

- **Utilité :** La bascule de flux vers une nouvelle plateforme peut laisser des commandes en vol et état incohérent.
- **Règle structurante :** Geler admission, drainer, réconcilier, transférer ownership, rouvrir avec canary, rollback sous conditions.
- **Danger :** Rollback de l'image ne défait pas une écriture financière déjà réglée.
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

1. **Critère central :** Aucun double effet lors de cutover ou retour.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

## 8. Question d'entretien

**Quelles garanties le pattern « Controlled Cutover / Rollback and Failback » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Geler admission, drainer, réconcilier, transférer ownership, rouvrir avec canary, rollback sous conditions. Il ne dispense pas des tests : aucun double effet lors de cutover ou retour. Le principal piège reste : rollback de l'image ne défait pas une écriture financière déjà réglée.

## 9. Voir aussi

- [Index de la famille](../README.md)
- [Cas d'étude détaillé](../CASE_STUDY.md)
- [Matrice de sélection](../DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](../../09-containerization-kubernetes-openshift-patterns/README.md)
