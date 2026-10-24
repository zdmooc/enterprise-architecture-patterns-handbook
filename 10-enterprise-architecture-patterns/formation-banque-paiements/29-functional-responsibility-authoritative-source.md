# Cours 29 — Responsabilités et source autoritative

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Qui possède une décision et quelle source fait foi ?

## 1. Besoin métier
Le canal bancaire affiche « ordre accepté » tandis que le système financier n'a pas encore confirmé le règlement.

## 2. Définition
La source autoritative est le système ou domaine légitime pour attester un fait donné. Il peut exister une source différente pour l'ordre, le solde, le résultat externe et la notification.

## 3. Étude de cas détaillée
Attribuer à la fonction Paiements l'état d'instruction, au domaine TenueDeCompte les écritures dont il est responsable et au mécanisme de rapprochement la confirmation obtenue selon le contrat externe. Exposer le degré de certitude dans le suivi client.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Une vue matérialisée n'est pas automatiquement source de vérité; le propriétaire de l'état est explicite; les copies ont une politique de fraîcheur.

**Anti-pattern :** Déduire la confirmation du paiement depuis l'état d'une notification, ou permettre à un consommateur de réécrire un statut autoritatif.

## 5. Plan de validation
Tester deux statuts contradictoires, copie ancienne, confirmation retardée et erreur d'identifiant de rapprochement.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**Quelle information doit l'emporter en cas de contradiction ?**

- **A.** Celle affichée en premier dans l'interface.
- **B.** La source autoritative définie pour le fait métier concerné.
- **C.** Celle qui arrive sur le dernier événement, quel qu'il soit.

**Correction : B.** La source autoritative est le système ou domaine légitime pour attester un fait donné. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
