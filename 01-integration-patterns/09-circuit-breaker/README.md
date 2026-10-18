# 09 — Circuit Breaker : prévention des pannes en cascade

## Problème
Un fournisseur de statut ou de paiement devient lent. Les threads, connexions et pools des services appelants se saturent, augmentant la panne. Le **Circuit Breaker** coupe provisoirement les appels vers une dépendance jugée défaillante.

## Machine à états
~~~mermaid
stateDiagram-v2
  [*] --> CLOSED
  CLOSED --> OPEN: Échec/lenteur au-delà du seuil
  OPEN --> HALF_OPEN: Délai écoulé
  HALF_OPEN --> CLOSED: Essais satisfaisants
  HALF_OPEN --> OPEN: Essais insuffisants / KO
~~~

**CLOSED** : appels autorisés et mesurés. **OPEN** : appels bloqués rapidement. **HALF_OPEN** : seulement un petit nombre d'appels pilotes. « Closed » ne signifie pas erreur !

## Exemple de configuration à discuter, pas valeur normative établissement bancaire
- fenêtre glissante : 20 appels ; minimum : 20 ;
- seuil d'échecs : 50 % ; attente OPEN : 30 s ;
- essais HALF_OPEN : 3 ; comptage des exceptions/slow calls à préciser.
La fenêtre d'échantillonnage, le faible débit, les délais de réaction et l'exclusion de certains codes métier doivent être discutés. Un refus « solde insuffisant » ne doit pas être compté comme une panne technique.

## Enchaînement avec les autres protections
**Timeout** borne l'attente ; **Retry** répète parfois ; **Circuit Breaker** limite les appels à une dépendance malade ; **Bulkhead** borne ressources et concurrence. Ordre d'application et budgets doivent éviter un retry storm et des délais cumulés supérieurs au SLO.

~~~mermaid
flowchart LR
  A["Payment API"] --> B["Bulkhead"]
  B --> C["Circuit Breaker"]
  C --> D["Timeout contrôlé"]
  D --> E["Statut bancaire"]
  C -->|OPEN| F["Réponse indisponible / vérification différée"]
~~~

## Politique métier de repli
- **GET statut** : dégradation explicite « temporairement indisponible », sans inventer un résultat.
- **POST création de virement** : si l'appel est bloqué, une erreur technique ou une acceptation durable **prouvée** ; ne pas accepter silencieusement sans avoir conservé l'ordre.
- **Confirmation perdue** : ne jamais transformer timeout/circuit ouvert en REJECTED ni rejouer avec nouvel identifiant.
- **Contrôle antifraude absent** : ne pas accepter implicitement un paiement sans décision validée par les risques et la conformité.

## Exploitation
Compter state transitions, rejected/not-permitted calls, slow calls, failures, p95/p99, saturation, timeouts, disponibilité des dépendances. Tracer circuit name, backend et correlation-id. Isoler les circuits selon *dépendance et type d'opération* ; ne pas faire qu'une panne de reporting bloque les virements.

## Tests à automatiser
1. Injecter 12 erreurs sur 20 appels ; voir OPEN selon configuration.
2. Vérifier refus rapide sans appel au backend.
3. Attendre 30 s, valider nombre d'essais HALF_OPEN.
4. Retour CLOSED uniquement après critères de succès.
5. Vérifier que le circuit OPEN n'entraîne aucun double paiement ni faux statut.
6. Vérifier HA de plusieurs Pods et cohérence de la stratégie de protection (circuit local vs partagé).

## Quand éviter
N'utiliser ni pour erreurs métier normales, ni comme remplacement de l'idempotence, ni comme buffer de messages. Pour protéger un consommateur asynchrone, combiner pause de consommation, backpressure, DLQ/parking et retry maîtrisé.

## Entretien
**Q : est-ce un mécanisme de file d'attente ?** Non. **Q : HALF_OPEN = retour automatique à la normale ?** Non, tests limités. **Q : différence avec Bulkhead ?** Bulkhead isole les ressources concurrentes ; Circuit Breaker refuse les appels selon une politique de santé.

Référence : [Resilience4j Circuit Breaker](https://resilience4j.readme.io/docs/circuitbreaker).

---

## Illustrations complémentaires — simulation des états et saturation

### 20 appels : seuil d'ouverture illustratif
~~~mermaid
flowchart TB
    C["CLOSED : 20 appels observés"]
    C --> K{"Erreurs ?"}
    K -->|"2 / 20 = 10 %"| STAY["Rester CLOSED"]
    K -->|"12 / 20 = 60 %"| O["OPEN : appels refusés rapidement"]
    O -->|"Après 30 secondes"| H["HALF_OPEN : 3 appels de test"]
    H -->|"Tests réussis"| C
    H -->|"Échecs"| O
~~~
Paramètres purement pédagogiques (fenêtre 20, taux 50 %, OPEN 30 s, HALF_OPEN 3). Les erreurs **métier** normales (plafond dépassé, solde insuffisant) ne doivent pas être traitées comme des **pannes techniques** du service.

### Timeout, Retry, Circuit Breaker et Bulkhead
~~~mermaid
flowchart LR
    A["Service appelant"] --> B["Bulkhead : isoler la concurrence"]
    B --> C["Circuit Breaker : autoriser ou refuser"]
    C --> D["Timeout : borner l'attente"]
    D --> E["Dépendance bancaire"]
    C -->|"OPEN"| F["Réponse contrôlée, sans statut financier inventé"]
    D -.->|Échec transitoire + retry permis| R["Retry borné / backoff / jitter"]
    R --> C
~~~
Les retries ne doivent pas multiplier les tentatives au point de dépasser la deadline réglementaire ni créer une nouvelle intention de virement.

### Repli
Pour \`GET statut\`, renvoyer « statut momentanément indisponible ». Pour \`POST paiement\`, ne pas renvoyer « rejeté » alors que la commande a peut-être déjà été exécutée.

