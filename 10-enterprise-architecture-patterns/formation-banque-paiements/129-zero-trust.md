# Cours 129 — Zero Trust / Never Trust by Network · Sécurité et Zero Trust

> Cas bancaire pédagogique fictif : virement SEPA de 500 EUR, API Java/Spring, IBM MQ et OpenShift. **Cours publié avec corrigé théorique ; évaluation individuelle non réalisée.**

## 1. Problème concret
La Payment API et le worker IBM MQ sont dans le même cluster OpenShift. Cette proximité réseau ne doit jamais suffire pour lire ou modifier un ordre de paiement.

**Objectif :** À chaque requête, identifier le sujet (utilisateur ou service), la ressource et l'action. Valider token et claims, vérifier l'appartenance de l'ordre à son propriétaire et la politique de risque. Refuser par défaut.

## 2. Modèle de menaces, périmètre de confiance
Le client, le pod OpenShift, la Gateway, le broker IBM MQ et le réseau privé **ne sont jamais réputés sûrs par simple localisation**. Distinguer authentification (qui appelle ?), autorisation (quelle action et quel objet ?) et preuve d'exécution (quel résultat financier a réellement eu lieu ?).

## 3. Acteurs et HLD
```mermaid
flowchart LR
    A["Client / workload authentifié"] --> B["Contrôle d'identité et de contexte"]
    B --> C["Service et ressource autorisés"]
    B -. "Refus ou erreur" .-> D["Accès interdit + audit expurgé"]
```

**Invariant non négociable :** Un pod du même namespace sans identité valide, ou un utilisateur d'un autre tenant, ne peut lire l'ordre bancaire.

## 4. Contrat de sécurité (pseudo-code)
```text
allow = validIdentity(subject) && authorized(subject, resource, action) && acceptableContext(request)

if NOT allow:
    deny()
    audit(referencedPolicyVersion, opaqueCorrelationId)
else:
    executeAuthorizedOperation()
```
Le pseudo-code n'est pas un composant Spring exécutable ; les identités, attributs et politiques sont obtenus exclusivement depuis des sources **vérifiées**. Une décision d'accès ne prouve pas le règlement du paiement.

## 5. Séquence nominale et refus
```mermaid
sequenceDiagram
    participant C as Client / pod
    participant E as Enforcement
    participant P as Contrôle / politique
    participant S as Ressource bancaire
    C->>E: requête avec identité vérifiable
    E->>P: identité, action, ressource et contexte
    alt autorisation établie
        P-->>E: ALLOW
        E->>S: opération autorisée
        S-->>E: résultat exact
        E-->>C: résultat contractuel
    else non autorisé ou résultat incertain
        P-->>E: DENY ou indisponible
        E-->>C: refus sans fuite de données
    end
```

## 6. Tests, contrôles et observabilité
1. **Test nominal :** un appelant muni de droits vérifiables ne peut exécuter que l'action permise.
2. **Test négatif prioritaire :** Créer un pod non autorisé dans le réseau interne puis tenter GET /payment-orders/{id} : réponse refusée, aucune donnée sensible.
3. **Scénario de défaillance :** Une erreur d'introspection ou du moteur de politique entraîne un accès accordé ; la politique doit définir refus et traitement de l'indisponibilité.
4. **Révocation :** vérifier que l'accès cesse selon une fenêtre de révocation définie, sans supposer que tous les jetons sont instantanément invalidés.
5. **Cohérence financière :** une erreur d'autorisation ne doit pas se transformer en ordre accepté ou réglé.
6. **Preuves d'exploitation :** P95 des vérifications d'accès, volume de refus, identité des workloads, journaux expurgés et réévaluation aux points nécessaires.

## 7. Arbitrage et limites
Zero Trust est une architecture de vérification continue, non une technologie et non un synonyme de microsegmentation.

Documenter l'ADR : menace traitée, points de contrôle, propriétaire de la politique, risque résiduel, disponibilité du service de sécurité, rotation et critères de validation. Privilégier des droits minimaux et une limitation explicite des impacts.

## 8. Exercice corrigé
**Quel choix retenir pour sécuriser le scénario « Zero Trust / Never Trust by Network » ?**
- **A.** Considérer qu'un réseau privé suffit à autoriser l'opération.
- **B.** Appliquer Zero Trust / Never Trust by Network avec un contrôle vérifiable des sujets et des ressources.
- **C.** Accepter toute requête si l'autorité de sécurité est momentanément indisponible.

**Bonne réponse théorique : B.** Un pod du même namespace sans identité valide, ou un utilisateur d'un autre tenant, ne peut lire l'ordre bancaire.

**Attention :** le corrigé sert à l'auto-étude et ne correspond à aucune réponse individuelle de l'apprenant.

## 9. Fiche technique existante et références
[Fiche de référence sur GitHub](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/01-zero-trust/README.md)

> **Famille : Sécurité et Zero Trust** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

#### 1. Problème et exigence

Une application intracluster est réputée sûre du seul fait de son adresse.

**Solution proposée :** Vérifier explicitement identité, appareil/workload, objet métier et risque pour chaque accès.

#### 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["Client / workload"] --> B["Décision continue de confiance"] --> C["Ressource protégée"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

#### 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as Client / workload
    participant B as Décision continue de confiance
    participant C as Ressource protégée
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** Un Pod dans le même namespace doit fournir identité pour lire un dossier restreint.

#### 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **Appel interne sans jeton est refusé.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

#### 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : Une application intracluster est réputée sûre du seul fait de son adresse.
- **Attention :** Réseau privé ne remplace pas AuthZ.
- **Non-garantie :** Vérifier explicitement identité, appareil/workload, objet métier et risque pour chaque accès. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

#### 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

#### 7. Plan de qualification

- Vérifier **Appel interne sans jeton est refusé.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

#### 8. Question d'entretien

**Quelle est la limite du pattern « Zero Trust / Never Trust by Network » ?** Réseau privé ne remplace pas AuthZ. La garantie à présenter au comité n'est acquise qu'après tests de appel interne sans jeton est refusé.

#### 9. Navigation

- [Les patterns de cette famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/README.md)
- [Architecture transverse, incidents et ADR](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/CASE_STUDY.md)
- [Matrice de choix](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/DECISION_MATRIX.md)
- [Invariants financiers existants](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)

[Programme des 140 cours](README.md) · [Exercices Sécurité 129–140](exercices-et-corriges/cours-129-140.md)
