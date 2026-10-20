# HLD Integration and Eventing

## Objectif
Décrire les échanges, l’exposition API et le backbone événementiel de MayaBank.

## Composants
- Kong API Gateway
- Kafka event backbone
- APIs métier
- batch interfaces
- Data/IA ingestion and enrichment flows

## Point Data/IA
Le domaine Data/IA dépend fortement de Kafka et des patterns d’ingestion. Les pipelines d’enrichissement et de restitution doivent être pensés comme des consommateurs et producteurs de services transverses.
