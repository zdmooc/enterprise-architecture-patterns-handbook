# Cours 213 — Parallel Run / Shadow · Modernisation Legacy Java/JEE

> Cas bancaire fictif : ancien moteur de paiement Java/JEE et modernisation OpenShift. **Corrigé théorique, aucune exécution sur produit propriétaire revendiquée.**

## 1. Déclencheur et cadre de la transformation
Pour comparer un nouveau moteur de règles, l'ancien décide en production et le candidat calcule en miroir sans effet.

## 2. Architecture AS-IS → transition → TO-BE
~~~mermaid
flowchart LR
    A["Ordre bancaire copié et expurgé"] --> B["Évaluation shadow isolée"]
    B --> C["Différences de décision auditées"]
    B -. "Risque de divergence" .-> D["Comparaison / réconciliation"]
~~~

**Invariant métier :** Le mode shadow ne transmet jamais d'ordre supplémentaire ni d'effet financier.

## 3. Cartographie et ADR avant migration
1. Recenser flux synchrones/async, API, dossiers, sessions, jobs batch, états financiers, données maîtresses et consommateurs.
2. Auditer dépendances JTA/XA, EJB, JDBC, IBM MQ/JMS, cache, fichiers, certificats et restrictions OpenShift.
3. Définir AS-IS, cible, transition, wave de migration, owners et versions d'API/contrats.
4. Fixer critères GO/NO-GO : autorisation, latence p99, volume, absence de double effet, RTO/RPO, reprise.
5. Écrire le plan de retour technique et le protocole de rapprochement financier sans promettre rollback métier.

**Limite connue :** Un shadow réussi n'établit pas seul la capacité de charge, ni l'absence de divergence sur les cas rares.

## 4. Séquence de cutover et incident
~~~mermaid
sequenceDiagram
    participant O as Design Authority
    participant R as Façade / Routeur
    participant L as Legacy Java/JEE
    participant N as Nouvelle solution
    O->>R: bascule approuvée d'une fonction
    R->>L: désactiver écriture sur périmètre migré
    R->>N: activer chemin autoritatif
    N-->>R: état observé
    alt résultat inconnu ou incident
       R->>N: rechercher statut par référence stable
       N-->>R: preuve ou UNKNOWN
       R-->>O: bloquer double traitement et décider
    else conformité démontrée
       R-->>O: GO avec trace et indicateurs
    end
~~~

## 5. Tests et livrables attendus
- **Test de migration ciblé :** Comparer 100 dossiers synthétiques avec doubles calculs ; bloquer toute sortie active du shadow.
- Tests de contrats, non-régression métier et jeux anonymisés avant/après.
- Test timeout/ACK perdu, duplication du message, backout MQ, reprise des jobs et états intermédiaires.
- Scénario deux writers, gestion d'affinité de sessions et incompatibilité de base.
- Evidence matrix avec versions, commits, résultats de tests, logs expurgés et responsabilités.
- Décision d'architecture comparative : Rehost, Replatform, Refactor, Replace, Retire, Retain.

## 6. Exercice corrigé
**Quelle option défendrais-tu pour Parallel Run / Shadow ?**
- **A.** Déployer la cible puis oublier les consommateurs et les contrats du legacy.
- **B.** Choisir Parallel Run / Shadow avec inventaire, contrats de non-régression et preuve de bascule.
- **C.** Exécuter ancien et nouveau moteurs financiers en parallèle sans aucun garde-fou.

**Réponse théorique : B.** Le mode shadow ne transmet jamais d'ordre supplémentaire ni d'effet financier.

## 7. Fiche de référence détaillée
[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/08-parallel-run-shadow/README.md)

> **Famille : Modernisation du SI historique** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

#### 1. Problème et contexte

La nouvelle implémentation doit être comparée à l'ancienne avant bascule.

**Pattern retenu :** Exécuter ancien chemin autoritatif et nouveau chemin shadow sans effet de bord, comparer réponses et écarts.

#### 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Chemin ancien autoritatif"] --> B["Shadow lecture seule"] --> C["Comparateur des écarts"]
~~~

**Exemple de conception :** Une consultation fictive est évaluée deux fois ; seul l'ancien résultat est affiché.

#### 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
  actor Sponsor as Responsable de capacité
  participant A as Chemin ancien autoritatif
  participant B as Shadow lecture seule
  participant C as Comparateur des écarts
  Sponsor->>A: Demande / événement métier
  A->>B: Contrat, identité et budget
  B->>C: Traitement conditionnel
  C-->>B: Résultat confirmé / résultat incertain
  B-->>A: État + preuve ou erreur explicite
  A-->>Sponsor: Résultat avec limites
~~~

#### 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **chemin ancien autoritatif**, **shadow lecture seule** et **comparateur des écarts**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

#### 5. Alternatives et décisions de design

- **Utilité :** La nouvelle implémentation doit être comparée à l'ancienne avant bascule.
- **Règle structurante :** Exécuter ancien chemin autoritatif et nouveau chemin shadow sans effet de bord, comparer réponses et écarts.
- **Danger :** Shadow sur commande financière réelle peut causer double débit.
- **À comparer :** statu quo surveillé, service managé conforme, capacité monolithique, séparation progressive et coûts réels.
- **Responsabilité :** le propriétaire métier signe les invariants ; l'exploitation certifie les procédures de reprise ; la Design Authority approuve les écarts.

#### 6. Matrice de pannes / contrôles

| Incident | Réaction attendue |
|---|---|
| Dépendance inaccessible avant traitement | Refuser/attendre selon contrat et durée maximale, sans succès fictif |
| Réponse réseau perdue après un commit | Retrouver la référence et l'état autoritatif sans répéter l'effet |
| Charge ou coûts dépassent le budget | Admission/régulation mesurable, alerte, maintien des requêtes déjà acquittées |
| Bascule/rollback sous données incompatibles | Bloquer opération et ouvrir runbook de reprise contrôlée |

#### 7. Expériences de qualification

1. **Critère central :** 0 effet externe du shadow, écarts expliqués.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

#### 8. Question d'entretien

**Quelles garanties le pattern « Parallel Run / Shadow Read-Only » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Exécuter ancien chemin autoritatif et nouveau chemin shadow sans effet de bord, comparer réponses et écarts. Il ne dispense pas des tests : 0 effet externe du shadow, écarts expliqués. Le principal piège reste : shadow sur commande financière réelle peut causer double débit.

#### 9. Voir aussi

- [Index de la famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/README.md)
- [Cas d'étude détaillé](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/CASE_STUDY.md)
- [Matrice de sélection](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/README.md)

[Programme](README.md) · [Cahier de révision 206–215](exercices-et-corriges/cours-206-215.md)
