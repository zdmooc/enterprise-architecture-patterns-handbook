# Cours 06 — Application Portfolio Rationalization / TIME
**Niveau :** Urbanisation et stratégie de portefeuille | **Progression :** QCM B validé | [Fiche canonique](../06-application-portfolio-rationalization/README.md)

## Objectifs
Évaluer les applications par valeur, santé technique, coût et risque ; utiliser **TIME — Tolerate / Invest / Migrate / Eliminate** ; sécuriser les obligations et dépendances avant tout retrait.

## 1. Le problème
Une banque paie plusieurs licences de reporting de virements SEPA. Deux outils délivrent les mêmes tableaux, mais l'un produit également un fichier nocturne requis pour une obligation métier/réglementaire fictive. La direction demande de le supprimer.

**Le critère « doublon visible » n'est pas une preuve que l'application peut disparaître.** Il faut inventorier les contrats, la conservation des données, les jobs batch et le propriétaire des sorties.

## 2. Comprendre TIME
| Classement | Interprétation | Exemple fictif | Risque à cadrer |
|---|---|---|---|
| **Tolerate** | Maintenir sous contrôle avec réexamen | Core Banking stable, supporté | Dette technique et dépendance |
| **Invest** | Renforcer une capacité stratégique | Service antifraude nécessitant amélioration | Dépense et bénéfice démontré |
| **Migrate** | Remplacer, refondre, replatformer | Moteur Java/JEE à moderniser | Transactions et compatibilité |
| **Eliminate** | Retirer après reprise des usages | Reporting A réellement superflu | Flux oublié, rupture de preuve |

Un classement est **candidat**, non une validation de décommission. L'arbitrage doit réunir métier, propriétaires IT, sécurité, exploitation et finance.

## 3. Matrice de portefeuille illustrative
~~~mermaid
flowchart TB
  INV["Inventaire des applications et coûts"] --> ASS["Mesurer valeur métier, santé, risque et dépendances"]
  ASS --> DEC{"Décision TIME"}
  DEC --> T["T : conserver / réévaluer"]
  DEC --> I["I : investir / démontrer gain"]
  DEC --> M["M : migrer / plan de coexistence"]
  DEC --> E["E : éliminer après reprise et preuve"]
~~~

## 4. Grille d'évaluation argumentée
Pour chaque application, renseigner :
- **Métier** : capacités couvertes, clients et processus affectés, obligations contractuelles et réglementaires.
- **Technique** : support éditeur, obsolescence, incidents, sécurité, accès aux données, disponibilité.
- **Dépendances** : entrées/sorties, batch, rapports, flux MQ/Kafka, consommateur de fichiers, utilisateurs.
- **Économie** : coût complet (licences, RUN, BUILD, migration, double RUN, sortie), budget disponible.
- **Changement** : effort, tests, fenêtres et rollback, preuve d'absence de double traitement.
- **Gouvernance** : décision, sponsor, risk owner, date de revue et critères GO/NO-GO.

Utiliser une échelle explicite et des pondérations approuvées, pas des scores fictifs présentés comme mesurés. Un système très ancien peut être maintenu si le risque de remplacement excède le bénéfice.

## 5. Cas pratique sur notre banque
| Application | Signal | Hypothèse TIME | Condition |
|---|---|---|---|
| Core Banking | Autorité financière, fonctionnement stable | T | Support et PRA vérifiés |
| Moteur Java/JEE | Fin de support du runtime hypothétique | M | Audit WAR/EAR, JNDI, JMS/XA, canary |
| Anti-fraude | Besoin métier prioritaire | I | Gain mesuré, contrôle des faux positifs |
| Reporting A | Données et fonctions redondantes | E possible | Aucune sortie exclusive après reprise |
| Reporting B | Production réglementaire nocturne | T temporaire | Reprise et conservation de la sortie |

## 6. Retirer B : démarche obligatoire
~~~mermaid
flowchart LR
  A["Analyser usages de Reporting B"] --> B["Identifier fichier nocturne unique"]
  B --> C["Qualifier obligation et owner"]
  C --> D["Reprendre le traitement ailleurs"]
  D --> E["Comparer sorties et archives"]
  E --> F{"Non-régression et décommission validés ?"}
  F -->|Oui| G["Retrait progressif"]
  F -->|Non| H["Maintien contrôlé"]
~~~
Évaluer la période de double-run et le coût de suppression, y compris sauvegardes, licences, archivage et opération de repli. Le « zéro logiciel dupliqué » n'est pas une fin en soi.

## 7. Livrables
Registre d'applications ; matrice TIME justifiée ; coût TCO ; heatmap risques ; décisions avec propriétaires et dates ; plans de migration/retrait ; tests de non-régression ; matrice des dépendances et conservation.

## 8. Exercice corrigé
**Question :** supprimer Reporting B, alors qu'il publie aussi un fichier réglementaire. (A) supprimer, (B) analyser fonctions/flux/obligations puis préparer la reprise, (C) conteneuriser puis supprimer.

**Correction : B.** Une rationalisation responsable vérifie la continuité de chaque obligation et fonction critique. Le reclassement E n'est possible qu'après preuve de reprise.

## 9. Entretien
**« Comment construisez-vous une décision TIME ? »** J'associe la valeur métier et la criticité à la santé technique, aux coûts complets et aux risques de sortie ; je documente les dépendances et soumets une trajectoire conditionnelle plutôt qu'un tableau de préférences technologiques.

---

## Cadre et limites
Architecture pédagogique **fictive et anonymisée**, non description d'une banque réelle ni preuve de production. Tous les débits, chiffres, fichiers, indicateurs et interfaces sont illustratifs. Toute décision réelle demande inventaire, approbation métier, analyse de risque, vérification réglementaire et tests. Un accusé HTTP, MQ ou Kafka ne prouve jamais à lui seul le règlement ; l'idempotence doit couvrir l'effet financier et une échéance expirée doit être contrôlée avant toute reprise.
