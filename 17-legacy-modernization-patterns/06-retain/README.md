# 06 — Retain / Encapsulate

> **Famille : Modernisation du SI historique** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

## 1. Problème et contexte

Un système est encore fiable/obligatoire malgré son ancienneté.

**Pattern retenu :** Le conserver sous protection et contrats stables, isoler interfaces et planifier évolution ultérieure.

## 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Core historique"] --> B["ACL + sécurité"] --> C["Services modernes"]
~~~

**Exemple de conception :** La tenue de compte fictive reste autoritative ; les nouveaux services consultent ses APIs.

## 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
  actor Sponsor as Responsable de capacité
  participant A as Core historique
  participant B as ACL + sécurité
  participant C as Services modernes
  Sponsor->>A: Demande / événement métier
  A->>B: Contrat, identité et budget
  B->>C: Traitement conditionnel
  C-->>B: Résultat confirmé / résultat incertain
  B-->>A: État + preuve ou erreur explicite
  A-->>Sponsor: Résultat avec limites
~~~

## 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **core historique**, **acl + sécurité** et **services modernes**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

## 5. Alternatives et décisions de design

- **Utilité :** Un système est encore fiable/obligatoire malgré son ancienneté.
- **Règle structurante :** Le conserver sous protection et contrats stables, isoler interfaces et planifier évolution ultérieure.
- **Danger :** Retain ne justifie pas une dette sans supervision/support.
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

1. **Critère central :** Contrat, support, patchs et RTO sont explicitement suivis.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

## 8. Question d'entretien

**Quelles garanties le pattern « Retain / Encapsulate » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Le conserver sous protection et contrats stables, isoler interfaces et planifier évolution ultérieure. Il ne dispense pas des tests : contrat, support, patchs et rto sont explicitement suivis. Le principal piège reste : retain ne justifie pas une dette sans supervision/support.

## 9. Voir aussi

- [Index de la famille](../README.md)
- [Cas d'étude détaillé](../CASE_STUDY.md)
- [Matrice de sélection](../DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](../../09-containerization-kubernetes-openshift-patterns/README.md)
