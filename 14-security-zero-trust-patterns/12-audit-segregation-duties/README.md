# 12 — Audit Trail / Segregation of Duties

> **Famille : Sécurité et Zero Trust** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

## 1. Problème et exigence

Un seul acteur peut demander, approuver, exécuter et effacer la preuve.

**Solution proposée :** Séparer demandeur, approbateur, exécuteur et auditeur, avec événements infalsifiables et rétention.

## 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["Demande"] --> B["Approbation indépendante"] --> C["Exécution + audit"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

## 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as Demande
    participant B as Approbation indépendante
    participant C as Exécution + audit
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** Une correction fictive nécessite approbation distincte et enregistre référence d'opération.

## 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **Un approbateur ne peut approuver sa propre demande.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

## 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : Un seul acteur peut demander, approuver, exécuter et effacer la preuve.
- **Attention :** Logs applicatifs non protégés ne constituent pas preuve forte.
- **Non-garantie :** Séparer demandeur, approbateur, exécuteur et auditeur, avec événements infalsifiables et rétention. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

## 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

## 7. Plan de qualification

- Vérifier **Un approbateur ne peut approuver sa propre demande.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

## 8. Question d'entretien

**Quelle est la limite du pattern « Audit Trail / Segregation of Duties » ?** Logs applicatifs non protégés ne constituent pas preuve forte. La garantie à présenter au comité n'est acquise qu'après tests de un approbateur ne peut approuver sa propre demande.

## 9. Navigation

- [Les patterns de cette famille](../README.md)
- [Architecture transverse, incidents et ADR](../CASE_STUDY.md)
- [Matrice de choix](../DECISION_MATRIX.md)
- [Invariants financiers existants](../../07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)
