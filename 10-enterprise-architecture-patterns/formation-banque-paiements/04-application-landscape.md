# Cours 04 — Application Landscape / Cartographie applicative
**Niveau :** Architecture d'entreprise et applicative | **Progression :** QCM B validé | [Fiche canonique](../04-application-landscape/README.md)

## Objectifs
Inventorier le patrimoine applicatif de paiement, relier capacités aux applications, identifier les interfaces, données, contrats, hébergements et propriétaires. Produire une base probante pour le diagnostic d'impact et la migration Java/JEE → OpenShift.

## 1. Cas étudié
Une banque envisage de remplacer son moteur de paiement Java/JEE. Son périmètre réel comprend des fonctions visibles et cachées : API d'initiation, processus batch, messages MQ, retours de rejets, procédures de rapprochement et reporting. **Sans cartographie, une migration peut réussir techniquement et échouer métier.**

| Application / système | Fonction | Technologie hypothétique | Dépendances principales |
|---|---|---|---|
| Portail et mobile | Initier et suivre | Web / mobile | API Gateway / IAM |
| Payment API | Capturer une intention unique | Java | DB ordres, moteur |
| Moteur paiement | Contrôler, orchestrer, suivre | Java/JEE sur VM | Anti-fraude, DB, MQ |
| Service fraude | Évaluer un ordre | Service de décision | Sources de risque |
| Adaptateur Core | Traduire la commande et la réponse | JMS / MQ | Queue Manager, Core |
| Core Banking | Exécution autoritative | Système historique | Comptes, règlement |
| Passerelle SEPA | Échanges externes | Connecteur/rail | Core, interbancaire |
| Notifications | Informer client | Consommateur événementiel | Kafka, canal de notification |
| Reporting | Indicateurs de paiement | Entrepôt ou service | Sources autoritatives et dérivées |

IBM MQ et Kafka sont des **composants d'intégration** ; ils apparaissent dans la cartographie technique, sans être confondus avec des applications métier.

## 2. Carte illustrative des dépendances
~~~mermaid
flowchart TB
  C["Client mobile"] --> GW["API Gateway"]
  GW --> API["Payment API"]
  API --> M["Moteur paiement Java/JEE"]
  M --> F["Service fraude"]
  M --> D[("Base d'intentions / suivi")]
  D --> O["Outbox relay"]
  O --> MQ["IBM MQ"]
  MQ --> AD["Adaptateur Core"]
  AD --> CORE["Core Banking"]
  CORE --> SEPA["Passerelle SEPA"]
  D --> EV["Relais événements"]
  EV --> K["Kafka"]
  K --> N["Notifications / reporting"]
~~~
Cette vue décrit des relations logiques, **pas** une chronologie exacte ni une affirmation de déploiement réel.

## 3. Une fiche d'application exploitable
Chaque entrée d'inventaire doit comporter au minimum :
- **Identité** : nom unique, responsable métier, responsable IT, criticité, statut de cycle de vie.
- **Fonctions** : capacités et processus servis, opérations critiques, échéances.
- **Interfaces** : émetteur/destinataire, direction, protocole, contrat, version, volume, mode de reprise.
- **Données** : lecture/écriture, système autoritatif, rétention, classification et destinataires.
- **Technique** : runtime Java, serveur JEE, EJB/JNDI/JMS, dépendances XA, DB, hébergement, OS, réseau et certificats.
- **Opération** : SLO, incidents, exploitation, RTO/RPO validés, tests, licence/support, fin de vie et coûts.
- **Preuve** : configuration, traces et inventaire validés, date, propriétaire de la preuve.

Exemple : « PAYMENT.REQUEST » n'est pas une simple flèche ; c'est un contrat versionné, une queue, une population de producteurs/consommateurs, des droits, une corrélation et une politique de redélivrance.

## 4. Analyse d'impact avant migration
~~~mermaid
flowchart LR
  A["Changer le moteur Java/JEE"] --> B["Identifier les appels entrants"]
  A --> C["Identifier les sorties et effets"]
  B --> D["API, fichiers, batch, MQ"]
  C --> E["Core, DB, événements, notifications"]
  D --> F["Contrats et tests"]
  E --> F
  F --> G["Analyse risques, coûts et cutover"]
~~~

Distinguer **application** (fonction logique), **instance** (exécution), **environnement** (dev/preprod/prod) et **composant technique** (broker, DB, cluster).

## 5. Démarche pratique
1. Partir des capabilities et collecter CMDB/inventaires, schémas, WAR/EAR, interfaces et contrats.
2. Confronter inventaire déclaratif aux faits : logs, métriques, appels réseau, MQ, tâches planifiées.
3. Valider chaque dépendance P0 avec métier, propriétaires et exploitation.
4. Identifier objets autoritatifs, flux de retour, batch et usages hors horaires.
5. Réaliser une matrice d'impact entrée/sortie, lister hypothèses et inconnues.
6. Planifier tests de non-régression et stratégie de coexistence avant de modifier la topologie.

## 6. Risques à démontrer
- Flux batch nocturne absent de la cartographie → arrêt du traitement réglementaire.
- Driver JDBC/JNDI ou transactions XA non compatibles sous nouveau runtime → panne silencieuse.
- Message MQ consommé deux fois après redémarrage → effet financier dupliqué si Core non idempotent.
- Passerelle SEPA dépend d'une version implicite d'interface → rejet interbancaire.

## 7. Livrables
Carte C4 ou ArchiMate (applicative) ; portefeuille et owners ; matrice applications–capacités ; catalogue d'interfaces ; registre des dépendances P0 ; carte des données maîtresses ; cartographie AS-IS datée ; dossier d'impact.

## 8. Exercice corrigé
**Question :** migrer un moteur Java/JEE vers OpenShift dont MQ, Core et batch sont partiellement documentés. (A) conteneuriser immédiatement, (B) inventorier toutes les dépendances, (C) remplacer MQ par Kafka.

**Correction : B.** Le diagnostic et la preuve d'exhaustivité sont des prérequis. Kubernetes n'efface pas les couplages du legacy.

## 9. Entretien
**« À quoi sert l'Application Landscape ? »** À visualiser les responsabilités applicatives et à rendre vérifiable l'impact d'une transformation, y compris les dépendances cachées.

---

## Cadre et limites
Architecture pédagogique **fictive et anonymisée**, non description d'une banque réelle ni preuve de production. Tous les débits, chiffres, fichiers, indicateurs et interfaces sont illustratifs. Toute décision réelle demande inventaire, approbation métier, analyse de risque, vérification réglementaire et tests. Un accusé HTTP, MQ ou Kafka ne prouve jamais à lui seul le règlement ; l'idempotence doit couvrir l'effet financier et une échéance expirée doit être contrôlée avant toute reprise.
