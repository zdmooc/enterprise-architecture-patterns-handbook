# MayaBank Vision

## 1. Objet

MayaBank est une banque d’investissement fictive utilisée comme support de travail pour concevoir un dépôt d’architecture, de gouvernance, de lab semi-exécutable et de pilotage FinOps.

Le but n’est pas de simuler toute la finance de marché, mais de représenter un **contexte crédible** dans lequel on retrouve les contraintes qui intéressent un architecte plateforme senior :
- workloads critiques ;
- exigences de sécurité et de traçabilité ;
- arbitrages stateful vs stateless ;
- exposition API ;
- intégration IAM/SSO ;
- besoins batch et flux événementiels ;
- coûts, capacité, résilience et gouvernance ;
- montée vers une **plateforme data/IA** maîtrisée.

## 2. Ambition

Ce dépôt doit permettre de progresser depuis :
- une bonne compréhension du socle Kubernetes / OKD ;
- vers une posture d’architecte capable de raisonner comme sur une cible OpenShift enterprise ;
- avec une extension naturelle vers des problématiques **Data Platform / AI Platform**.

## 3. Positionnement

MayaBank est :
- un dépôt de **référence pédagogique sérieuse** ;
- un support d’**entretien / comité d’architecture** ;
- un support d’**industrialisation progressive** ;
- un support de **montée en compétences Data/IA** dans un cadre bancaire.

MayaBank n’est pas :
- une vraie plateforme de production ;
- un produit bancaire réel ;
- un dépôt limité à du YAML technique sans cadre d’architecture.

## 4. Axes de valeur

- clarté de la trajectoire
- cohérence HLD / LLD / ADR / runbooks / FinOps
- différenciation nette entre actuel, semi-exécutable et cible future
- capacité à reprendre le chantier dans le temps
- intégration cohérente du domaine **Data/IA** sans casser le modèle plateforme

## 5. Pourquoi une plateforme Data/IA dans MayaBank

Une banque d’investissement moderne ne traite plus Data/IA comme un sujet annexe.

Dans MayaBank, le domaine Data/IA sert à simuler des cas d’usage crédibles :
- **risk analytics** ;
- **pricing assistance** ;
- **anomaly / fraud detection** ;
- **reporting enrichi** ;
- **knowledge retrieval** pour support, exploitation et documentation ;
- **RAG interne** pour capitaliser sur la connaissance applicative et d’exploitation.

Le domaine Data/IA est volontairement intégré au même dépôt parce qu’il dépend fortement de :
- Kafka ;
- IAM/SSO ;
- observabilité ;
- stockage ;
- sécurité ;
- FinOps ;
- gouvernance des environnements.

## 6. Vision cible

À terme, MayaBank doit représenter une plateforme cohérente où coexistent :
- des workloads métier critiques ;
- des services partagés ;
- des composants stateful ;
- des flux événementiels ;
- un domaine data/IA maîtrisé ;
- une gouvernance d’architecture et de coûts lisible.
