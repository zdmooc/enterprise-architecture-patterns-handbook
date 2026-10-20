# Capacity and Cost Model

## Objectif
Mettre en regard capacité, criticité, HA, stockage, observabilité et coût.

## Dimensions
- CPU / memory requests
- storage size and class
- network egress
- log ingestion and retention
- environment tier
- resilience target
- data volume growth
- vector storage growth
- pipeline runtime cost
- inference / serving cost hypotheses

## Lecture Data/IA
Le domaine Data/IA impose une discipline spécifique :
- distinguer coût d’infrastructure et coût de traitement ;
- surveiller l’explosion du stockage et des logs ;
- comparer coût d’un pipeline batch vs coût d’un service d’inférence ;
- relier chaque capacité Data/IA à un centre de coût métier.
