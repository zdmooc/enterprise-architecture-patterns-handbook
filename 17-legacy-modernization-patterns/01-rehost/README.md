# 01 — Rehost / Lift-and-Shift

> **Famille : Modernisation du SI historique** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

## 1. Problème et contexte

La plateforme historique est obsolète mais une refonte immédiate n'est pas autorisée.

**Pattern retenu :** Déplacer presque à l'identique l'exécution vers une infrastructure supportée, sans promettre une modernisation applicative.

## 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Serveur historique"] --> B["Environnement rehost"] --> C["Service identique"]
~~~

**Exemple de conception :** Une VM fictive est migrée avec mêmes contrats et sauvegardes.

## 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
  actor Sponsor as Responsable de capacité
  participant A as Serveur historique
  participant B as Environnement rehost
  participant C as Service identique
  Sponsor->>A: Demande / événement métier
  A->>B: Contrat, identité et budget
  B->>C: Traitement conditionnel
  C-->>B: Résultat confirmé / résultat incertain
  B-->>A: État + preuve ou erreur explicite
  A-->>Sponsor: Résultat avec limites
~~~

## 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **serveur historique**, **environnement rehost** et **service identique**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

## 5. Alternatives et décisions de design

- **Utilité :** La plateforme historique est obsolète mais une refonte immédiate n'est pas autorisée.
- **Règle structurante :** Déplacer presque à l'identique l'exécution vers une infrastructure supportée, sans promettre une modernisation applicative.
- **Danger :** Déplacer ne corrige pas dette logicielle ni licences.
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

1. **Critère central :** Tests métier identiques et PRA requalifié.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

## 8. Question d'entretien

**Quelles garanties le pattern « Rehost / Lift-and-Shift » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Déplacer presque à l'identique l'exécution vers une infrastructure supportée, sans promettre une modernisation applicative. Il ne dispense pas des tests : tests métier identiques et pra requalifié. Le principal piège reste : déplacer ne corrige pas dette logicielle ni licences.

## 9. Voir aussi

- [Index de la famille](../README.md)
- [Cas d'étude détaillé](../CASE_STUDY.md)
- [Matrice de sélection](../DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](../../09-containerization-kubernetes-openshift-patterns/README.md)
