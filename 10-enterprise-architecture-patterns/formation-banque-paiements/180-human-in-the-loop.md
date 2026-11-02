# Cours 180 — Human-in-the-Loop (HITL) — Approbation humaine · Architecture IA et agentique

> Banque fictive · ordre SEPA de 500 EUR. **Support pédagogique publié avec corrigé théorique ; aucun exercice individuel ni test sur cluster n'est déclaré validé.**

## 1. Besoin métier et problème
L'agent propose une correction d'écart sur un dossier de paiement fictif ; un collaborateur habilité doit approuver exactement les paramètres prévus avant toute action.

## 2. HLD : responsabilités des composants
~~~mermaid
flowchart LR
    A["Proposition IA versionnée"] --> B["ApprovalRequest hash + approbateur"]
    B --> C["Service métier idempotent"]
    B -. "Risque / absence de preuve" .-> STOP["Refus, attente ou abstention"]
~~~

**Décision d'architecture :** Stocker une proposition immuable avec hash, périmètre, initiateur, expiration, version métier et identifiant. Séparer demandeur et approbateur, revalider droits et payload au moment d'exécuter, puis appeler l'outil métier idempotent.

**Invariant à défendre :** Une modification d'un montant ou d'une référence invalide l'approbation précédente et interdit l'exécution.

## 3. Contrat de contrôle
~~~text
allowExecute = approved && hash(payload)==approval.hash && notExpired && SoD && currentStateVersion==approval.stateVersion
~~~

Ce pseudo-code est conceptuel et ne constitue pas un composant d'IA ou un connecteur bancaire exécutable.

## 4. Séquence principale et incident
~~~mermaid
sequenceDiagram
    participant U as Analyste habilité
    participant P as AI Gateway et Policy Engine
    participant A as Composant IA
    participant R as Source ou modèle autorisé
    U->>P: demande et identité
    P->>A: contexte filtré + budget / version
    A->>R: traitement autorisé
    alt résultat valide
        R-->>A: preuves et données
        A-->>P: réponse sourcée ou proposition
        P-->>U: résultat clairement non autoritatif
    else panne, refus ou sortie incertaine
        R--xA: timeout / erreur
        A-->>P: refus, attente ou UNKNOWN
        P-->>U: abstention ou incident
    end
~~~

## 5. Sécurité, qualité et preuves de laboratoire
1. **Contrôle nominal :** mesurer la réussite d'une tâche à périmètre et modèle fixés.
2. **Attaque simulée :** Modifier le montant après approbation : mismatch de hash ; refus et nouvelle approbation nécessaire.
3. **Panne / non-régression :** Exécuter sans accord, avec accord périmé, double approbation, changement d'état, deux clics et timeout après effet.
4. **Reprise et confidentialité :** ne jamais interpréter une indisponibilité de l'IA comme un règlement rejeté ou réglé ; conserver la classification des données.
5. **Mesures à instrumenter :** taux de rejets justifiés, délai d'approbation, double-effet évité, audits SoD, approbations expirées.
6. **Responsabilité métier :** toute opération sensible conserve une politique déterministe et, le cas échéant, une approbation humaine indépendante.

## 6. ADR et choix d'alternatives
Comparer la solution à une application déterministe, à un RAG sans agent et à un modèle local lorsque cela réduit le coût, la latence ou le risque. Documenter limites de contexte, budgets, risques indirects, versions, capacités OpenShift et stratégie de retrait.

## 7. Auto-évaluation corrigée
**Que faire si l'agent change le montant après validation humaine ?**
- **A.** Exécuter malgré tout puisque l'humain a déjà dit oui.
- **B.** Accepter si le modèle indique que la modification est mineure.
- **C.** Rejeter l'action, rendre l'accord caduc et exiger une nouvelle approbation exacte.

**Bonne réponse théorique : C.** Rejeter l'action, rendre l'accord caduc et exiger une nouvelle approbation exacte.

Cette clé est un corrigé de cours, pas une validation individuelle.

## 8. Référence détaillée existante dans le dépôt
[Fiche source du catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/10-human-in-the-loop/README.md)

> **Famille :** Sécurité / gouvernance · **Référentiel pédagogique anonymisé**. Aucun client ni fournisseur réel n'est identifié.

#### 1. Définition et problème métier

Une étape d'approbation humaine explicite contrôle les décisions ou actions à fort impact. Le système suspend l'exécution jusqu'à réception d'une approbation **authentifiée, autorisée, bornée et liée à un contenu immuable**.

**Pourquoi :** Un agent propose une correction comptable ou une modification de politique d'accès. Il ne doit pas agir simplement parce que son texte est convaincant.

#### 2. Architecture logique

~~~mermaid
flowchart TB
 AG["Agent : propose une action"] --> REQ["ApprovalRequest signée / versionnée"]
 REQ --> WAIT["Statut PENDING"]
 WAIT --> HUM{"Approbateur habilité"}
 HUM -->|Refus| STOP["Aucune action"]
 HUM -->|Expire| STOP
 HUM -->|Accord exact| CHECK["Revalider droits, hash, état métier"]
 CHECK --> EXEC["Outil métier idempotent"]
 EXEC --> AUDIT["Audit et résultat autoritatif"]
~~~

#### Déroulement

1. L'agent formule une **proposition** complète : effet attendu, paramètres, risques, références et preuves.
2. Créer un objet ApprovalRequest avec identifiant, hash du payload, demandeur, scope et deadline.
3. Notifier un approbateur habilité, différent du demandeur lorsque séparation des tâches requise.
4. L'approbateur voit la proposition exacte et approuve ou refuse avec authentification renforcée si nécessaire.
5. Le service métier revalide identité, approbation, version et état courant **avant** la mutation.
6. Exécuter au plus une fois avec idempotency-key ; enregistrer preuves, décisions, rejet ou expiration.

#### 3. Séquence métier illustrative

~~~mermaid
sequenceDiagram
 participant A as Agent
 participant W as Workflow HITL
 actor H as Approbateur
 participant T as Outil sensible
 A->>W: Proposer action X, hash H1
 W->>H: Examiner exact payload H1
 H-->>W: APPROVE H1 (identité attestée)
 W->>W: Vérifier expiry, droits, changement d'état
 W->>T: Execute action X + approvalId
 T-->>W: Résultat/exception vérifiable
 W-->>A: Réponse sur l'exécution, pas d'autorisation implicite
~~~

**Exemple :** L'agent prépare une proposition de **correction d'écart fictif**, mais seule une équipe habilitée peut valider. La proposition peut expirer si le statut financier a changé. Le workflow n'accepte pas d'approbation d'une version précédente.

#### 4. Arbitrages d'architecture

- Définir matrice d'autorisation et séparation des tâches par risque.
- Lier approbation à une **action précise** via hash et paramètres immuables.
- Expiration, révocation, double approbation éventuelle, délégation auditée.
- État PENDING/APPROVED/REJECTED/EXPIRED/EXECUTED et prévention des courses.
- Rejouabilité idempotente, investigation après timeout et preuve opposable.

#### 5. Scénarios de panne et attaques

| Incident | Parade |
|---|---|
| Proposition modifiée après accord | Hash mismatch => nouvelle approbation. |
| Approval ancienne sur état devenu différent | Revalider version avant action. |
| Compte approbateur compromis | Contrôles IAM/SCA adaptés, double approbation selon politique. |
| Double clic / retry de mutation | Idempotency-key + statut autoritatif. |
| Approval oubliée | Expiration et aucune mutation par défaut. |

#### 6. Tests de qualification

1. Mutation sans approbation échoue.
2. Même approvalId ne peut exécuter deux actions.
3. Modification d'un seul montant invalide l'approbation.
4. Approbation expirée/refusée empêche toute exécution.

**Critère transversal :** aucun accès à un compte ni changement financier sans la politique du système exécutant et son autorisation explicite.

#### 7. Quand choisir, quand éviter

Ajoute un délai humain et des coûts d'exploitation ; indispensable pour classes d'actions critiques, non requis sur simple réponse FAQ.

Mesurer sur un jeu d'essais : qualité, fidélité aux preuves, coût, latence p95/p99, permissions effectivement imposées et sécurité face aux contenus non fiables.

#### 8. Question d'entretien

**Question :** Comment empêcher qu'un agent exécute une action différente de celle approuvée ?

**Réponse :** Lier le consentement à un payload immuable, vérifier son hash et revalider l'état et les droits côté outil.

#### 9. Mise en œuvre / prolongements

- Services Java ou Python sur Kubernetes/OpenShift, policy engine et métriques, sans dépendance obligatoire à un éditeur particulier.
- [Plateforme IA de référence](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) · [Matrice des patterns](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/PATTERNS_DECISION_MATRIX.md) · [Références](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/08-ai-architecture-patterns/REFERENCES.md).
- Ne jamais confondre **proposition générée**, **approbation** et **exécution réellement confirmée**.

[Retour au programme](README.md) · [Cahier des exercices IA](exercices-et-corriges/cours-171-185.md)
