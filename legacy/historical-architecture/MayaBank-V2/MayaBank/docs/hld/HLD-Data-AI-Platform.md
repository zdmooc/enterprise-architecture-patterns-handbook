# HLD Data/AI Platform

## 1. Objectif

Définir le domaine **Data/AI Platform** de MayaBank comme une extension structurée de la plateforme globale, sans en faire un dépôt séparé.

## 2. Pourquoi ce domaine existe

Le domaine Data/IA sert à couvrir des besoins crédibles d’une banque d’investissement moderne :
- risk analytics ;
- pricing assistance ;
- anomaly detection ;
- search and retrieval interne ;
- enrichissement documentaire et knowledge services ;
- exposition de services d’inférence à des workloads métier.

## 3. Principes d’architecture
- le domaine Data/IA ne doit pas réinventer les services transverses ;
- IAM/SSO, observabilité, secrets, réseau et FinOps doivent rester mutualisés ;
- les workloads Data/IA doivent être pensés avec une discipline stateful / stateless claire ;
- les coûts Data/IA doivent être traçables séparément ;
- les patterns Data/IA doivent rester compatibles avec une lecture OKD puis OpenShift enterprise.

## 4. Composants de référence
- **data-pipelines**
- **vector-database**
- **ml-serving**
- **rag-patterns**
- **analytics workers**
- **feature / metadata patterns** documentés à terme

## 5. Dépendances transverses
- Keycloak pour IAM / SSO / OIDC
- Kong pour exposition API
- Kafka pour événementiel et ingestion
- observability stack pour métriques, logs et alerting
- PostgreSQL / MongoDB comme socles de données complémentaires
- FinOps pour coûts, budgets et showback/chargeback

## 6. Découpage de maturité

### V1
- cadrage du domaine
- composants de référence documentés
- premiers cas d’usage
- hypothèses de coût et de capacité

### V2
- patterns techniques détaillés
- premières hypothèses de déploiement
- observabilité spécifique Data/IA
- intégration plus forte avec Kafka et API management

### V3
- ML serving plus structuré
- vector database patterns plus détaillés
- gouvernance des données et des modèles
- contrôles FinOps renforcés

### V4
- posture enterprise-ready
- auditabilité renforcée
- sécurité et IAM matures
- mapping explicite vers une cible OpenShift / écosystème enterprise

## 7. Risques majeurs
- dérive de périmètre ;
- surcoût observability et stockage ;
- sous-estimation des workloads stateful ;
- flou entre cas d’usage Data/IA et exigences de production réelle.
