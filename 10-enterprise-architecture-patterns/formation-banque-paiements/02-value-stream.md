# Cours 02 — Value Stream Mapping
**Niveau :** Architecture métier | **Statut :** cours étudié, QCM corrigé B | **Référence :** [pattern 02](../02-value-stream-mapping/README.md)

## Objectifs
Comprendre la valeur livrée au client, distinguer temps de traitement et temps d'attente, attribuer chaque étape à une capacité métier et localiser les frictions avant d'optimiser un produit technique.

## 1. Cas bancaire : virement instantané fictif de 500 EUR
Un client demande l'envoi de 500 EUR. La valeur est obtenue quand le résultat financier est établi et correctement communiqué, pas simplement quand l'API répond ou que le message est accepté par MQ.

| Étape | Résultat métier recherché | Temps simulé | Capacité | Responsable à confirmer |
|---|---|---:|---|---|
| 1. Initier | Ordre capturé avec consentement requis | 0,2 s | Initiation | Canaux |
| 2. Contrôler | Vérifications et décisions effectuées | 0,5 s | Autorisation | Paiements / Fraude |
| 3. Attendre | Aucun progrès métier : ordre en attente | 3,0 s | Exécution | Exploitant / domaine Paiements |
| 4. Traiter | Instruction exécutée, résultat à confirmer | 0,7 s | Exécution | Core / Interbancaire |
| 5. Informer | Statut communiqué sur preuve métier | 0,3 s | Suivi | Paiements |
| **Total** | **Délai fictif bout-en-bout** | **4,7 s** | | |

**3,0 / 4,7 s ≈ 64 %** du parcours sont absorbés par une attente hypothétique. Cela justifie une enquête, **pas** une conclusion automatique que MQ est trop lent.

## 2. Vue de parcours de valeur
~~~mermaid
flowchart LR
  A["Demande client"] --> B["Contrôles / décision"]
  B --> C["Attente identifiée"]
  C --> D["Exécution / interbancaire"]
  D --> E["Résultat attesté et information"]
  C -. "Friction à mesurer" .-> X["Queue depth, âge message, workers, DB, aval"]
~~~

## 3. Une value stream n'est pas une séquence technique
- **Value stream** : valeur, acteurs, étapes, attentes, métriques et irritants.
- **BPMN** : logique détaillée du processus, décisions et exceptions.
- **UML Sequence** : appels entre composants.
- **Distributed trace** : chronologie d'exécution effectivement observée.
L'architecte les relie sans les confondre. Pour une latence de bout en bout, il croise mesures applicatives, MQ et Core Banking, avec des identifiants de corrélation sûrs.

## 4. Démarche terrain
1. Fixer le **point de départ** (action client acceptée) et le **point d'arrivée** (preuve de résultat + information).
2. Décrire le parcours nominal et les parcours « rejet », « issue inconnue », « retour interbancaire ».
3. Collecter des durées réelles p50/p95/p99, délais en file, reprises, distribution par produit/heure.
4. Repérer délais sans valeur, reprises manuelles et doubles saisies.
5. Relier chaque friction à sa capacité, son owner, son système et ses flux.
6. Comparer options de traitement, risques et gains ; piloter une expérience mesurée.
7. Vérifier que l'amélioration locale ne dégrade pas la fiabilité ou les obligations du scheme.

## 5. Scénarios de panne et arbitrages
| Observation | Hypothèses à tester | Ce qu'il ne faut pas faire |
|---|---|---|
| Âge des messages augmente | Consommateur bloqué, charge, Core lent | Remplacer MQ sans mesure |
| API lente | DB verrouillée, appels synchrones, saturation | Ajouter des pods sans vérifier le goulot |
| Réponse métier perdue | Réseau, adaptateur, consommateur | Afficher REJECTED sans preuve |
| Kafka lag élevé | Abonné lent, partitionnement, panne | Assimiler retard reporting à échec financier |

**KPI utiles :** délai bout en bout mesuré, p99, taux d'issue UNKNOWN, temps de réconciliation, taux de paiements sans statut confirmé, incidents par rail.

## 6. Livrables
Carte de valeur AS-IS / cible ; mesures et sources ; registre des irritants ; owners des étapes ; métriques de référence ; scénario avant/après ; hypothèses et budget de latence à négocier.

## 7. Exercice corrigé
**Question :** 3 secondes sont perdues avant exécution. Faut-il (A) remplacer MQ, (B) mesurer le temps d'attente et déterminer la cause, (C) ajouter des pods ?

**Correction : B.** La capacité aval peut être saturée, une transaction SQL peut bloquer, ou les consommateurs peuvent manquer de ressources. Un changement technologique n'est défendable qu'après attribution, mesures et tests comparatifs.

## 8. Entretien senior
**Q : « Comment démontrez-vous la valeur du Value Stream Mapping ? »**  
**R :** « Je pars de l'expérience du client, décompose le parcours en étapes et temps d'attente, mesure les points de friction, rattache leurs causes aux capacités et aux responsables, puis valide les gains sans sacrifier les garanties financières. »

---

## Cadre de l'étude
Cas **fictif et anonymisé** : une banque imaginaire modernise des services de virements SEPA et instantanés. Aucun SI client réel, flux propriétaire, métrique mesurée ou conformité certifiée n'est revendiqué. Les identifiants, seuils et composants sont des hypothèses pédagogiques. Les obligations de chaque scheme de paiement, licences et NFR doivent être vérifiés avant usage réel.

**Fil rouge :** virement de 500 EUR, référence métier immuable VIR-001. Un ACK réseau/MQ ne prouve jamais un règlement ; seul le système financier/rail autoritatif permet de conclure. Un timeout ne prouve pas un échec. Les reprises nécessitent idempotence, preuve et respect de l'échéance de l'ordre.
