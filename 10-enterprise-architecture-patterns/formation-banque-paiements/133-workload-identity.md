# Cours 133 — Workload Identity / Credentials courte durée · Sécurité et Zero Trust

> Cas bancaire pédagogique fictif : virement SEPA de 500 EUR, API Java/Spring, IBM MQ et OpenShift. **Cours publié avec corrigé théorique ; évaluation individuelle non réalisée.**

## 1. Problème concret
Les pods Spring Boot et workers MQ ne doivent plus partager le même mot de passe de service écrit dans les manifests ou l'image.

**Objectif :** Délivrer des identités liées au workload, avec audience et expiration bornées ; choisir ServiceAccount tokens projetés, identité fédérée ou certificats courts selon la plateforme. Limiter les droits et automatiser rotation et révocation.

## 2. Modèle de menaces, périmètre de confiance
Le client, le pod OpenShift, la Gateway, le broker IBM MQ et le réseau privé **ne sont jamais réputés sûrs par simple localisation**. Distinguer authentification (qui appelle ?), autorisation (quelle action et quel objet ?) et preuve d'exécution (quel résultat financier a réellement eu lieu ?).

## 3. Acteurs et HLD
```mermaid
flowchart LR
    A["Pod + ServiceAccount distinct"] --> B["Issuer d'identité / certificat court"]
    B --> C["API ou coffre qui valide l'identité"]
    B -. "Refus ou erreur" .-> D["Accès interdit + audit expurgé"]
```

**Invariant non négociable :** Un token d'un worker ne permet pas d'accéder à l'API d'un autre service ou à un autre tenant.

## 4. Contrat de sécurité (pseudo-code)
```text
allow = workloadIdentity.issuer == trusted && workloadIdentity.audience == target && hasAllowedServiceRole

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
2. **Test négatif prioritaire :** Copier un jeton du pod A pour accéder à une cible avec audience B : refus, aucune fuite de secret.
3. **Scénario de défaillance :** Un ServiceAccount commun à tous les namespaces possède des droits trop larges ; la compromission d'un pod devient transversale.
4. **Révocation :** vérifier que l'accès cesse selon une fenêtre de révocation définie, sans supposer que tous les jetons sont instantanément invalidés.
5. **Cohérence financière :** une erreur d'autorisation ne doit pas se transformer en ordre accepté ou réglé.
6. **Preuves d'exploitation :** Durée de vie, autorisations de ServiceAccount, tokens montés, audiences, politique d'échange et rotation mesurée.

## 7. Arbitrage et limites
Workload Identity établit la personnalité technique ; les politiques d'autorisation limitent les opérations qui lui sont accordées.

Documenter l'ADR : menace traitée, points de contrôle, propriétaire de la politique, risque résiduel, disponibilité du service de sécurité, rotation et critères de validation. Privilégier des droits minimaux et une limitation explicite des impacts.

## 8. Exercice corrigé
**Quel choix retenir pour sécuriser le scénario « Workload Identity / Credentials courte durée » ?**
- **A.** Considérer qu'un réseau privé suffit à autoriser l'opération.
- **B.** Accepter toute requête si l'autorité de sécurité est momentanément indisponible.
- **C.** Appliquer Workload Identity / Credentials courte durée avec un contrôle vérifiable des sujets et des ressources.

**Bonne réponse théorique : C.** Un token d'un worker ne permet pas d'accéder à l'API d'un autre service ou à un autre tenant.

**Attention :** le corrigé sert à l'auto-étude et ne correspond à aucune réponse individuelle de l'apprenant.

## 9. Fiche technique existante et références
[Fiche de référence sur GitHub](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/05-workload-identity/README.md)

> **Famille : Sécurité et Zero Trust** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

#### 1. Problème et exigence

Les services utilisent des mots de passe partagés et persistants.

**Solution proposée :** Attribuer identité cryptographique courte durée par workload et cible, et vérifier son audience.

#### 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["Service A identity"] --> B["Certificat / jeton éphémère"] --> C["Service B AuthZ"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

#### 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as Service A identity
    participant B as Certificat / jeton éphémère
    participant C as Service B AuthZ
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** Deux services Java s'authentifient mutuellement sans secret permanent dans le code.

#### 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **Révocation d'identité bloque immédiatement la nouvelle session selon contrat.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

#### 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : Les services utilisent des mots de passe partagés et persistants.
- **Attention :** Le ServiceAccount partagé par tous les Pods élargit le rayon d'attaque.
- **Non-garantie :** Attribuer identité cryptographique courte durée par workload et cible, et vérifier son audience. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

#### 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

#### 7. Plan de qualification

- Vérifier **Révocation d'identité bloque immédiatement la nouvelle session selon contrat.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

#### 8. Question d'entretien

**Quelle est la limite du pattern « Workload Identity / Short-Lived Credentials » ?** Le ServiceAccount partagé par tous les Pods élargit le rayon d'attaque. La garantie à présenter au comité n'est acquise qu'après tests de révocation d'identité bloque immédiatement la nouvelle session selon contrat.

#### 9. Navigation

- [Les patterns de cette famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/README.md)
- [Architecture transverse, incidents et ADR](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/CASE_STUDY.md)
- [Matrice de choix](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/DECISION_MATRIX.md)
- [Invariants financiers existants](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)

[Programme des 140 cours](README.md) · [Exercices Sécurité 129–140](exercices-et-corriges/cours-129-140.md)
