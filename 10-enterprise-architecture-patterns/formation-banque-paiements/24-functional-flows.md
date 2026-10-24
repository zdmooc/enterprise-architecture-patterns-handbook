# Cours 24 — Flux fonctionnels

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Comment les fonctions se transmettent-elles des informations ?

## 1. Besoin métier
Pour notre virement de 500 EUR, RéceptionOrdre fournit les données à Contrôle, puis PilotageTraitement attend une décision.

## 2. Définition
Un flux fonctionnel décrit information, émetteur, récepteur, sens, déclencheur et signification; il n'impose ni REST, ni MQ, ni Kafka.

## 3. Étude de cas détaillée
Schéma fonctionnel : RéceptionOrdre → ContrôleÉligibilité (ordre, identité); ContrôleÉligibilité → PilotageTraitement (accepté/refusé + motif); PilotageTraitement → Suivi (référence, progression); RésultatExterne → Rapprochement (preuve). Documenter échanges synchrones ou différés uniquement si la sémantique l'exige.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Chaque flux porte une référence stable; un accusé technique n'est pas un résultat métier; les données sensibles sont minimisées.

**Anti-pattern :** Prendre un HTTP 200 pour une confirmation de règlement; cacher le traitement asynchrone.

## 5. Plan de validation
Simuler refus, demande identique répétée et confirmation retardée; tracer quel flux porte la preuve.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Quel est un flux fonctionnel ?**

- **A.** Une adresse IP entre deux serveurs.
- **B.** Une table SQL nommée flux.
- **C.** Un échange d'informations défini entre deux fonctions avec signification métier.

**Correction : C.** Un flux fonctionnel décrit information, émetteur, récepteur, sens, déclencheur et signification; il n'impose ni REST, ni MQ, ni Kafka. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
