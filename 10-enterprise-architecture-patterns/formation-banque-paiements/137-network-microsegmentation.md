# Cours 137 — Network Micro-Segmentation / NetworkPolicy · Sécurité et Zero Trust

> Banque fictive · virement SEPA de 500 EUR · API Spring, IBM MQ et OpenShift. **Cours publié, corrigé théorique disponible ; exercice individuel non encore validé.**

## 1. Problème et contexte
Dans un cluster OpenShift partagé, les pods Reporting n'ont pas besoin de contacter la base Paiement. Une politique « allow all east-west » accroît la surface latérale en cas de compromission.

## 2. Objectif d'architecture et garanties
Appliquer default deny ingress ET egress sur les workloads sensibles, ouvrir les flux nécessaires (ports, sélecteurs, DNS, dépendances), valider le comportement réel du CNI et vérifier l'isolement entre namespaces.

**Invariant à démontrer :** Un pod d'un namespace non autorisé ne peut pas se connecter directement au port de la base des paiements.

## 3. Architecture de référence
```mermaid
flowchart LR
    A["Pod reporting / intrus"] --> B["Default deny et règles ingress/egress"]
    B --> C["DB paiements autorisée uniquement depuis son API"]
    B -. "Incident ou refus" .-> D["Blocage + diagnostic + audit"]
```

### Contrat de contrôle (pseudo-code)
```text
permitNetwork = sourceNamespace == 'payments-api' && sourceServiceAccount == allowed && port == approvedDbPort

if NOT allow:
    denyAndAudit()
else:
    executeOnlyAuthorizedOperation()
```

Le pseudo-code est conceptuel ; il ne remplace pas le moteur de politique, le coffre ou les contrôles en production.

## 4. Séquence nominale et négative
```mermaid
sequenceDiagram
    participant A as Workload ou opérateur
    participant P as Politique et contrôle
    participant R as Ressource protégée
    A->>P: identité et opération sur ressource
    P->>P: valider droits, contexte, version
    alt contrôle validé
        P->>R: exécuter l'action autorisée
        R-->>P: résultat exact
        P-->>A: résultat sans secret
    else contrôle rejeté ou indisponible
        P-->>A: accès bloqué et incident traçable
    end
```

## 5. Tests de sécurité et de résilience
1. Cas nominal : autorisation accordée uniquement à l'identité et à l'action attendues.
2. **Attaque simulée :** Depuis un pod reporting, tenter une connexion TCP à PostgreSQL Paiement : échec réseau ; l'API autorisée reste opérationnelle.
3. **Défaillance ou panne de cycle de vie :** Une règle egress oubliée laisse sortie vers l'extérieur ou une ouverture trop large expose les services pendant la bascule.
4. Les tests doivent vérifier le comportement en OpenShift (plusieurs pods, renouvellement, perte réseau, chemins directs ou détournés).
5. Les journaux, métriques et traces ne contiennent ni mots de passe, jetons, clés privées ni données bancaires injustifiées.
6. Des contrôles en échec n'autorisent jamais un paiement par défaut ; les états financiers restent exacts.
7. **Exploitation :** Conserver matrice flux/ports/propriétaires, tests pod-à-pod, DNS, routes opérateur, egress et comportement lors d'une nouvelle version.

## 6. Compromis, périmètre et ADR
La segmentation limite les chemins réseau ; elle ne prouve ni la bonne identité du client ni son droit métier sur la ressource.

Documenter les responsabilités, la frontière de confiance, le blast radius, les exceptions à durée limitée, les paramètres de refus en cas de panne, le coût et les critères GO/NO-GO.

## 7. QCM corrigé
**Quelle solution convient au besoin de Network Micro-Segmentation / NetworkPolicy ?**
- **A.** Supposer que le réseau privé ou une seule mesure technique suffit à autoriser la transaction.
- **B.** Désactiver les contrôles lors de l'indisponibilité de la sécurité et déclarer le paiement accepté.
- **C.** Appliquer Network Micro-Segmentation / NetworkPolicy avec des droits minimaux, des preuves de contrôle et des tests de panne.

**Bonne réponse : C.** Un pod d'un namespace non autorisé ne peut pas se connecter directement au port de la base des paiements.

Ce corrigé n'indique pas une réponse déjà obtenue en session.

## 8. Documentation approfondie du catalogue
[Fiche existante dans le dépôt](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/09-network-microsegmentation/README.md)

> **Famille : Sécurité et Zero Trust** · Modèle de référence, exemples fictifs sans attribution à une entreprise.

#### 1. Problème et exigence

Les workloads communiquent tous en est-ouest.

**Solution proposée :** Imposer default deny et seules ouvertures nécessaires sur namespaces, pods, ports et identités.

#### 2. Schéma d'architecture

~~~mermaid
flowchart LR
    A["Zone A"] --> B["Policy réseau + egress"] --> C["Zone B"]
~~~

Le chemin de décision représente des responsabilités : il ne présuppose ni fournisseur, ni protocole, ni disponibilité prouvée. Chaque flèche doit recevoir un contrat et des mesures de sécurité.

#### 3. Séquence et preuve

~~~mermaid
sequenceDiagram
    actor Owner as Responsable autorisé
    participant A as Zone A
    participant B as Policy réseau + egress
    participant C as Zone B
    Owner->>A: Demander opération selon politique
    A->>B: Contrat, identité et référence
    B->>C: Décision/transition contrôlée
    C-->>B: Preuve ou résultat incertain
    B-->>A: État attesté, erreur ou investigation
    A-->>Owner: Résultat sans invention d'effet
~~~

**Exemple illustratif :** L'API peut joindre son DB mais pas le namespace de l'analytique.

#### 4. Choix architecturaux

1. Identifier actifs, propriétaires, menace/panne de référence et hypothèses de déploiement.
2. Définir frontières, identité métier stable, requêtes et réponses autoritatives.
3. Écrire l'invariant avant la technologie : **Un Pod intrus ne peut appeler la DB protégée.**
4. Choisir mécanisme de stockage et d'accès, autorisations minimales et observabilité.
5. Prévoir fail-safe / fail-closed selon obligations, sans confondre indisponibilité et rejet financier.
6. Documenter coût, latence p99, capacité et modèle de responsabilité d'astreinte.

#### 5. Compromis et non-garanties

- **À privilégier** quand le scénario déclenche réellement : Les workloads communiquent tous en est-ouest.
- **Attention :** Policy réseau sans politique egress reste incomplète.
- **Non-garantie :** Imposer default deny et seules ouvertures nécessaires sur namespaces, pods, ports et identités. Le résultat doit encore être **prouvé par test** sur les ressources et sources de vérité concernées.
- **Alternative à évaluer :** simplifier le nombre de composants, utiliser un mécanisme géré déjà disponible ou réduire le rayon d'impact si les NFR le permettent.

#### 6. Scénarios d'échec et attaques

| Injection contrôlée | Comportement attendu |
|---|---|
| L'appelant perd la réponse après l'effet | Conserver la même référence, retrouver état ou investigation |
| Nœud, lien ou instance indisponible | Pas de divergence silencieuse ni décision sans preuve |
| Identité invalide / token expiré | Refus au point de contrôle concerné, audit sans secret |
| Modification de configuration risquée | Gate CI/policy ou ADR et rollback technique contrôlé |

#### 7. Plan de qualification

- Vérifier **Un Pod intrus ne peut appeler la DB protégée.** avec scénario reproductible et états avant/après.
- Injecter réseau partitionné ou certificat expiré selon scénario, sans mettre en péril un environnement réel.
- Vérifier observabilité : saturation, latence p95/p99, logs d'audit expurgés, SLI/SLO et alertes.
- Démontrer contrôle d'autorisation avec un acteur ayant **zéro privilège** sur l'objet cible.
- Simuler reprise ou révocation et mesurer temps de convergence, RPO/RTO si pertinent.

#### 8. Question d'entretien

**Quelle est la limite du pattern « Network Micro-Segmentation » ?** Policy réseau sans politique egress reste incomplète. La garantie à présenter au comité n'est acquise qu'après tests de un pod intrus ne peut appeler la db protégée.

#### 9. Navigation

- [Les patterns de cette famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/README.md)
- [Architecture transverse, incidents et ADR](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/CASE_STUDY.md)
- [Matrice de choix](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/DECISION_MATRIX.md)
- [Invariants financiers existants](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/07-case-studies/instant-payments-openshift/ARCHITECTURE_DE_REFERENCE.md)

[Programme des 140 cours](README.md) · [Exercices Sécurité 129–140](exercices-et-corriges/cours-129-140.md)
