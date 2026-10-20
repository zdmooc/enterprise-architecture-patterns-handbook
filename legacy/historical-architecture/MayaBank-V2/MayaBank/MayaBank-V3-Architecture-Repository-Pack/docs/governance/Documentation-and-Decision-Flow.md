# Documentation and Decision Flow

## 1. Objet

Ce document décrit comment les artefacts du dépôt MayaBank s’enchaînent pour former un **flux de décision d’architecture** cohérent.

## 2. Flux cible

1. **Vision**
2. **Principes**
3. **HLD**
4. **ADR**
5. **LLD**
6. **Roadmap / Sprint**
7. **Implémentation semi-exécutable**
8. **Runbooks / evidence**
9. **Mise à jour des risques et dettes**

## 3. Rôle de chaque couche

### Vision
Décrit le pourquoi métier, la cible et les capacités.

### HLD
Décrit les blocs d’architecture, leurs responsabilités et les frontières principales.

### ADR
Décrit les décisions structurantes et leurs justifications.

### LLD
Décrit les choix détaillés d’implémentation et de design.

### Roadmap / Sprint
Décrit l’ordre de réalisation, la priorisation et le niveau de maturité.

### Runbooks / Evidence
Décrivent comment opérer, vérifier, prouver et reprendre.

## 4. Règle forte

Un détail technique ne doit pas apparaître uniquement dans le backlog s’il modifie la cible d’architecture.  
Dans ce cas :
- mise à jour HLD ou LLD ;
- ADR si arbitrage ;
- puis backlog.

## 5. Résultat recherché

Le dépôt doit permettre à un lecteur de comprendre :
- ce qui est voulu ;
- ce qui a été décidé ;
- ce qui doit être fait ;
- ce qui reste à arbitrer.
