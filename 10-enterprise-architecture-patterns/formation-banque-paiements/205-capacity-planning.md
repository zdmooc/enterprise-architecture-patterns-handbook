# Cours 205 — Capacity Planning · Performance et SRE

> Cas fictif : API Paiements Java/Spring, PostgreSQL, IBM MQ, OpenShift. **Corrigé théorique ; ni benchmark exécuté ni validation individuelle revendiqués.**

## 1. Besoin et contraintes
La hausse des volumes SEPA et la migration Java sur OpenShift exigent une projection CPU, mémoire JVM, partitions MQ et capacité de base.

## 2. Architecture de décision
~~~mermaid
flowchart LR
    A["Volumétrie + profil de charge"] --> B["Modèle capacitaire + tests"]
    B --> C["Requests/limits + marge validée"]
    B -. "Saturation ou panne" .-> D["Backpressure / alerte / investigation"]
~~~

**Invariant à vérifier :** Les pics prévus sont absorbés sans surcharge silencieuse du core, du broker ni des pods.

## 3. Contrat de performance et propriété du signal
- Décrire les SLI utilisateurs et métiers : erreurs réelles, p95/p99, trafic, saturation et fraîcheur.
- Enregistrer les limites : débit aval, nombre de connexions, stockage, mémoire JVM, deadline et coût.
- Distinguer refus avant acceptation d'une commande et perte de réponse après son exécution.
- Définir les budgets de retries/timeout, la stratégie de limitation de charge et le plan d'escalade.
- **Limite du pattern :** Dimensionner des pods sans tester la capacité aval et les règles de backpressure surestime le débit.

## 4. Séquence d'incident
~~~mermaid
sequenceDiagram
    participant U as Client
    participant A as API / Worker
    participant P as Limiteur ou contrôleur de ressources
    participant C as Source autoritative
    U->>A: demande, référence immuable
    A->>P: budget de capacité / admission
    alt Capacité suffisante
      P-->>A: autorisé
      A->>C: opération / consultation
      C-->>A: statut exact ou timeout
      A-->>U: état prouvé ou UNKNOWN
    else Saturé ou refusé avant effet
      P-->>A: limite atteinte
      A-->>U: refus contrôlé / retry policy
    end
~~~

## 5. Qualification et décision d'architecture
1. **Scénario ciblé :** Simuler croissance, perte d'une zone et requêtes longues ; mesurer p99, heap, backlog et coût.
2. Mesurer p50/p95/p99, trafic, saturation, erreurs métier et backlog selon la nature du service.
3. Produire un profil de charge progressif incluant pic, long tail, burst et panne d'une dépendance.
4. Contrôler coût/efficacité de l'option, stabilité des pools, autoscaling et plafonds aval.
5. Rejouer une commande avec clé stable après perte de réponse : un seul effet bancaire.
6. Exiger un GO/NO-GO sur les SLO et sur la confidentialité des traces.

## 6. Auto-évaluation
**Quelle architecture défendrais-tu pour Capacity Planning ?**
- **A.** Prétendre qu'un pod Running et un HTTP 200 prouvent un paiement correctement réglé.
- **B.** Retenter sans borne et supprimer les quotas pour améliorer la performance.
- **C.** Retenir Capacity Planning avec contrat de service, mesure et test de saturation/panne.

**Corrigé : C.** Les pics prévus sont absorbés sans surcharge silencieuse du core, du broker ni des pods.

## 7. Fiche technique détaillée du référentiel
[Source du pattern](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/16-performance-sre-patterns/10-capacity-planning/README.md)

> **Famille : Performance et SRE** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

#### 1. Problème et contexte

Une plateforme marche au nominal mais s'effondre sous burst et perte de zone.

**Pattern retenu :** Modéliser charge, demandes en vol, marges, GC, dépendances externes et capacité survivante.

#### 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Profil de trafic"] --> B["Modèle capacité"] --> C["Tests charge / stress / endurance"]
~~~

**Exemple de conception :** Un service Java est testé en pointe et avec une zone indisponible.

#### 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
  actor Sponsor as Responsable de capacité
  participant A as Profil de trafic
  participant B as Modèle capacité
  participant C as Tests charge / stress / endurance
  Sponsor->>A: Demande / événement métier
  A->>B: Contrat, identité et budget
  B->>C: Traitement conditionnel
  C-->>B: Résultat confirmé / résultat incertain
  B-->>A: État + preuve ou erreur explicite
  A-->>Sponsor: Résultat avec limites
~~~

#### 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **profil de trafic**, **modèle capacité** et **tests charge / stress / endurance**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

#### 5. Alternatives et décisions de design

- **Utilité :** Une plateforme marche au nominal mais s'effondre sous burst et perte de zone.
- **Règle structurante :** Modéliser charge, demandes en vol, marges, GC, dépendances externes et capacité survivante.
- **Danger :** Réplicas supplémentaires n'augmentent pas débit d'un core saturé.
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

1. **Critère central :** Charge x3 sous panne de zone respecte politique admission et intégrité.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

#### 8. Question d'entretien

**Quelles garanties le pattern « Capacity Planning / Load Profiles » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Modéliser charge, demandes en vol, marges, GC, dépendances externes et capacité survivante. Il ne dispense pas des tests : charge x3 sous panne de zone respecte politique admission et intégrité. Le principal piège reste : réplicas supplémentaires n'augmentent pas débit d'un core saturé.

#### 9. Voir aussi

- [Index de la famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/16-performance-sre-patterns/README.md)
- [Cas d'étude détaillé](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/16-performance-sre-patterns/CASE_STUDY.md)
- [Matrice de sélection](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/16-performance-sre-patterns/DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/README.md)

[Programme](README.md) · [Cahier SRE 196–205](exercices-et-corriges/cours-196-205.md)
