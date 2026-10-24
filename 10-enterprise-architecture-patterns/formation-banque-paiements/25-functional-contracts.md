# Cours 25 — Contrats fonctionnels

> **Formation architecture bancaire — parcours fonctionnel.** Banque fictive, virement SEPA de 500 EUR. Aucun SI réel n'est décrit.

## Objectif
**Question d'architecte :** Que doit garantir une fonction à ses consommateurs ?

## 1. Besoin métier
La fonction ContrôlerPlafond reçoit la référence du virement et le montant de 500 EUR, puis retourne sa décision.

## 2. Définition
Le contrat fonctionnel précise préconditions, entrées, sorties, règles, erreurs métier, invariants et sémantique des statuts; il est indépendant du protocole technique.

## 3. Étude de cas détaillée
Contrat ContrôlerPlafond : entrée client identifié, ordre référencé, montant et devise; sortie Autorisé ou RefuséAvecMotif; précondition droits de demande vérifiés; erreur « donnée indisponible » distincte de « plafond dépassé »; date et version de règle.

### Vue de décision
1. **Déclencheur** — Identifier la demande, sa référence, son auteur et la règle applicable.
2. **Contrat** — Décrire les informations d'entrée et de sortie et leur signification métier.
3. **Exécution fonctionnelle** — Faire intervenir la fonction propriétaire de la décision.
4. **Issue** — Distinguer accepté, refusé, transmis, confirmé et à investiguer selon la preuve disponible.
5. **Traçabilité** — Conserver la décision, la version de règle et la provenance des informations nécessaires.

## 4. Garanties et limites
Un résultat absent ne signifie pas refus; la référence d'ordre est stable; le consommateur peut distinguer erreur technique et décision métier.

**Anti-pattern :** Retourner true/false sans motif et faire diverger les significations selon l'application.

## 5. Plan de validation
Tests de contrat : valeur limite, règle en vigueur, données manquantes, répétition et cas où la source du plafond ne répond pas.

**Preuves attendues :** scénarios nominatifs et négatifs, résultat réel comparé au critère, écart documenté et propriétaire de correction. Ne pas confondre disponibilité d'une API avec règlement financier confirmé.

## 6. Exercice de consolidation et corrigé
**À quoi sert le contrat ?**

- **A.** À expliciter les entrées, décisions, exceptions et garanties de la fonction.
- **B.** À fixer obligatoirement le protocole SOAP.
- **C.** À remplacer les règles métier.

**Correction : A.** Le contrat fonctionnel précise préconditions, entrées, sorties, règles, erreurs métier, invariants et sémantique des statuts; il est indépendant du protocole technique. Le choix retenu tient compte de la responsabilité métier et de ses preuves.

## 7. Questions de revue d'architecture
- Qui possède la règle et la donnée faisant foi ?
- Quel état peut-on affirmer avec la preuve disponible ?
- Que se passe-t-il après refus, timeout, doublon ou reprise ?
- Le changement reste-t-il traçable du besoin au test ?

[Retour à l'index](README.md) · [Architecture métier](21-business-architecture-synthesis.md)
