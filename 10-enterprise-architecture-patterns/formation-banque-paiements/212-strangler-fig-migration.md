# Cours 212 — Strangler Fig Migration · Modernisation Legacy Java/JEE

> Cas bancaire fictif : ancien moteur de paiement Java/JEE et modernisation OpenShift. **Corrigé théorique, aucune exécution sur produit propriétaire revendiquée.**

## 1. Déclencheur et cadre de la transformation
Une façade API route progressivement les services métiers d'un monolithe JEE vers des composants modernes.

## 2. Architecture AS-IS → transition → TO-BE
~~~mermaid
flowchart LR
    A["API Gateway / anti-corruption"] --> B["Routage par fonction/version"]
    B --> C["Legacy ou cible autoritative"]
    B -. "Risque de divergence" .-> D["Comparaison / réconciliation"]
~~~

**Invariant métier :** Chaque commande mutante a exactement un exécuteur autorisé pendant chaque vague de migration.

## 3. Cartographie et ADR avant migration
1. Recenser flux synchrones/async, API, dossiers, sessions, jobs batch, états financiers, données maîtresses et consommateurs.
2. Auditer dépendances JTA/XA, EJB, JDBC, IBM MQ/JMS, cache, fichiers, certificats et restrictions OpenShift.
3. Définir AS-IS, cible, transition, wave de migration, owners et versions d'API/contrats.
4. Fixer critères GO/NO-GO : autorisation, latence p99, volume, absence de double effet, RTO/RPO, reprise.
5. Écrire le plan de retour technique et le protocole de rapprochement financier sans promettre rollback métier.

**Limite connue :** La coexistence de deux implémentations exige politiques de données, ownership et détection de divergence.

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
- **Test de migration ciblé :** Basculer un type d'ordre vers nouveau module puis revenir sur ancien sans double effet.
- Tests de contrats, non-régression métier et jeux anonymisés avant/après.
- Test timeout/ACK perdu, duplication du message, backout MQ, reprise des jobs et états intermédiaires.
- Scénario deux writers, gestion d'affinité de sessions et incompatibilité de base.
- Evidence matrix avec versions, commits, résultats de tests, logs expurgés et responsabilités.
- Décision d'architecture comparative : Rehost, Replatform, Refactor, Replace, Retire, Retain.

## 6. Exercice corrigé
**Quelle option défendrais-tu pour Strangler Fig Migration ?**
- **A.** Choisir Strangler Fig Migration avec inventaire, contrats de non-régression et preuve de bascule.
- **B.** Déployer la cible puis oublier les consommateurs et les contrats du legacy.
- **C.** Exécuter ancien et nouveau moteurs financiers en parallèle sans aucun garde-fou.

**Réponse théorique : A.** Chaque commande mutante a exactement un exécuteur autorisé pendant chaque vague de migration.

## 7. Fiche de référence détaillée
[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/07-strangler-fig-migration/README.md)

> **Famille : Modernisation du SI historique** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

#### 1. Problème et contexte

Une réécriture big bang est trop risquée pour un SI interconnecté.

**Pattern retenu :** Insérer façade puis migrer capacité par capacité, jusqu'au retrait documenté de l'ancien.

#### 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Canaux"] --> B["Façade / routes"] --> C["Ancien et nouveau modules"]
~~~

**Exemple de conception :** Une consultation est migrée sans déclencher deux traitements d'écriture.

#### 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
  actor Sponsor as Responsable de capacité
  participant A as Canaux
  participant B as Façade / routes
  participant C as Ancien et nouveau modules
  Sponsor->>A: Demande / événement métier
  A->>B: Contrat, identité et budget
  B->>C: Traitement conditionnel
  C-->>B: Résultat confirmé / résultat incertain
  B-->>A: État + preuve ou erreur explicite
  A-->>Sponsor: Résultat avec limites
~~~

#### 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **canaux**, **façade / routes** et **ancien et nouveau modules**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

#### 5. Alternatives et décisions de design

- **Utilité :** Une réécriture big bang est trop risquée pour un SI interconnecté.
- **Règle structurante :** Insérer façade puis migrer capacité par capacité, jusqu'au retrait documenté de l'ancien.
- **Danger :** Deux propriétaires d'écriture simultanés sont inacceptables.
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

1. **Critère central :** Bascule peut revenir au chemin ancien sans double effet.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

#### 8. Question d'entretien

**Quelles garanties le pattern « Strangler Fig / Incremental Replacement » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Insérer façade puis migrer capacité par capacité, jusqu'au retrait documenté de l'ancien. Il ne dispense pas des tests : bascule peut revenir au chemin ancien sans double effet. Le principal piège reste : deux propriétaires d'écriture simultanés sont inacceptables.

#### 9. Voir aussi

- [Index de la famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/README.md)
- [Cas d'étude détaillé](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/CASE_STUDY.md)
- [Matrice de sélection](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/17-legacy-modernization-patterns/DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/README.md)

[Programme](README.md) · [Cahier de révision 206–215](exercices-et-corriges/cours-206-215.md)
