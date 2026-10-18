# 10 — Human-in-the-Loop (HITL)

> **Famille :** Sécurité / gouvernance · **Référentiel pédagogique anonymisé**. Aucun client ni fournisseur réel n'est identifié.

## 1. Définition et problème métier

Une étape d'approbation humaine explicite contrôle les décisions ou actions à fort impact. Le système suspend l'exécution jusqu'à réception d'une approbation **authentifiée, autorisée, bornée et liée à un contenu immuable**.

**Pourquoi :** Un agent propose une correction comptable ou une modification de politique d'accès. Il ne doit pas agir simplement parce que son texte est convaincant.

## 2. Architecture logique

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

### Déroulement

1. L'agent formule une **proposition** complète : effet attendu, paramètres, risques, références et preuves.
2. Créer un objet ApprovalRequest avec identifiant, hash du payload, demandeur, scope et deadline.
3. Notifier un approbateur habilité, différent du demandeur lorsque séparation des tâches requise.
4. L'approbateur voit la proposition exacte et approuve ou refuse avec authentification renforcée si nécessaire.
5. Le service métier revalide identité, approbation, version et état courant **avant** la mutation.
6. Exécuter au plus une fois avec idempotency-key ; enregistrer preuves, décisions, rejet ou expiration.

## 3. Séquence métier illustrative

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

## 4. Arbitrages d'architecture

- Définir matrice d'autorisation et séparation des tâches par risque.
- Lier approbation à une **action précise** via hash et paramètres immuables.
- Expiration, révocation, double approbation éventuelle, délégation auditée.
- État PENDING/APPROVED/REJECTED/EXPIRED/EXECUTED et prévention des courses.
- Rejouabilité idempotente, investigation après timeout et preuve opposable.

## 5. Scénarios de panne et attaques

| Incident | Parade |
|---|---|
| Proposition modifiée après accord | Hash mismatch => nouvelle approbation. |
| Approval ancienne sur état devenu différent | Revalider version avant action. |
| Compte approbateur compromis | Contrôles IAM/SCA adaptés, double approbation selon politique. |
| Double clic / retry de mutation | Idempotency-key + statut autoritatif. |
| Approval oubliée | Expiration et aucune mutation par défaut. |

## 6. Tests de qualification

1. Mutation sans approbation échoue.
2. Même approvalId ne peut exécuter deux actions.
3. Modification d'un seul montant invalide l'approbation.
4. Approbation expirée/refusée empêche toute exécution.

**Critère transversal :** aucun accès à un compte ni changement financier sans la politique du système exécutant et son autorisation explicite.

## 7. Quand choisir, quand éviter

Ajoute un délai humain et des coûts d'exploitation ; indispensable pour classes d'actions critiques, non requis sur simple réponse FAQ.

Mesurer sur un jeu d'essais : qualité, fidélité aux preuves, coût, latence p95/p99, permissions effectivement imposées et sécurité face aux contenus non fiables.

## 8. Question d'entretien

**Question :** Comment empêcher qu'un agent exécute une action différente de celle approuvée ?

**Réponse :** Lier le consentement à un payload immuable, vérifier son hash et revalider l'état et les droits côté outil.

## 9. Mise en œuvre / prolongements

- Services Java ou Python sur Kubernetes/OpenShift, policy engine et métriques, sans dépendance obligatoire à un éditeur particulier.
- [Plateforme IA de référence](../reference-ai-platform-openshift/README.md) · [Matrice des patterns](../PATTERNS_DECISION_MATRIX.md) · [Références](../REFERENCES.md).
- Ne jamais confondre **proposition générée**, **approbation** et **exécution réellement confirmée**.
