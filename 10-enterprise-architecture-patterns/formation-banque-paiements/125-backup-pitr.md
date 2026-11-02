# Cours 125 — Backup / PITR · Résilience et systèmes distribués

> Formation bancaire fictive : virement 500 EUR. Corrigé théorique ; **exercice individuel non validé en session**.

## 1. Intention
Le pattern **Backup / PITR** sert à traiter un risque précis de saturation, de perte, de reprise ou de cohérence dans une architecture bancaire répartie.

## 2. Architecture du cas pédagogique
```mermaid
flowchart LR
    A["Sauvegardes et WAL"] --> B["Restauration à un instant"]
    B --> C["Rapprochement métier"]
    B -.-> D["Panne / timeout / divergence"]
    D --> E["Mesure, décision et reprise contrôlée"]
```

**Invariant de conception :** La restauration SQL ne rembobine pas les effets sur des systèmes tiers.

## 3. Exigences et contrats
- Identifier propriétaire de chaque donnée et de chaque effet financier.
- Définir p95/p99, RTO, RPO, budget d'erreurs et délais métier suivant le service concerné.
- Documenter la politique de reprise : référence stable, ancien/nouveau owner, idempotence, compensation licite.
- Distinguer `RECU`, `ACCEPTE`, `TRANSMIS`, `REGLE` et `UNKNOWN`.
- Protéger secrets, privilèges et données des clients pendant l'incident.
- Produire ADR, runbook et critères GO/NO-GO appuyés par une expérience réplicable.

## 4. Séquence incident et reprise
```mermaid
sequenceDiagram
    participant U as Client ou opérateur
    participant R as Contrôle de résilience
    participant S as Système source de vérité
    U->>R: opération ou vérification (réf stable)
    R->>S: demande autorisée
    S--xR: perte de résultat ou panne
    R->>R: classer l'incident, préserver les traces
    R->>S: recherche de statut / preuve et droits
    S-->>R: état prouvé ou indéterminé
    R-->>U: état exact / procédure d'investigation
```

## 5. Cas de qualification
1. Nominal : comportement et preuve de traitement exact.
2. Panne après commit : aucune répétition incontrôlée du même paiement.
3. Double sollicitation et partition : absence de double autorité.
4. Contrainte d'exploitation : pas de saturation silencieuse ni de rejet fictif.
5. Retour à la normale : critères vérifiables, alerte, traces et responsabilité d'astreinte.

## 6. Exercice corrigé
**Quelle option est correcte pour Backup / PITR ?**
- **A.** Appliquer Backup / PITR avec mesures, invariants et procédure de reprise testée.
- **B.** Répéter automatiquement tout virement après un timeout sans vérifier son statut.
- **C.** Remplacer les preuves métier par l'état Running d'un pod.

**Bonne réponse théorique : A.** La restauration SQL ne rembobine pas les effets sur des systèmes tiers.

## 7. Lecture technique approfondie du référentiel
[Source originale](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/13-resilience-distributed-systems-patterns/12-backup-pitr/README.md)

> **Famille : Systèmes distribués et résilience** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

#### 1. Problème et exigence

La réplication propage aussi une corruption logique et ne constitue pas une sauvegarde.

**Solution proposée :** Créer backups immuables/isolés, journaux PITR, restauration testée, clés et procédures.

#### 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["DB opérationnelle"] --> B["Backup + journaux isolés"] --> C["Restore à l'instant T"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

#### 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as DB opérationnelle
    participant B as Backup + journaux isolés
    participant C as Restore à l'instant T
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** Une suppression accidentelle est restaurée à une heure précise dans un lab.

#### 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **Exercice de restauration reconstruit les données avec RTO mesuré.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

#### 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : La réplication propage aussi une corruption logique et ne constitue pas une sauvegarde.
- **Attention :** Backup jamais restauré n'est pas une preuve de continuité.
- **Non-garantie :** Créer backups immuables/isolés, journaux PITR, restauration testée, clés et procédures. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

#### 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

#### 7. Plan de qualification

- Vérifier **Exercice de restauration reconstruit les données avec RTO mesuré.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

#### 8. Question d'entretien

**Quelle est la limite du pattern « Backup / Point-in-Time Recovery » ?** Backup jamais restauré n'est pas une preuve de continuité. La garantie à présenter au comité n'est acquise qu'après tests de exercice de restauration reconstruit les données avec rto mesuré.

#### 9. Navigation

- [Les patterns de cette famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/13-resilience-distributed-systems-patterns/README.md)
- [Architecture transverse, incidents et ADR](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/13-resilience-distributed-systems-patterns/CASE_STUDY.md)
- [Matrice de choix](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/13-resilience-distributed-systems-patterns/DECISION_MATRIX.md)
- [Invariants financiers existants](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)

[Retour au programme](README.md)
