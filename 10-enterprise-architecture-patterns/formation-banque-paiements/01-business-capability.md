# Cours 01 — Business Capability Mapping
**Niveau :** Architecture métier / urbanisation | **Statut :** cours étudié, QCM corrigé B | **Référence :** [pattern 01](../01-business-capability-mapping/README.md)

## Objectifs pédagogiques
- Distinguer **capacité métier**, processus, domaine, organisation et application.
- Construire une carte des capacités de paiement indépendante des choix Java, MQ ou OpenShift.
- Mesurer la criticité, les redondances et la couverture applicative avant toute rationalisation.

## 1. Question d'architecture
Une banque découvre trois applications dites « de virements SEPA ». Peut-elle en supprimer deux ? **Pas avant d'avoir cartographié les capacités réellement servies.** Une capacité exprime *ce que la banque doit savoir faire* (par exemple gérer des ordres de virement), pas comment elle le fait ni quel logiciel elle achète.

| Notion | Exemples sur le paiement | Erreur fréquente |
|---|---|---|
| Capacité métier | Initier, vérifier, autoriser, exécuter, suivre et rapprocher | Confondre capacité avec étape technique |
| Processus | Saisir → contrôler → traiter → informer | Confondre déroulement et aptitude durable |
| Domaine | Clients, Comptes, Paiements, Fraude, Interbancaire | Prendre un organigramme pour un domaine |
| Application | Portail, moteur de paiement, reporting | Appeler une application « capacité » |
| Plateforme | IBM MQ, Kafka, OpenShift | Faire entrer une technologie dans la carte métier |

## 2. Carte de capacités de notre banque fictive
~~~mermaid
flowchart TB
  P["Domaine Paiements : rendre possible un transfert de fonds"]
  P --> IN["Initier un ordre"]
  P --> VE["Vérifier bénéficiaire et admissibilité"]
  P --> AU["Contrôler et autoriser"]
  P --> EX["Acheminer / faire exécuter"]
  P --> ST["Suivre les statuts et incidents"]
  P --> RE["Réconcilier et justifier"]
  EX -. "Dépend de" .-> CO["Domaine Comptes / Core Banking"]
  AU -. "Contribue" .-> FR["Domaine Fraude"]
  EX -. "Dépend de" .-> IB["Domaine Interbancaire"]
~~~

Pour les virements SEPA et SCT Inst, certaines capacités sont partagées, mais les délais et règles peuvent différer. Les cartes peuvent être décomposées en niveaux L1 (gérer les paiements), L2 (initier/contrôler/exécuter) et L3 (contrôle des limites, validation du bénéficiaire, retour de statut, etc.).

## 3. Faire la matrice capacité × application
| Capacité | Appli A — Saisie | Appli B — Exécution | Appli C — Suivi |
|---|---|---|---|
| Recevoir la demande | Responsable | Consomme l'ordre | Lecture |
| Appliquer les contrôles | Partiels | Complémentaires | Aucun |
| Soumettre à l'exécution | Non | Responsable | Non |
| Traiter les retours et rejets | Affiche | Référence / statut | Consolide |
| Réconcilier | Non | Source de suivi | Analyse |

**Lecture senior :** A, B et C semblent similaires par leur étiquette « paiement » mais peuvent porter des capacités complémentaires. La suppression de C doit vérifier l'obligation d'audit et les consommateurs de ses rapports, pas seulement le coût de licence.

## 4. Démarche en mission
1. Identifier objectifs métier, sponsor, vocabulaire, périmètre de produits et rails (SCT, SCT Inst, cartes, prélèvements).
2. Construire L1 → L2 → L3 lors d'ateliers métier et de revue documentaire.
3. Rattacher processus et applications à chaque capacité ; documenter *observé / déclaré / à confirmer*.
4. Scorer séparément **importance métier**, maturité, criticité, risque, conformité et coût, selon une grille publiée.
5. Détecter capacités non couvertes et solutions redondantes ; ne pas inférer qu'une redondance logicielle est inutile.
6. Décider des études prioritaires ; nommer propriétaire, preuve, date de revue et trajectoire.

## 5. Risques et contre-exemples
- Supprimer une application de reporting qui produit encore une déclaration réglementaire cachée : revue des flux et exigences de conservation requise.
- Confondre deux capacités « exécuter » : instruction interne et règlement interbancaire n'ont pas la même autorité.
- Dessiner les équipes au lieu des capacités : une réorganisation rend la carte obsolète.
- Mettre « Kafka » dans le niveau L2 de cartographie métier : il s'agit d'un choix de réalisation.

## 6. Livrables
Carte hiérarchique L1/L2/L3 ; dictionnaire des capacités ; matrice capacités ↔ applications ↔ processus ; heatmap valeur/risque ; liste des hypothèses ; plan de validation métier ; registre de dépendances.

## 7. Exercice corrigé
**Situation :** A saisit un ordre, B le transmet au Core Banking, C produit des retours obligatoires. Peut-on ne conserver qu'une application au motif que les trois « font du SEPA » ?

**A** Choisir immédiatement une application plus récente.  
**B** Cartographier capacités, fonctions et dépendances.  
**C** Conteneuriser les trois d'abord.

**Correction : B.** L'inventaire fonctionnel et métier précède la décision de rationalisation. *Condition GO :* chaque capacité critique reste couverte, avec propriétaire et test de non-régression.

## 8. Questions d'entretien
- **Pourquoi une capability map ne mentionne-t-elle pas IBM MQ ?** Parce qu'elle décrit le métier indépendamment de l'implémentation.
- **Comment prouver la valeur de la carte ?** Elle permet de repérer une capacité critique sans propriétaire, d'analyser l'impact d'un retrait et de prioriser les investissements.
- **Quel lien avec TOGAF/ArchiMate ?** Les capacités et leurs relations forment une vue métier réutilisable pour relier stratégie, processus, applications et feuille de route.

---

## Cadre de l'étude
Cas **fictif et anonymisé** : une banque imaginaire modernise des services de virements SEPA et instantanés. Aucun SI client réel, flux propriétaire, métrique mesurée ou conformité certifiée n'est revendiqué. Les identifiants, seuils et composants sont des hypothèses pédagogiques. Les obligations de chaque scheme de paiement, licences et NFR doivent être vérifiés avant usage réel.

**Fil rouge :** virement de 500 EUR, référence métier immuable VIR-001. Un ACK réseau/MQ ne prouve jamais un règlement ; seul le système financier/rail autoritatif permet de conclure. Un timeout ne prouve pas un échec. Les reprises nécessitent idempotence, preuve et respect de l'échéance de l'ordre.
