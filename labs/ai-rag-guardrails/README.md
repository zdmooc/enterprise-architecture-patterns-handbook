# Lab IA — Retrieval ACL + outils sécurisés + approbation humaine

## Objet
Laboratoire **100 % local, offline et sans dépendance externe**, écrit en Python standard. Il illustre cinq invariants : filtrage documentaire par tenant/rôle, citations extraites de sources autorisées, allowlist d'outils en lecture, approval liée à un payload immuable, exécution idempotente d'une **action fictive**.

> **Pas d'appel LLM, pas d'embeddings, pas d'index vectoriel, pas d'intégration bancaire, aucune opération financière.** Le moteur de recherche est lexical simplifié et sert à vérifier le fonctionnement des frontières d'accès, non la qualité réelle d'un RAG génératif. Le système d'approbation est **en mémoire**, sans verrou interprocessus, stockage durable ou identité cryptographique ; il n'est **pas production-ready**.

## Exécuter

Depuis la racine du dépôt :

~~~bash
python labs/ai-rag-guardrails/demo.py
python -m unittest discover -s labs/ai-rag-guardrails -v
~~~

Versions conseillées : Python 3.10 ou supérieur.

## Fichiers
- [demo.py](demo.py) : Retriever ACL, outil en lecture seule, workflow d'approbation et action de modification d'un dossier **fictif**.
- [test_demo.py](test_demo.py) : tests de tenant, scopes, citation, injection non exécutée, refus d'outil, séparation demandeur/approbateur, immutabilité, expiration, concurrence d'état et idempotence.

## Explication de la démonstration
1. L'utilisateur \`tenant-a\` demande une procédure sur les timeouts. Le moteur cherche **uniquement** les documents de son tenant et de son rôle avant tout classement.
2. Il renvoie des **citations littérales** sans invoquer le contenu comme instruction. Un document malveillant peut être cité comme texte, mais ne déclenche **aucun** outil.
3. \`ToolBroker\` n'autorise que \`case.read_status\` pour le rôle analyste, sur les dossiers du tenant.
4. L'analyste dépose une proposition \`MARK_REVIEWED\` sur le dossier fictif \`D-001\` à sa version courante.
5. Un approbateur **distinct**, dans le même tenant, accepte une empreinte du payload avant expiration.
6. L'exécution revérifie hash, version et identités ; un second appel retourne le **même résultat** sans nouvel effet.

## Invariants testés, sans surpromesse
| Contrôle | Test |
|---|---|
| Pas de fuite entre tenants | \`test_other_tenant_filtered\` |
| Droit documentaire | \`test_confidential_document_filtered\` |
| Résultat sourcé | \`test_allowed_source_has_citation\` |
| Document non fiable ne devient pas un outil | \`test_untrusted_document_is_only_quoted_not_executed\` |
| Tool allowlist | \`test_tool_allowlist_blocks_mutation\` |
| Séparation maker/checker | \`test_maker_checker_separation\` |
| Hash d'approbation | \`test_payload_change_invalidates_approval\` |
| Approbation expirée | \`test_expired_approval_rejected\` |
| Idempotence de l'effet fictif | \`test_idempotent_execution_of_approved_action\` |
| Version d'état | \`test_stale_case_state_blocked\` |

## Extension pour un vrai POC
- Remplacer le Retriever lexical par un RAG vectoriel/hybride, avec re-filtrage d'habilitations.
- Ajouter un **LLM local** en consultation uniquement ; red-team d'injection et tests de fidélité.
- Séparer Tool Broker, HITL et système de référence ; auth réelle et RBAC à chaque frontière.
- Utiliser stockage ACID durable + contrainte unique + contrôles de concurrence pour les approbations et effets.
- Déployer via manifestes sécurisés et exécuter des tests d'injection, charge, résilience et PRA.

Voir : [Architecture complète](../../08-ai-architecture-patterns/reference-ai-platform-openshift/README.md) et [Guardrails](../../08-ai-architecture-patterns/09-guardrails/README.md).
