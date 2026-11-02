# Cours 191 — Multi-Region Strategy · Cloud hybride / Multicloud

> Banque fictive : virement SEPA de 500 EUR, core bancaire historique, Payment API Java/OpenShift. **Corrigé théorique fourni ; aucune évaluation personnelle ni preuve runtime revendiquée.**

## 1. Situation et déclencheur
Les services de consultation peuvent reprendre dans une région distante ; l'état financier ne doit jamais être écrit par deux régions sans propriété exclusive.

## 2. Structure et décision d'architecture
~~~mermaid
flowchart LR
    A["Région active"] --> B["Réplication / propriété d'écriture"]
    B --> C["Région de secours"]
    B -. "Rupture, dérive, non-conformité" .-> D["Refus / investigation / reprise"]
~~~

**Invariant à prouver :** La région secondaire n'écrit pas la même partition avant fencing et preuve de propriété.

## 3. Contrats d'architecture
1. Définir ownership, classification, IAM, identité workload, flux permis, localisation des données et interfaces de sortie.
2. Fixer les SLO, budget de latence, RTO/RPO, domaines de panne, coûts réseau/stockage et réversibilité.
3. Séparer la responsabilité du cloud et celle de la source de vérité bancaire.
4. Distinguer approbation de la gouvernance, disponibilité du réseau et exécution financière.
5. Établir matrice de flux, décisions ADR, responsable d'exploitation et procédure de retour.

**Limite connue :** Multi-région n'implique pas RPO zéro ni règlement exactly-once.

## 4. Séquence de défaillance
~~~mermaid
sequenceDiagram
    participant A as Architecte / opérateur
    participant P as Gouvernance cloud
    participant W as Workload Java
    participant S as Système bancaire source
    A->>P: demander changement de réseau/placement
    P->>W: appliquer contrat et politiques
    W->>S: échange autorisé, référence stable
    S--xW: liaison perdue / réponse inconnue
    W->>S: consulter état connu si autorisé
    S-->>W: état confirmé ou UNKNOWN
    W-->>P: incident / qualité de service
~~~

## 5. Tests, NFR et critères de Design Authority
- **Test ciblé :** Perdre la région active, simuler un primaire isolé encore vivant et tester le rejet des écritures tardives.
- Répéter une commande après perte réseau avec référence métier stable : aucune exécution financière double.
- Prouver frontières IAM/réseau, secret, chiffrement et localisation au périmètre spécifié.
- Mesurer failover, coût de trafic interrégional, latence p95/p99, capacité, RPO et RTO.
- Documenter alternative plus simple et risques de dépendance fournisseur.
- Distinguer preuve de configuration, test de laboratoire et acceptation opérationnelle.

## 6. QCM corrigé
**Quelle proposition est la plus défendable concernant Multi-Region Strategy ?**
- **A.** Choisir Multi-Region Strategy après cadrage et prouver les frontières, l'invariant et les tests de panne.
- **B.** Autoriser toute circulation dès que les réseaux sont privés.
- **C.** Considérer que le routage cloud garantit le règlement.

**Bonne réponse théorique : A.** La région secondaire n'écrit pas la même partition avant fencing et preuve de propriété.

## 7. Documentation approfondie du catalogue existant
[Consulter la fiche source](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/15-cloud-hybrid-architecture-patterns/06-multi-region-strategy/README.md)

> **Famille : Cloud hybride** · Architecture illustrative et anonyme, aucune affirmation sur un environnement réel.

#### 1. Problème et contexte

Le plan de continuité néglige les services globaux et la résidence des données.

**Pattern retenu :** Définir régions primaires/secondaires et périmètres de réplication, souveraineté, RTO/RPO et restauration.

#### 2. Diagramme d'architecture

~~~mermaid
flowchart LR
  A["Région primaire"] --> B["Réplication + contrôle"] --> C["Région de secours"]
~~~

**Exemple de conception :** Une région secondaire ne reprend une partition qu'après preuve des données acquittées.

#### 3. Diagramme de séquence

~~~mermaid
sequenceDiagram
  actor Sponsor as Responsable de capacité
  participant A as Région primaire
  participant B as Réplication + contrôle
  participant C as Région de secours
  Sponsor->>A: Demande / événement métier
  A->>B: Contrat, identité et budget
  B->>C: Traitement conditionnel
  C-->>B: Résultat confirmé / résultat incertain
  B-->>A: État + preuve ou erreur explicite
  A-->>Sponsor: Résultat avec limites
~~~

#### 4. Principes de mise en œuvre

1. Établir l'existant : dépendances, données, contrats, coûts, résilience et habilitations.
2. Expliquer les frontières entre **région primaire**, **réplication + contrôle** et **région de secours**.
3. Choisir une source d'autorité, définir références et versions ; ne jamais substituer un ACK réseau à un commit métier.
4. Définir les politiques de sécurité, réseau, sessions, quotas et télémétrie de chaque frontière.
5. Mettre en place un chemin de retour arrière compatible avec l'état durable ; si irréversible, définir investigation.
6. Qualifier performances p95/p99 et pannes (instance, réseau, stockage, zone/site selon NFR).

#### 5. Alternatives et décisions de design

- **Utilité :** Le plan de continuité néglige les services globaux et la résidence des données.
- **Règle structurante :** Définir régions primaires/secondaires et périmètres de réplication, souveraineté, RTO/RPO et restauration.
- **Danger :** Deux régions en lecture ne signifient pas réplication synchrone.
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

1. **Critère central :** Perte région mesurée; aucune écriture reconnue silencieusement perdue.
2. Vérifier le cas nominal et le comportement après crash entre commit et ACK.
3. Injecter une panne de connexion puis mesurer temps de convergence, RPO/RTO si applicable et ressources consommées.
4. Tester ACL utilisateur et identité workload, rotation des secrets, journaux expurgés.
5. Conserver preuve dans un dossier d'ADR : hypothèse, commande, résultat, test et responsable.

#### 8. Question d'entretien

**Quelles garanties le pattern « Multi-Region / Region Pair » apporte-t-il, et lesquelles n'apporte-t-il pas ?**

Définir régions primaires/secondaires et périmètres de réplication, souveraineté, RTO/RPO et restauration. Il ne dispense pas des tests : perte région mesurée; aucune écriture reconnue silencieusement perdue. Le principal piège reste : deux régions en lecture ne signifient pas réplication synchrone.

#### 9. Voir aussi

- [Index de la famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/15-cloud-hybrid-architecture-patterns/README.md)
- [Cas d'étude détaillé](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/15-cloud-hybrid-architecture-patterns/CASE_STUDY.md)
- [Matrice de sélection](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/15-cloud-hybrid-architecture-patterns/DECISION_MATRIX.md)
- [30 patterns Docker/Kubernetes/OpenShift](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/09-containerization-kubernetes-openshift-patterns/README.md)

[Programme](README.md) · [Cahier des exercices 186–195](exercices-et-corriges/cours-186-195.md)
