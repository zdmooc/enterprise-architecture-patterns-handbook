# Cours 130 — Policy Decision Point / Policy Enforcement Point · Sécurité et Zero Trust

> Cas bancaire pédagogique fictif : virement SEPA de 500 EUR, API Java/Spring, IBM MQ et OpenShift. **Cours publié avec corrigé théorique ; évaluation individuelle non réalisée.**

## 1. Problème concret
La banque a plusieurs règles de consultation d'ordres : rôle du collaborateur, appartenance à l'organisation et statut de confidentialité. Une Gateway seule ne suffit pas.

**Objectif :** Le PEP intercepte l'opération sur chaque chemin pertinent. Il envoie au PDP identité, action, ressource et contexte fiables ; il applique allow/deny avec obligations éventuelles. En cas d'indisponibilité, politique de refus documentée.

## 2. Modèle de menaces, périmètre de confiance
Le client, le pod OpenShift, la Gateway, le broker IBM MQ et le réseau privé **ne sont jamais réputés sûrs par simple localisation**. Distinguer authentification (qui appelle ?), autorisation (quelle action et quel objet ?) et preuve d'exécution (quel résultat financier a réellement eu lieu ?).

## 3. Acteurs et HLD
```mermaid
flowchart LR
    A["Requête au PEP local"] --> B["PDP : décision de politique"]
    B --> C["Service métier protégé"]
    B -. "Refus ou erreur" .-> D["Accès interdit + audit expurgé"]
```

**Invariant non négociable :** Contourner la Gateway et appeler directement le service ne doit pas permettre de consulter un ordre d'un autre client.

## 4. Contrat de sécurité (pseudo-code)
```text
decision = PDP.evaluate(subject, action, paymentOwner, tenant, context); if decision != ALLOW then DENY

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
2. **Test négatif prioritaire :** Le compte A tente GET /payment-orders/B, puis appel direct au service : refus dans les deux cas.
3. **Scénario de défaillance :** Le PDP dit deny mais le PEP l'ignore, ou le service répond avant le contrôle : fuite de données.
4. **Révocation :** vérifier que l'accès cesse selon une fenêtre de révocation définie, sans supposer que tous les jetons sont instantanément invalidés.
5. **Cohérence financière :** une erreur d'autorisation ne doit pas se transformer en ordre accepté ou réglé.
6. **Preuves d'exploitation :** Décisions allow/deny, latence p99 PDP, métriques par politique (sans PII), traçabilité de version et tests de bypass.

## 7. Arbitrage et limites
PDP décide ; PEP applique. Aucun de ces deux rôles ne doit être délégué à un simple prompt LLM.

Documenter l'ADR : menace traitée, points de contrôle, propriétaire de la politique, risque résiduel, disponibilité du service de sécurité, rotation et critères de validation. Privilégier des droits minimaux et une limitation explicite des impacts.

## 8. Exercice corrigé
**Quel choix retenir pour sécuriser le scénario « Policy Decision Point / Policy Enforcement Point » ?**
- **A.** Considérer qu'un réseau privé suffit à autoriser l'opération.
- **B.** Accepter toute requête si l'autorité de sécurité est momentanément indisponible.
- **C.** Appliquer Policy Decision Point / Policy Enforcement Point avec un contrôle vérifiable des sujets et des ressources.

**Bonne réponse théorique : C.** Contourner la Gateway et appeler directement le service ne doit pas permettre de consulter un ordre d'un autre client.

**Attention :** le corrigé sert à l'auto-étude et ne correspond à aucune réponse individuelle de l'apprenant.

## 9. Fiche technique existante et références
[Fiche de référence sur GitHub](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/02-policy-decision-enforcement/README.md)

> **Famille : Sécurité et Zero Trust** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

#### 1. Problème et exigence

Les règles d'accès sont dispersées et appliquées inégalement.

**Solution proposée :** Séparer PDP qui évalue la politique de PEP qui la fait respecter au point d'accès.

#### 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["Requête contextualisée"] --> B["PDP : décision"] --> C["PEP : exécution ou refus"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

#### 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as Requête contextualisée
    participant B as PDP : décision
    participant C as PEP : exécution ou refus
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** Le service autorise une lecture uniquement si rôle et tenant correspondent.

#### 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **Bypass de passerelle est bloqué côté service métier.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

#### 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : Les règles d'accès sont dispersées et appliquées inégalement.
- **Attention :** Le prompt IA n'est jamais un PEP fiable.
- **Non-garantie :** Séparer PDP qui évalue la politique de PEP qui la fait respecter au point d'accès. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

#### 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

#### 7. Plan de qualification

- Vérifier **Bypass de passerelle est bloqué côté service métier.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

#### 8. Question d'entretien

**Quelle est la limite du pattern « Policy Decision Point / Enforcement Point » ?** Le prompt IA n'est jamais un PEP fiable. La garantie à présenter au comité n'est acquise qu'après tests de bypass de passerelle est bloqué côté service métier.

#### 9. Navigation

- [Les patterns de cette famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/README.md)
- [Architecture transverse, incidents et ADR](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/CASE_STUDY.md)
- [Matrice de choix](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/DECISION_MATRIX.md)
- [Invariants financiers existants](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)

[Programme des 140 cours](README.md) · [Exercices Sécurité 129–140](exercices-et-corriges/cours-129-140.md)
