# Cours 206 — Rehost · Modernisation Legacy Java/JEE

> Cas bancaire fictif : ancien moteur de paiement Java/JEE et modernisation OpenShift. **Corrigé théorique, aucune exécution sur produit propriétaire revendiquée.**

## 1. Déclencheur et cadre de la transformation
Une application de paiement Java/JEE sur VM doit changer d'infrastructure en conservant son runtime et ses contrats presque inchangés.

## 2. Architecture AS-IS → transition → TO-BE
~~~mermaid
flowchart LR
    A["VM et artefact identifiés"] --> B["Migration infrastructure"]
    B --> C["Runtime cible qualifié"]
    B -. "Risque de divergence" .-> D["Comparaison / réconciliation"]
~~~

**Invariant métier :** Les interfaces et le comportement bancaire restent identiques avant et après changement d'hébergement.

## 3. Cartographie et ADR avant migration
1. Recenser flux synchrones/async, API, dossiers, sessions, jobs batch, états financiers, données maîtresses et consommateurs.
2. Auditer dépendances JTA/XA, EJB, JDBC, IBM MQ/JMS, cache, fichiers, certificats et restrictions OpenShift.
3. Définir AS-IS, cible, transition, wave de migration, owners et versions d'API/contrats.
4. Fixer critères GO/NO-GO : autorisation, latence p99, volume, absence de double effet, RTO/RPO, reprise.
5. Écrire le plan de retour technique et le protocole de rapprochement financier sans promettre rollback métier.

**Limite connue :** Rehost réduit le changement applicatif mais conserve souvent dette technique, licences et dépendances legacy.

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
- **Test de migration ciblé :** Migrer une VM de préproduction ; comparer transactions/latence, retours d'API, fichiers, certificats et rollback.
- Tests de contrats, non-régression métier et jeux anonymisés avant/après.
- Test timeout/ACK perdu, duplication du message, backout MQ, reprise des jobs et états intermédiaires.
- Scénario deux writers, gestion d'affinité de sessions et incompatibilité de base.
- Evidence matrix avec versions, commits, résultats de tests, logs expurgés et responsabilités.
- Décision d'architecture comparative : Rehost, Replatform, Refactor, Replace, Retire, Retain.

## 6. Exercice corrigé
**Quelle option défendrais-tu pour Rehost ?**
- **A.** Choisir Rehost avec inventaire, contrats de non-régression et preuve de bascule.
- **B.** Déployer la cible puis oublier les consommateurs et les contrats du legacy.
- **C.** Exécuter ancien et nouveau moteurs financiers en parallèle sans aucun garde-fou.

**Réponse théorique : A.** Les interfaces et le comportement bancaire restent identiques avant et après changement d'hébergement.

## 7. Fiche de référence détaillée
[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/01-rehost/README.md)

> **Famille : Modernisation du SI historique** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

#### 1. Problème et contexte

La plateforme historique est obsolète mais une refonte immédiate n'est pas autorisée.

**Pattern retenu :** Déplacer presque à l'identique l'exécution vers une infrastructure supportée, sans promettre une modernisation applicative.

#### 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Serveur historique"] --> B["Environnement rehost"] --> C["Service identique"]
~~~

**Exemple de conception :** Une VM fictive est migrée avec mêmes contrats et sauvegardes.

#### 3. Diagramme de séquence

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

#### 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **serveur historique**, **environnement rehost** et **service identique**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

#### 5. Alternatives et décisions de design

- **Utilité :** La plateforme historique est obsolète mais une refonte immédiate n'est pas autorisée.
- **Règle structurante :** Déplacer presque à l'identique l'exécution vers une infrastructure supportée, sans promettre une modernisation applicative.
- **Danger :** Déplacer ne corrige pas dette logicielle ni licences.
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

1. **Critère central :** Tests métier identiques et PRA requalifié.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

#### 8. Question d'entretien

**Quelles garanties le pattern « Rehost / Lift-and-Shift » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Déplacer presque à l'identique l'exécution vers une infrastructure supportée, sans promettre une modernisation applicative. Il ne dispense pas des tests : tests métier identiques et pra requalifié. Le principal piège reste : déplacer ne corrige pas dette logicielle ni licences.

#### 9. Voir aussi

- [Index de la famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/README.md)
- [Cas d'étude détaillé](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/CASE_STUDY.md)
- [Matrice de sélection](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/README.md)

[Programme](README.md) · [Cahier de révision 206–215](exercices-et-corriges/cours-206-215.md)
