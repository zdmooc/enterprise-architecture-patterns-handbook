# Séquences détaillées — plateforme IA de référence

**Cas entièrement fictifs.** Aucune transaction bancaire ou entreprise réelle ; les paiements ne sont cités que pour illustrer la **non-autorité de l'IA** sur les mouvements financiers.

## S1 — RAG en lecture, avec droits documentaires

~~~mermaid
sequenceDiagram
  autonumber
  actor U as Collaborateur
  participant G as AI/API Gateway
  participant P as Policy Engine
  participant R as RAG Service
  participant I as Index documentaire
  participant M as LLM local
  participant V as Validateur citations
  U->>G: Pourquoi un virement reste sans confirmation ?
  G->>P: AuthN, tenant, droits, classification
  P-->>G: Corpus autorisé, budget
  G->>R: Question + identité
  R->>I: Search(query, filter ACL, version courante)
  I-->>R: Passages référencés, sourceId, version
  R->>R: Revérifier ACL, fraîcheur et provenance
  R->>M: Question + contexte délimité non fiable
  M-->>R: Synthèse et références
  R->>V: Contrôle appui des conclusions
  alt Sources suffisantes
    V-->>G: Réponse avec citations
    G-->>U: Procédure et limites
  else Sources insuffisantes
    V-->>G: Abstention motivée
    G-->>U: Sources insuffisantes
  end
~~~

**Cas de panne :** index indisponible → abstention/erreur selon contrat, **aucune génération non sourcée** d'une procédure critique. Document retiré → filtrage ACL empêche réapparition depuis un index obsolète.

## S2 — Agent avec outil de consultation autorisé

~~~mermaid
sequenceDiagram
  autonumber
  actor U as Analyste
  participant A as Agent
  participant P as Autorisations
  participant T as API de consultation
  participant L as LLM
  U->>A: Quel statut pour dossier D-001 ?
  A->>P: Requête get_case_status(D-001)
  P->>P: Identité, objet, allowlist, paramètres
  P-->>A: Autorisé, lecture seule
  A->>T: GET /cases/D-001
  T-->>A: Status=PENDING_REVIEW, version=7
  A->>L: Résultat d'outil comme donnée non fiable
  L-->>A: Proposition de réponse
  A-->>U: Statut PENDING_REVIEW, source=API
~~~

**Limite :** la sortie \`PENDING_REVIEW\` est un état déclaré par une API métier fictive. Si l'outil est indisponible, l'agent ne devine pas le statut ; une erreur technique n'autorise aucun outil de mutation.

## S3 — HITL sécurisé : l'agent propose, l'humain autorise

~~~mermaid
sequenceDiagram
  autonumber
  actor U as Utilisateur
  participant A as Agent
  participant W as Workflow d'approbation
  actor H as Approbateur habilité
  participant P as Policy Engine
  participant T as Outil métier idempotent
  U->>A: Préparer correction contrôlée d'un écart fictif
  A->>W: ApprovalRequest(action, params, payloadHash, expireAt)
  W-->>H: Proposer action exacte et preuves
  H->>W: APPROVED(payloadHash, identity)
  W->>P: Vérifier identité, autorité, expiry, payloadHash
  P-->>W: Approval valide sur état métier actuel
  W->>T: Execute(action, approvalId, idempotencyKey)
  T-->>W: Résultat ou UNKNOWN
  alt Résultat confirmé
    W-->>U: Exécution attestée et référence
  else Résultat inconnu
    W->>T: QueryStatus(approvalId)
    T-->>W: Statut autoritatif
    W-->>U: Statut vérifié ou investigation
  end
~~~

**Menaces à tester :** paramètre modifié après approbation, approbation expirée, approbateur dépourvu de droit, demande de mutation répétée, réponse API perdue et référence de mutation dupliquée.

## S4 — IA asynchrone sur événement d'incident

~~~mermaid
sequenceDiagram
  autonumber
  participant C as Service métier autoritatif
  participant O as Outbox
  participant B as Broker
  participant I as Worker IA + Inbox
  participant R as RAG runbooks
  actor H as Exploitant
  C->>O: TX: état incident + Outbox(eventId=E01)
  O->>B: Publish E01 (republication possible)
  B->>I: Incident E01
  I->>I: Inbox: E01 déjà traité ?
  alt Événement nouveau
    I->>R: Recherche autorisée
    R-->>I: Procédure documentée
    I-->>H: Rapport assisté, non autoritatif
  else Réception répétée
    I-->>B: ACK sans nouveau rapport
  end
  Note over C,H: Aucun mouvement financier déclenché par l'IA
~~~

**Panne :** le worker IA peut être indisponible ; les fonctions bancaires ne dépendent pas de sa reprise. La profondeur du broker, les quotas IA et le traitement de poison messages sont surveillés.

## S5 — Fallback de modèle et circuit ouvert

~~~mermaid
sequenceDiagram
  actor U as Utilisateur
  participant G as AI Gateway
  participant P as Router/Policy
  participant M1 as Modèle principal local
  participant M2 as Modèle secondaire local
  U->>G: Demande interne classifiée
  G->>P: Access policy, timeout budget
  P->>M1: Inférence v3
  M1--xP: 503 / timeout
  P->>P: Vérifier budget + cible secondaire autorisée
  alt Alternative conforme
    P->>M2: Même classe de données / contrat
    M2-->>P: Réponse v2 conforme
    P-->>G: Résultat + version réellement utilisée
    G-->>U: Résultat validé
  else Aucune alternative permise
    P-->>G: INFERENCE_UNAVAILABLE
    G-->>U: Indisponible, pas de transfert interdit
  end
~~~

La disponibilité ne justifie jamais un routage de données privées vers une cible non autorisée.

## S6 — Évaluation avant nouvelle version de modèle ou index

~~~mermaid
sequenceDiagram
  participant CI as Pipeline GitOps
  participant E as Evaluation Offline
  participant R as Red-Team Tests
  participant O as Responsable
  participant K as Plateforme qualification
  CI->>E: Modèle v4 + corpus v12 + golden set
  E-->>CI: Qualité et fidélité aux citations
  CI->>R: Scénarios injection et fuite
  R-->>CI: Résultats sécurité
  CI->>O: Synthèse des seuils
  alt Tous gates validés
    O-->>CI: Approval canary
    CI->>K: Déploiement shadow/canary
    K-->>O: SLO, taux refus, coût, drift
  else Gate critique échoué
    O-->>CI: Rejet et correction
  end
~~~

**À prouver :** le pipeline bloque effectivement toute régression d'accès documentaire, d'approbation d'outil et de fidélité sur les cas critiques.
