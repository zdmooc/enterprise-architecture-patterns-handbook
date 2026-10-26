# Cahier de révision — cours 63 à 73 · Les 11 GoF comportementaux

> Fiches de référence et corrigés théoriques des exercices. **Aucun des 11 exercices individuels de cette série n'est encore validé en session** ; le cours 63 avait déjà été présenté oralement, sans réponse à son exercice.

| Cours | Pattern | Réponse corrigée | Preuve d'architecture attendue |
|---:|---|:---:|---|
| 63 | [Chain of Responsibility](../63-chain-of-responsibility.md) | **B** | Ordre conforme : chaque contrôle obligatoire est appelé exactement une fois. |
| 64 | [Command](../64-command.md) | **A** | Commande valide : même contrat, statut retourné inchangé. |
| 65 | [Interpreter](../65-interpreter.md) | **A** | Montant sous le plafond et devise EUR : vrai. |
| 66 | [Iterator](../66-iterator.md) | **B** | Collection vide : `hasNext()` est faux. |
| 67 | [Mediator](../67-mediator.md) | **B** | Montant invalide : bouton désactivé. |
| 68 | [Memento](../68-memento.md) | **B** | Sauvegarder puis modifier : restore retrouve les champs du brouillon. |
| 69 | [Observer](../69-observer.md) | **B** | État réellement modifié : chaque abonné local reçoit la notification. |
| 70 | [State](../70-state.md) | **C** | Brouillon : opération de modification admise et montant valide. |
| 71 | [Strategy](../71-strategy.md) | **A** | Deux produits : politiques distinctes et sélection correcte. |
| 72 | [Template Method](../72-template-method.md) | **B** | Format invalide : étape de soumission jamais atteinte. |
| 73 | [Visitor](../73-visitor.md) | **B** | SEPA : la bonne surcharge de `visit` est appelée. |

## Comparatif des choix
- **Chain of Responsibility** : répartir les contrôles sur plusieurs handlers.
- **Command** : encapsuler l'intention d'une action.
- **Interpreter** : évaluer une grammaire et des expressions contrôlées.
- **Iterator** : parcourir sans dévoiler le stockage.
- **Mediator** : coordonner des objets entre eux sans dépendances croisées.
- **Memento** : restaurer un brouillon, jamais un règlement.
- **Observer** : notifier localement des objets, pas de garantie Kafka/MQ.
- **State** : comportement et transitions guidés par l'état d'un ordre.
- **Strategy** : sélectionner une famille d'algorithmes.
- **Template Method** : définir un squelette stable avec hooks.
- **Visitor** : déporter une opération applicable à des classes stables.

## Trois questions de synthèse (corrigés inclus)
**1. Comment éviter qu'une opération non autorisée soit exécutée sur un ordre accepté ?**
A. Memento ; **B. State** ; C. Iterator. **Réponse B** : les transitions autorisées appartiennent aux règles métier de l'agrégat et à l'état.

**2. Un tableau de bord local doit recevoir un signal après un changement d'état validé.** A. Memento ; B. Interpreter ; **C. Observer**. **Réponse C** : publication in-process best effort après commit ; pour une livraison distribuée fiable, Outbox et broker.

**3. Comment appliquer différentes politiques de tarification pour plusieurs produits ?** **A. Strategy** ; B. Iterator ; C. Visitor. **Réponse A** : même interface de calcul, algorithmes interchangeables et tarifs versionnés.

## Précautions bancaires communes
Le fait de transmettre une commande ou un événement ne signifie pas qu'un virement est réglé. Un timeout ne prouve pas l'absence d'effet. Les contrôles de concurrence, idempotence, autorité financière, conformité et reprise après incident doivent être traités explicitement au-delà des patterns objets GoF.

[Programme de formation](../README.md) · [Cours 59–62](cours-59-62.md)
