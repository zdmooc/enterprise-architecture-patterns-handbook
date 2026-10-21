# Cours 03 — Business Domain Architecture
**Niveau :** Architecture métier / données | **Statut :** cours étudié, QCM corrigé B | **Référence :** [pattern 03](../03-business-domain-architecture/README.md)

## Objectifs
Délimiter les domaines de responsabilité d'une banque de paiements, maîtriser **Data Ownership / System of Record** et définir des contrats interdomaines sans transformer chaque équipe en microservice.

## 1. Domaines de notre SI bancaire fictif
| Domaine | Responsabilités | Donnée dont il peut être autorité |
|---|---|---|
| Clients | Identité, coordonnées, cycle de vie client | Identité de référence |
| Comptes / Core Banking | Tenue de compte et écritures | Écritures/solde autoritatifs |
| Paiements | Instruction, orchestration, statuts de suivi | Référence d'ordre et intention |
| Fraude / Risques | Politique et évaluation du risque | Décision motivée/versionnée de risque |
| Interbancaire | Échange avec les infrastructures externes | Accusés et réponses du rail, selon contrat |
| Comptabilité / Rapprochement | Rapprochements et justificatifs | Dossiers de rapprochement, pas nécessairement ledger maître |

**Attention :** un « domaine » désigne une frontière métier et un ensemble de responsabilités. Il n'est ni un namespace OpenShift, ni une équipe de développement, ni une base de données.

## 2. Schéma de responsabilités
~~~mermaid
flowchart TB
  C["Clients : identité maître"] -->|"Référence client / contrat"| P["Paiements : intention et statut"]
  A["Comptes : écritures autoritatives"] <-->|"Instruction et résultat attesté"| P
  P -->|"Demande d'évaluation"| F["Fraude : décision et motifs"]
  P <-->|"Messages et retours"| I["Interbancaire : rail / échanges"]
  P -->|"Événements dérivés"| S["Suivi, audit, reporting"]
~~~

## 3. Data Ownership : exemple concret
Le domaine Paiements a besoin de connaître le nom et parfois l'adresse du client. Il peut conserver une **copie datée** pour preuve historique, mais il ne doit pas créer une deuxième autorité de modification des informations clients.

- **Commande** : demande à l'autorité de modifier un objet qu'elle maîtrise (par exemple une adresse).
- **Consultation** : lire des attributs via un contrat autorisé.
- **Événement** : informer les abonnés qu'une donnée a changé.
- **Projection** : copie dérivée, potentiellement périmée, dont la fraîcheur doit être explicite.
- **Rapprochement** : comparer la projection à la source autoritative selon les règles du domaine.

Un solde calculé dans un tableau Kafka n'est **pas** une autorité d'écriture financière. Le statut de suivi PAYMENT_SUBMITTED n'est **pas** SETTLED.

## 4. Contrats interdomaines
Exemple de contrat logique *CheckFunds* :
- Requête : paymentId, accountRef, amountMinor=50000, currency=EUR, horodatage, identité du service.
- Réponse : statut d'admissibilité, référence de décision, échéance de validité et code de motif.
- Propriétaire : domaine Comptes ; consommateurs autorisés : domaine Paiements.
- NFR : latence, disponibilité, confidentialité, contrôle d'accès, version du contrat.
- Erreur : timeout ⇒ issue **UNKNOWN**, pas une autorisation implicite.

Les données personnelles et financières doivent être minimisées, sécurisées et gouvernées.

## 5. Démarche d'urbanisation
1. Cartographier capacités, informations maîtresses, politiques métier et événements.
2. Identifier les responsables du **sens métier** de chaque objet (client, compte, ordre, écriture, fraude).
3. Préciser ce qui est lecture, décision, commande, publication d'un fait ou simple cache.
4. Établir des frontières et contrats entre domaines ; analyser couplages et partages de schéma.
5. Tester changements de contrat, retards d'événements et incohérences de projections.
6. Faire valider les frontières par métiers, sécurité, données, exploitation et architectes.

## 6. Pannes typiques
| Problème | Risque | Protection |
|---|---|---|
| Clients et Paiements modifient l'adresse maître | Versions divergentes | Autorité unique ; contrat de modification |
| Reporting croit qu'un événement Kafka prouve un règlement | Faux statut | Preuve Core/rail, provenance |
| Deux systèmes commandent le même paiement | Double exécution | Référence stable et idempotence à l'autorité |
| Une projection est en retard | Décision fondée sur ancien état | Fraîcheur, politique de fallback |

## 7. Livrables
Carte des domaines, définitions et propriétaires ; catalogue d'objets métier ; matrice CRUD d'autorité ; context map ; contrats API/événements ; règles de synchronisation ; ADR sur les frontières ; jeux de tests.

## 8. Exercice corrigé
**Question :** Clients et Paiements modifient tous deux nom/adresse de référence. (A) garder deux bases maîtres, (B) désigner Clients comme autorité et exposer un contrat, (C) fusionner toutes les applications Java.

**Correction : B.** Une source autoritative, des interfaces vérifiables et des copies dérivées gouvernées préviennent les contradictions. Un domaine ne doit pas être fusionné pour corriger un problème de responsabilité.

## 9. Questions d'entretien
- **Domaine vs application ?** Frontière métier vs réalisation logicielle, potentiellement plusieurs applications par domaine.
- **Pourquoi Data Ownership ?** Éviter des mises à jour concurrentes et rendre traçable la source de vérité.
- **Quel lien avec DDD ?** Les bounded contexts applicatifs peuvent suivre les frontières métier, sans coïncidence obligatoire.

---

## Cadre de l'étude
Cas **fictif et anonymisé** : une banque imaginaire modernise des services de virements SEPA et instantanés. Aucun SI client réel, flux propriétaire, métrique mesurée ou conformité certifiée n'est revendiqué. Les identifiants, seuils et composants sont des hypothèses pédagogiques. Les obligations de chaque scheme de paiement, licences et NFR doivent être vérifiés avant usage réel.

**Fil rouge :** virement de 500 EUR, référence métier immuable VIR-001. Un ACK réseau/MQ ne prouve jamais un règlement ; seul le système financier/rail autoritatif permet de conclure. Un timeout ne prouve pas un échec. Les reprises nécessitent idempotence, preuve et respect de l'échéance de l'ordre.
