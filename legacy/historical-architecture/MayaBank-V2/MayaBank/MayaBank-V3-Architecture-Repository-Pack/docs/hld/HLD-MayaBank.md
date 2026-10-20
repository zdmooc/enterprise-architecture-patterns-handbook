# HLD MayaBank

## 1. Objet

Ce document définit le **High Level Design principal** du dépôt MayaBank.  
Il décrit la cible d’architecture globale, le périmètre du dépôt, les grands domaines couverts, les principes structurants et la trajectoire de maturité.

## 2. Positionnement

MayaBank est un dépôt de référence d’architecture pour une banque d’investissement fictive, construit sur :

- une base **OKD / Kubernetes open source** ;
- une couverture **on-prem + AWS + Azure** ;
- une logique de **lab semi-exécutable** ;
- une trajectoire explicite vers **OpenShift enterprise**.

Le dépôt sert à la fois de :
- support d’apprentissage ;
- support d’architecture ;
- support de démonstration ;
- support de reprise ;
- support de montée en posture d’architecte senior.

## 3. Domaines d’architecture

Les domaines couverts sont :

1. **Platform**
2. **Shared Services**
3. **Business Workloads**
4. **Data / AI Platform**
5. **Security / IAM / Compliance**
6. **FinOps / Governance / Operations**
7. **Architecture Repository & Tooling**

## 4. Nouveau bloc V3 : Architecture Repository & Tooling

À partir de la V3, MayaBank introduit un domaine explicite d’**outillage d’architecture et de repository d’architecture**.

Ce domaine couvre :

- la structuration des documents d’architecture ;
- la traçabilité entre vision, HLD, LLD, ADR, backlog et réalisation ;
- la modélisation cible en **ArchiMate** ;
- la démarche de travail compatible **TOGAF** ;
- le mapping entre outils open source de pratique et outils enterprise.

## 5. Principes directeurs

- garder un **modèle d’architecture commun** entre on-prem, AWS et Azure ;
- distinguer clairement **socle**, **industrialisation**, **posture d’architecte**, **cible enterprise** ;
- relier systématiquement **architecture**, **exploitation** et **coût** ;
- traiter la **Data/IA** comme un domaine structurant et non comme une annexe ;
- faire du dépôt Git un **repository d’architecture simplifié**, lisible et versionné.

## 6. Références liées

- `docs/hld/HLD-Platform.md`
- `docs/hld/HLD-Security.md`
- `docs/hld/HLD-FinOps.md`
- `docs/hld/HLD-Data-AI-Platform.md`
- `docs/hld/HLD-Architecture-Repository-and-Tooling.md`
