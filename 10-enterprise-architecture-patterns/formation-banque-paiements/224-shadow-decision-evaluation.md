# Cours 224 — Shadow Decision Evaluation · Architecture décisionnelle / ODM (patterns génériques)

> Contexte fictif : plateforme OpenShift/Java et services bancaires. **Corrigé théorique, pas de runtime IBM ODM sous licence ni test CRC exécuté dans cette formation.**

## 1. Déclencheur métier / plateforme
Une version candidate d'une règle métier doit être comparée à celle actuellement autoritative sans impacter aucun contrat bancaire.

## 2. Architecture et responsabilités
~~~mermaid
flowchart LR
    A["Cas métier synthétiques / anonymisés"] --> B["Moteur actif + candidat shadow"]
    B --> C["Différences et écarts classés"]
    B -. "Refus, version incompatible ou panne" .-> D["Incident documenté / pas d'effet implicite"]
~~~

**Invariant :** Le moteur shadow ne modifie aucun état et sa réponse ne devient jamais la décision effective.

## 3. Contrat et frontière de confiance
1. Identifier les propriétaires des décisions, données et politiques ainsi que les consommateurs et identités techniques.
2. Versionner le contrat, définir les states autoritatifs, la sécurité et les permissions applicables.
3. Décrire impact de panne du plan ou moteur, conditions de retry et comportement si réponse indéterminée.
4. Tracer input, output, version, refus, latence p99, coût et revue d'architecture.
5. **Limite :** Shadow aide à comparer ; ne prouve pas exhaustivité sur cas rares ni performance sous charge.

## 4. Séquence nominale / incident
~~~mermaid
sequenceDiagram
    participant C as Consommateur / opérateur
    participant P as Frontière de politique ou contrat
    participant E as Plan ou moteur cible
    C->>P: requête avec identité et version
    P->>P: vérifier habilitations et invariants
    alt autorisé et résultat démontré
      P->>E: action déclarative / évaluation
      E-->>P: état, décision et provenance
      P-->>C: réponse attestée
    else invalide ou moteur indisponible
      E--xP: timeout ou rejet
      P-->>C: refus ou INDETERMINATE explicite
    end
~~~

## 5. Preuves de Design Authority
- **Test principal :** Injecter un cas où les versions diffèrent : journaliser écarts, contrôler seuil GO/NO-GO et prouver absence d'effet shadow.
- Tester source/tenant non autorisé, données ou politiques non versionnées, panne et réponse perdue.
- Vérifier le statut métier exact : un ACK, une recommandation ou un contrôle d'admission ne vaut pas règlement bancaire.
- Mesurer disponibilité, SLO, p95/p99, coût, logs expurgés, impact du rollback et réconciliation.
- Fournir ADR avec alternatives, matrice de responsabilités et résultats GO/NO-GO.

## 6. QCM corrigé
**Quelle démarche retiens-tu pour Shadow Decision Evaluation ?**
- **A.** Appliquer Shadow Decision Evaluation avec contrats, invariants et preuves de test.
- **B.** Supposer que le framework ou le moteur garantit directement la finalité d'un paiement.
- **C.** Ignorer droits, différences de versions et tests de panne pour accélérer la livraison.

**Réponse théorique : A.** Le moteur shadow ne modifie aucun état et sa réponse ne devient jamais la décision effective.

## 7. Fiche existante et approfondissement
[Source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/20-decision-management-patterns/04-shadow-decision-evaluation/README.md)

#### Problème

Une version candidate doit être évaluée sur les mêmes dossiers avant bascule. Pattern de référence indépendant d'un éditeur, sans affirmation d'exécution sous licence.

#### Schéma logique

```mermaid
flowchart LR
 A["Entrée anonymisée"] --> B["Moteur actuel autoritatif"] --> C["Moteur candidat read-only"]
```

#### Séquence de contrôle

```mermaid
sequenceDiagram
 participant A as Consumer
 participant B as Decision Service
 participant C as Engine/Policy
 A->>B: décision (requestId, version, identité)
 B->>C: évaluer sous contraintes
 C-->>B: decision + reasonCodes + version
 B->>B: audit et invariant
 B-->>A: statut attesté / non déterminé
```

#### Invariant

Le moteur shadow ne doit produire aucun effet externe et ne fournit jamais la décision autoritative.

#### Tests et gouvernance

1. Comparer décisions, motifs, délais et classes d'écarts sans utiliser de données personnelles réelles.
2. Si écarts inattendus dépassent un seuil approuvé : NO-GO et investigation.
3. Expirer le token ou demander un dossier d'un autre tenant : 401/403 sans exécution du moteur.
4. Tester incident pendant évaluation : aucune nouvelle écriture arbitraire; retour explicitement déterminé/inconnu.

#### Alternatives et décision

Distinguer moteur éditeur, interpréteur libre, règles en code et décisions ML; comparer versions, coûts, licencing, débit et responsabilité de support. Un POC simulé ne prouve ni conformité des licences ODM ni compatibilité runtime éditeur. Documenter ADR, contrat et preuve d'exécution.

[Catalogue décisionnel](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/20-decision-management-patterns/README.md) · [Sécurité Zero Trust](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/14-security-zero-trust-patterns/README.md)

[Programme](README.md) · [Révisions et preuves de la catégorie](exercices-et-corriges/cours-221-225.md)
