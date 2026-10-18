# 10 — Encryption at Rest / Key Management

> **Famille : Sécurité et Zero Trust** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

## 1. Problème et exigence

Les données chiffrées perdent confidentialité si clés et droits sont exposés.

**Solution proposée :** Gérer clés distinctes par périmètre, rotation, envelope encryption et accès audités.

## 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["Donnée sensible"] --> B["Clé contrôlée / KMS"] --> C["Stockage chiffré"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

## 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as Donnée sensible
    participant B as Clé contrôlée / KMS
    participant C as Stockage chiffré
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** Une base fictive chiffre les champs sensibles sous une clé rotatable.

## 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **La révocation de droits empêche déchiffrement par service non autorisé.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

## 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : Les données chiffrées perdent confidentialité si clés et droits sont exposés.
- **Attention :** Exporter le secret maître à tous les services annule les protections.
- **Non-garantie :** Gérer clés distinctes par périmètre, rotation, envelope encryption et accès audités. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

## 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

## 7. Plan de qualification

- Vérifier **La révocation de droits empêche déchiffrement par service non autorisé.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

## 8. Question d'entretien

**Quelle est la limite du pattern « Encryption at Rest / Key Management » ?** Exporter le secret maître à tous les services annule les protections. La garantie à présenter au comité n'est acquise qu'après tests de la révocation de droits empêche déchiffrement par service non autorisé.

## 9. Navigation

- [Les patterns de cette famille](../README.md)
- [Architecture transverse, incidents et ADR](../CASE_STUDY.md)
- [Matrice de choix](../DECISION_MATRIX.md)
- [Invariants financiers existants](../../07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)
