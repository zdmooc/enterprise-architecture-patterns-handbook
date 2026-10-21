# Cours 09 — Transformation Roadmap / Vagues de migration
**Niveau :** Gouvernance de transformation | **Progression :** QCM C validé | [Fiche canonique](../09-transformation-roadmap/README.md)

## Objectifs
Transformer le blueprint et les architectures intermédiaires en une feuille de route **finançable, ordonnée et conditionnelle** : dépendances, capacité des équipes, risques, coûts, résultats mesurables, décisions GO/NO-GO et opérations après bascule.

## 1. Pourquoi une roadmap n'est pas un Gantt
Un Gantt fixe les activités dans le temps. Une roadmap d'architecture indique **pourquoi** une vague existe, **ce qu'elle rend possible**, ce qui bloque son lancement et comment elle s'inscrit dans le métier. Une date de jalon ne vaut pas une preuve de résilience.

~~~mermaid
flowchart LR
  P["Vague 0 : preuves AS-IS et contrats"] --> C["Vague 1 : consultation"]
  C --> E["Vague 2 : notifications / événements"]
  E --> T["Vague 3 : transactionnel après tests"]
  T --> K["Vague 4 : cutover"]
  K --> D["Vague 5 : décommission legacy"]
  T -. "Gate NO-GO si idempotence non prouvée" .-> R["Correction et requalification"]
  R --> T
~~~

## 2. Roadmap de notre SI bancaire fictif
| Vague | Cible métier et technique | Prérequis P0 | Preuve de sortie |
|---|---|---|---|
| 0. Fondations | Cartographier 100 % interfaces critiques ; owners, contrats, risques | Accès inventaire / sponsor | Flux et dépendances validés |
| 1. Consultation | Nouveau service de lecture sur OpenShift | IAM, réseaux, données en lecture | Non-régression + sécurité + perf |
| 2. Suivi | Notifications et événements Kafka | Contrats et schémas, Outbox, ACL | Rejeu, panne subscriber, lag qualifiés |
| 3. Transactionnel | Java modernisé + MQ/Core conservé, shadow puis canary | JTA/JMS/DB supportés, idempotence | Aucune double exécution lors des essais ; deadline gérée |
| 4. Cutover | Attribution nouveaux ordres sur cible | Reprise, réconciliation, rollback prouvés | Ordres en vol maîtrisés, SLO vérifiés |
| 5. Retrait | Désactiver moteur et interfaces temporaires | Aucun flux non repris, conservation | Décommission approuvé et auditable |

Le découpage des vagues **ne signifie pas** que chaque composant doit avoir été changé. Dans cet exemple, conserver MQ/Core peut réduire le risque.

## 3. Exemple du comité de programme
La vague 2 (notifications Kafka) passe ses tests. La vague 3 (transactions) échoue lors d'une redélivraison : la simulation montre deux effets comptables pour un paymentId.

**Décision recommandée :** avancer sur les livrables sans dépendance transactionnelle, mais **NO-GO** sur l'admission des vrais paiements par le nouveau moteur. Corriger l'unicité autoritative, rejouer les tests et faire approuver une nouvelle version des preuves.

## 4. Gouvernance d'une vague
~~~mermaid
flowchart TD
  A["Dossier d'entrée : besoin + prérequis + coût"] --> B["Construction / tests nominaux"]
  B --> C["Résilience, sécurité, charge, conformité"]
  C --> D{"Critères P0 satisfaits ?"}
  D -->|Oui| E["Design Authority : GO conditionnel"]
  D -->|Non| F["NO-GO : remédiation, replanification"]
  E --> G["Exploitation / indicateurs / revue"]
  F --> C
~~~

**À chaque vague :** sponsor, owner IT, responsable sécurité, responsable exploitation, budget CAPEX/OPEX ou assimilé, critères d'acceptation, preuves, risques résiduels, plan de retour arrière et date de décision.

## 5. Dépendances importantes
- Les contrats et ownership de données doivent précéder le découpage des services.
- Identité, certificats, réseau, secrets et observabilité doivent être opérationnels avant les tests métier.
- Sauvegarde/restauration et PRA ne doivent pas être ajoutés après le cutover.
- Disponibilité du Core et vieillissement des commandes MQ gouvernent les reprises SCT Inst.
- Formation RUN, licences/support éditeur et capacité des équipes font partie de la roadmap.

## 6. Indicateurs de réussite
Couverture d'interfaces validées ; taux de tests P0 réussis ; ordres en état UNKNOWN ; temps de réconciliation ; incidents lors des migrations ; performances à charge de pointe ; reste à faire de décommission ; coût dual-run. **Fixer les seuils par métier/SLO**, ne pas fabriquer une cible chiffrée.

## 7. Livrables
Roadmap par vagues et dépendances ; calendrier et budgets estimatifs ; risques ; RACI ; registre décisions ; KPI de sortie ; critères GO/NO-GO ; plan de conduite du changement, décommission et plan de réexamen.

## 8. Exercice corrigé
Le programme est sous pression. Les API et événements Kafka sont qualifiés ; tests MQ/Core/rollback non terminés. (A) tout basculer, (B) remplacer MQ par Kafka, (C) continuer les vagues sûres mais bloquer le transactionnel.

**Correction : C.** Risques et dépendances sont localisés. Le comité autorise ce qui ne compromet pas l'invariant financier et garde le P0 en NO-GO.

## 9. Entretien
**« Comment défendez-vous la roadmap devant un sponsor ? »** Je présente la valeur par vague, le chemin critique, les coûts, les décisions qui restent conditionnelles et les preuves sans lesquelles une mise en production serait injustifiable.

---

## Périmètre et intégrité pédagogique
Tous les exemples représentent un **SI bancaire fictif** et non l'architecture réelle d'un client. Les SLO, volumes, technologies et stratégies sont des hypothèses de conception ; les preuves de production ne sont pas revendiquées. Pour des paiements, un statut de transport n'est pas un règlement, un timeout ne démontre pas un échec, et une compensation applicative ne défait pas nécessairement un règlement irréversible. Les échéances métier et règles effectives du scheme doivent être validées.
