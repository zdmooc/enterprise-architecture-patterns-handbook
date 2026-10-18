# 02 — Active–Active Partition Ownership

> **Famille : Systèmes distribués et résilience** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

## 1. Problème et exigence

Éviter un point unique tout en empêchant les écritures concurrentes incompatibles.

**Solution proposée :** Répartir des partitions entre sites actifs, avec **un seul propriétaire d'écriture par partition** et transferts explicites.

## 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["Partition X -> site A"] --> B["Router et ownership"] --> C["Partition Y -> site B"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

## 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as Partition X -> site A
    participant B as Router et ownership
    participant C as Partition Y -> site B
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** Deux sites servent des dossiers distincts ; une partition défaillante est transférée avec epoch.

## 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **Un split-brain ne permet pas deux commits sur la même partition.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

## 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : Éviter un point unique tout en empêchant les écritures concurrentes incompatibles.
- **Attention :** Active–active ne signifie pas multi-writer sur un même compte.
- **Non-garantie :** Répartir des partitions entre sites actifs, avec **un seul propriétaire d'écriture par partition** et transferts explicites. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

## 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

## 7. Plan de qualification

- Vérifier **Un split-brain ne permet pas deux commits sur la même partition.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

## 8. Question d'entretien

**Quelle est la limite du pattern « Active–Active Partition Ownership » ?** Active–active ne signifie pas multi-writer sur un même compte. La garantie à présenter au comité n'est acquise qu'après tests de un split-brain ne permet pas deux commits sur la même partition.

## 9. Navigation

- [Les patterns de cette famille](../README.md)
- [Architecture transverse, incidents et ADR](../CASE_STUDY.md)
- [Matrice de choix](../DECISION_MATRIX.md)
- [Invariants financiers existants](../../07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)
