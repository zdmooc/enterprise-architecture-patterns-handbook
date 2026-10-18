# 13 — Chaos Engineering / Fault Injection

> **Famille : Systèmes distribués et résilience** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

## 1. Problème et exigence

Les scénarios de panne ne sont jamais exercés jusqu'à une crise réelle.

**Solution proposée :** Formuler hypothèse, rayon d'impact, garde-fous, rollback puis injecter pannes autorisées.

## 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["Hypothèse SLO"] --> B["Injection limitée"] --> C["Observation des invariants"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

## 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as Hypothèse SLO
    participant B as Injection limitée
    participant C as Observation des invariants
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** Un Pod de service fictif est tué pendant un test de charge en préproduction.

## 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **Panne simulée confirme le comportement prévu et le temps de reprise.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

## 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : Les scénarios de panne ne sont jamais exercés jusqu'à une crise réelle.
- **Attention :** Chaos destructif non approuvé ne constitue pas une preuve utile.
- **Non-garantie :** Formuler hypothèse, rayon d'impact, garde-fous, rollback puis injecter pannes autorisées. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

## 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

## 7. Plan de qualification

- Vérifier **Panne simulée confirme le comportement prévu et le temps de reprise.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

## 8. Question d'entretien

**Quelle est la limite du pattern « Chaos Engineering / Fault Injection » ?** Chaos destructif non approuvé ne constitue pas une preuve utile. La garantie à présenter au comité n'est acquise qu'après tests de panne simulée confirme le comportement prévu et le temps de reprise.

## 9. Navigation

- [Les patterns de cette famille](../README.md)
- [Architecture transverse, incidents et ADR](../CASE_STUDY.md)
- [Matrice de choix](../DECISION_MATRIX.md)
- [Invariants financiers existants](../../07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)
