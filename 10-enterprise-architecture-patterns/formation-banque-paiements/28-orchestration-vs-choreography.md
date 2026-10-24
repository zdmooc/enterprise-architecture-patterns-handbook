# Cours 28 — Orchestration et chorégraphie

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Quand choisir un pilote central ou une coordination par événements ?

## 1. Besoin métier
Après validation d'un paiement, plusieurs fonctions peuvent intervenir : transmission, suivi, notification et rapprochement.

## 2. Définition
L'orchestration utilise un coordinateur explicite. La chorégraphie relie des participants autonomes par événements et leurs réactions, sans pilote central du flux complet.

## 3. Étude de cas détaillée
Choix illustratif : garder une orchestration claire pour un traitement nécessitant une séquence d'autorisation; utiliser des événements « OrdreAccepté » pour déclencher la notification et d'autres consommateurs non critiques. Établir qui possède l'état global et comment diagnostiquer.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Un événement signifie un fait constaté; des consommateurs peuvent être retardés ou recevoir des doublons; la cohérence du paiement ne dépend pas de la réception de la notification.

**Anti-pattern :** Faire une chorégraphie opaque où personne ne peut expliquer le statut global; transformer chaque interaction en appel synchrone.

## 5. Plan de validation
Simuler consommateur de notification indisponible, doublon, délais et réordonnancement; vérifier que le traitement financier reste correct.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Quel énoncé est correct ?**

- **A.** Orchestration = coordinateur; chorégraphie = réactions distribuées aux événements.
- **B.** Les deux imposent un moteur BPM unique.
- **C.** La chorégraphie assure automatiquement l'exactly-once financier.

**Correction : A.** L'orchestration utilise un coordinateur explicite. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
