# Backlog and Design Authority Process

## 1. Objet

Ce document décrit la relation entre :
- l’architecture ;
- le backlog ;
- les sprints ;
- la revue d’architecture ;
- la design authority.

## 2. Principe

Le backlog ne doit pas devenir la seule mémoire des décisions.  
Les décisions d’architecture doivent être stabilisées dans le repository avant d’être simplement “consommées” par les sprints.

## 3. Flux de travail

### Cas 1 — changement mineur
- analyse
- mise à jour LLD si nécessaire
- backlog
- sprint

### Cas 2 — changement structurant
- analyse
- HLD impacté
- ADR
- backlog
- sprint
- mise à jour des risques si besoin

### Cas 3 — arbitrage transverse
- atelier
- proposition
- ADR
- décision en design authority
- déclinaison backlog

## 4. Design Authority dans MayaBank

MayaBank simule une **Design Authority** simplifiée à travers :
- `docs/governance/Architecture-Review-Checklist.md`
- `docs/governance/Design-Authority-Pack.md`
- `docs/governance/Decision-Log.md`
- `docs/adr/`

## 5. Objectif pédagogique

Ce processus sert à apprendre une posture :
- d’architecte qui décide ;
- d’architecte qui trace ses arbitrages ;
- d’architecte qui relie architecture et exécution.
