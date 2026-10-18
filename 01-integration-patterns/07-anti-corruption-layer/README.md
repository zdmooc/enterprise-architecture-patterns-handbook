# 07 — Adapter / Anti-Corruption Layer (ACL)

## Problème
Un nouveau service Java/OpenShift doit coopérer avec un système historique CICS/COBOL, IBM MQ ou Java/JEE. Les formats et **significations métier** ne sont pas identiques. Une conversion technique ne suffit pas : les codes « A01 = ordre accepté » et « règlement confirmé » ne décrivent pas le même état.

## Différence fondamentale
- **Adapter** : traduit interfaces techniques (REST/JSON ↔ MQ, SOAP, fichier, COBOL copybook), codecs, unités, formats.
- **Anti-Corruption Layer** : protège *le modèle de domaine* du système moderne en traduisant aussi statuts, invariants et conventions du legacy ; peut encapsuler un ou plusieurs adapters. Concept DDD.
- **API Gateway** : protège/routage les entrées ; ne remplace pas la traduction sémantique de domaine.

## Conception fictive
~~~mermaid
flowchart TB
  J["Service Java : ExecutePayment"]
  P["Port métier PaymentExecutionPort"]
  ACL["ACL : PaymentExecutionTranslator"]
  A["MQ Adapter : sérialisation, corrélation"]
  Q["IBM MQ REQUEST/RESPONSE"]
  C["COBOL / CICS legacy"]
  J --> P --> ACL --> A --> Q --> C
  C -.-> Q
  Q -.-> A
  A -.-> ACL
  ACL -.-> J
~~~

~~~text
Modèle Java : {paymentId:"VIR-001", amountMinor:50000, currency:"EUR"}
Modèle legacy fictif : REF=VIR-001 ; MONT_CENT=0000050000 ; DEVISE=EUR
Code retour A01 = ACCEPTED_FOR_PROCESSING ; E90 = REJECTED
~~~
Ce sont **des conventions inventées**, à ne jamais attribuer à CAPS ou à un produit IBM.

## Responsabilités du composant
1. Normaliser identifiants, unités monétaires, fuseaux, caractères, champs obligatoires.
2. Expliquer la correspondance des **états métier** ; jamais transformer ACCEPTED en SETTLED.
3. Centraliser anti-corruption des règles externes sans recopier le moteur métier dans l'ACL.
4. Traduire erreurs, codes, timeouts et cas « outcome unknown ».
5. Appliquer idempotency-key métier, correlation-id et versions de contrat sans inventer d'effet de livraison.
6. Journaliser transformations et décisions, sans exposer de données bancaires sensibles.

## Exemple de matrice de traduction
| Legacy fictif | API moderne | Précaution |
|---|---|---|
| A01 | ACCEPTED | Pas un règlement |
| E90 | REJECTED | Motif normalisé |
| Pas de réponse | UNKNOWN / TO_RECONCILE | Ne pas créer un nouveau paiement |
| S00 | SETTLED (après preuve) | Résultat autoritatif à conserver |

## Migration vers OpenShift
Strangler Fig : déployer une façade et de nouveaux services autour de l'existant ; migrer progressivement par capacités, jeux d'APIs, consommateurs et contrats stables. Décider si l'ACL vit en bibliothèque interne, microservice autonome ou composant d'intégration. Plus elle est centralisée, plus elle peut devenir un point de contention : haute disponibilité et ownership obligatoires.

## Modes de panne
- Format incompatible : mettre en quarantaine avec motif sans exécution.
- Legacy ne répond pas : statut indéterminé + interrogation/réconciliation.
- Réponse hors ordre : matcher la même référence, valider transition.
- Nouvelle version du copybook : contract tests entre versions ; rollback contrôlé.
- Arrêt de l'ACL : messages durables + circuit breaker des appelants + plan de reprise.

## Critères de décision
ACL recommandée si modèles métier indépendants, remplacement progressif, formats anciens ou risque élevé de pollution sémantique. Inutile si deux services partagent un contrat stable identique et pas de traduction de domaine.

## Entretien
**Q : pourquoi ne pas faire connaître les codes COBOL aux microservices ?** R : cela crée un couplage fort et reporte la complexité de migration partout. **Q : Adapter = ACL ?** Non, l'ACL porte la traduction sémantique et la protection du modèle.

Sources : [Microsoft Architecture Center — ACL](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer), Eric Evans, *Domain-Driven Design* (référence conceptuelle).
