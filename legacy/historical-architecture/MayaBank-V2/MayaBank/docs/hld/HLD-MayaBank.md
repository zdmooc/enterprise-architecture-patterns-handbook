# HLD MayaBank

## 1. Résumé exécutif

MayaBank est une architecture de référence pour une banque d’investissement fictive spécialisée dans les produits dérivés financiers.

La cible de départ repose sur une base **OKD / Kubernetes open source**, déclinée sur **on-prem, AWS et Azure**, avec une trajectoire explicite vers une cible **OpenShift enterprise**.

L’architecture est organisée en cinq plans :
- **platform**
- **shared services**
- **business workloads**
- **data-ai**
- **governance / FinOps / operations**

## 2. Objectifs du HLD
- définir la cible d’architecture globale ;
- structurer le dépôt ;
- clarifier les rôles des composants ;
- séparer ce qui est actuel, semi-exécutable et cible future ;
- servir de point d’entrée aux LLD.

## 3. Périmètre couvert

### Inclus
- topologie logique globale
- workloads majeurs
- shared services
- IAM/SSO
- data & stateful
- data/IA platform
- observabilité
- FinOps
- gouvernance
- mapping OKD → OpenShift enterprise

### Hors périmètre immédiat
- sizing détaillé de production
- contrat d’exploitation réel
- contraintes réglementaires exhaustives
- automatisation complète du build lab
- MLOps complet de niveau production

## 4. Vue logique

### 4.1 Platform layer
- cluster baseline
- ingress / exposure
- policy baseline
- quotas / namespaces
- observability hooks

### 4.2 Shared services layer
- Keycloak
- Kong
- Kafka
- shared observability
- secrets pattern

### 4.3 Business layer
- ODM
- Pega
- portals
- batch
- business APIs

### 4.4 Data layer
- PostgreSQL
- MongoDB

### 4.5 Data/AI layer
- data pipelines
- vector database patterns
- ML serving patterns
- retrieval / RAG patterns
- analytics workers
- AI governance and cost controls

## 5. Découpage on-prem / AWS / Azure

Le modèle d’architecture doit rester stable.
Les providers ne doivent introduire que des écarts d’implémentation :
- réseau
- compute
- load balancing
- stockage
- exposition
- services de données et capacités associées

## 6. Différenciation stateful / stateless

### Stateless
- client-portal-web
- business APIs
- certains composants front ou workers éphémères
- certains services d’inférence ou d’enrichissement data/IA

### Stateful
- PostgreSQL
- MongoDB
- Kafka
- portal session si persistance embarquée
- certains composants Pega / ODM selon pattern retenu
- vector database selon le pattern choisi

## 7. Sécurité et IAM

La sécurité est intégrée au HLD à travers :
- fédération d’identité ;
- secrets management ;
- segmentation réseau ;
- policy baseline ;
- audit logging ;
- compliance baseline progressive ;
- protection des flux data et IA.

## 8. Observabilité

L’observabilité doit couvrir :
- métriques plateforme ;
- métriques workloads ;
- logs techniques ;
- événements d’exploitation ;
- indicateurs FinOps liés à la consommation ;
- signaux spécifiques Data/IA : volume de données, coûts de pipelines, latence d’inférence, croissance du stockage vectoriel.

## 9. FinOps

Le HLD intègre un axe FinOps :
- showback / chargeback ;
- budgets par environnement ;
- coût par domaine ;
- coût des workloads stateful ;
- coût observability vs valeur ;
- coût du domaine Data/IA.

## 10. Roadmap de maturité

- **V1** : architecture crédible et dépôt structuré
- **V2** : industrialisation initiale
- **V3** : plateforme avancée
- **V4** : enterprise-ready

## 11. Critères de réussite

Le dépôt est considéré réussi si :
- il peut être lu dans un ordre logique ;
- il permet de reprendre le chantier plus tard ;
- les décisions majeures sont traçables ;
- le lien entre architecture, exploitation et coût est visible ;
- le domaine Data/IA est intégré sans casser la cohérence globale.
