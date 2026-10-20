# LLD Vector Database

## Objet
Décrire le pattern de base pour un stockage vectoriel utilisé par des cas d’usage retrieval / search / RAG interne.

## Cas d’usage MayaBank
- recherche documentaire interne
- support exploitation enrichi
- retrieval pour knowledge services
- recherche de proximité sur documents techniques et contenus réglementaires

## Points d’architecture
- workload stateful
- coût stockage à surveiller
- observabilité dédiée à la croissance de l’index
- sécurité d’accès via IAM / API Gateway selon exposition

## Statut
Documenté en V1, non implémenté en lab à ce stade.
