# Exercices corrigés — 10 cours d'architecture appliquée aux paiements

> Banque et virements **entièrement fictifs**. Ces cas ne représentent pas l'infrastructure réelle d'un établissement. La bonne réponse démontre un raisonnement d'architecture, pas la performance d'un produit. Un QCM validé ici n'est pas une certification.

## Utilisation
Pour chaque situation, choisir A/B/C puis argumenter avec : **besoin métier → invariant → risques → options → preuve → responsable**. Ne lire la correction qu'après avoir expliqué comment tester la décision.

### 01 — Business Capability Mapping
**Cas :** trois logiciels « SEPA » remplissent des tâches différentes. La DSI veut en éliminer deux.  
A. Choisir le plus moderne. **B. Cartographier capacités, fonctions et dépendances.** C. Les migrer sur Kubernetes.
**Correction B :** « SEPA » ne décrit pas le niveau de couverture. Vérifier initiation, contrôle, traitement, retours et conservation. **Preuve :** matrice capability × application vérifiée par les owners.

### 02 — Value Stream Mapping
**Cas :** une attente fictive de trois secondes est observée avant exécution.  
A. Remplacer MQ. **B. Mesurer chaque segment et le goulot.** C. Ajouter des pods.
**Correction B :** le temps d'attente peut être en file, DB ou aval. **Preuve :** mesures p99 et horodatages corrélés, comparaisons par charge et rail.

### 03 — Business Domain Architecture
**Cas :** Clients et Paiements modifient tous deux l'adresse de référence.  
A. Conserver deux maîtres. **B. Désigner Clients comme autorité, exposer un contrat.** C. Fusionner les domaines.
**Correction B :** la responsabilité de modification doit être explicite ; Paiements peut avoir une projection historisée. **Preuve :** matrice d'ownership, test de mise à jour et de propagation.

### 04 — Application Landscape
**Cas :** migration d'un moteur Java/JEE dont les interfaces MQ, Core et batch ne sont pas toutes connues.  
A. Conteneuriser. **B. Inventorier le patrimoine et les dépendances.** C. Remplacer MQ.
**Correction B :** les flux implicites peuvent être critiques. **Preuve :** inventaire daté, owners, rapports d'exécution et contrats vérifiés.

### 05 — Enterprise Flow Mapping
**Cas :** Core a traité un paiement, la réponse s'est perdue.  
A. Renvoyer avec un autre identifiant. **B. Conserver paymentId et réconcilier.** C. Publier SETTLED directement.
**Correction B :** un timeout est une issue inconnue. **Preuve :** QueryStatus autoritatif ou rapprochement de référence ; test de redélivrance sans double débit.

### 06 — Portfolio Rationalization / TIME
**Cas :** reporting B double une partie de A mais fournit un fichier réglementaire exclusif.  
A. Supprimer B. **B. Analyser usages, reprise et obligations avant classement E.** C. Replatformer puis arrêter.
**Correction B :** la suppression est une décision métier et risque. **Preuve :** tests du fichier repris, propriétaires et archivage validés.

### 07 — Target Architecture Blueprint
**Cas :** moderniser Java/JEE sans reconstruire simultanément Core et tous les middlewares.  
A. Remplacer tout. B. Conteneuriser sans analyse. **C. Définir une cible par couches et préserver l'autorité financière.**
**Correction C :** réduire le rayon d'impact ; documenter interfaces, NFR, alternative et validation. **Preuve :** blueprint lié à besoins/invariants et ADR.

### 08 — Transition Architecture
**Cas :** anomalie OpenShift pendant canary ; ordres en cours sur le nouveau moteur.  
A. Réémettre tous sur le legacy. **B. Suspendre admissions, réconcilier, rerouter les nouveaux si compatible.** C. Effacer MQ.
**Correction B :** le retour arrière de code ne défait pas un débit. **Preuve :** trace de propriété unique et résultats autoritatifs pour ordres en vol.

### 09 — Transformation Roadmap
**Cas :** API et Kafka qualifiés, idempotence et PRA transactionnels non prouvés.  
A. Bascule générale. B. Remplacer MQ par Kafka. **C. Continuer les vagues sûres ; bloquer la transactionnelle.**
**Correction C :** un jalon ne prime pas sur les risques P0. **Preuve :** gates, résultats de tests et décision GO/NO-GO signée.

### 10 — ABB/SBB
**Cas :** un ABB « commandes durables » utilise MQ ; Kafka est proposé pour le remplacer.  
A. Approuver car récent. **B. Comparer contrats, NFR, risques, coûts et preuves.** C. Interdire toute évolution.
**Correction B :** le fournisseur est un moyen ; l'ABB porte l'obligation. **Preuve :** matrice de conformité ABB↔SBB, tests comparatifs et ADR.

---

## Cas transversal senior — Réponse perdue pendant le cutover

**Contexte.** Le moteur legacy et le moteur OpenShift coexistent. Le routeur affecte les nouveaux ordres à l'un des deux moteurs avec une décision persistée. Un paiement VIR-001 de 500 EUR a été envoyé au Core via MQ. Le Core l'a exécuté ; sa réponse a été perdue. La banque souhaite rerouter le trafic vers le legacy après incident OpenShift.

**Travail à réaliser :**
1. Identifier la source financière autoritative et l'owner de VIR-001.
2. Dire quelle preuve manque pour passer de UNKNOWN à SETTLED.
3. Expliquer le comportement correct lors d'un réessai avec la même idempotency-key.
4. Définir les étapes d'un rollback qui n'émet pas de nouvel ordre financier.
5. Proposer deux tests de panne et deux NFR mesurables, avec seuils à négocier.
6. Nommer les livrables : capability map, catalogue des flux, ADR, transition, roadmap et ABB/SBB.

### Corrigé type
1. La preuve financière vient du Core/rail selon le contrat, **pas** de MQ ou du reporting Kafka ; l'owner du paiement est connu par table de routage durable.
2. Un statut attesté à référence stable ou un rapprochement documenté ; tant que la preuve n'existe pas, garder UNKNOWN/TO_RECONCILE.
3. Retrouver VIR-001, ne créer ni nouvel identifiant ni deuxième débit ; déduplication au niveau de l'effet financier.
4. Fermer l'admission ciblée, inventorier ordres en vol, drainer, réconcilier, valider les contrats et ne rerouter que les nouveaux ordres.
5. Tests : (i) panne après effet Core avant ACK ; (ii) panne pendant transfert d'ownership. NFR : p99 bout en bout et délai de réconciliation, selon seuils métier décidés, plus sécurité et disponibilité.
6. Les artefacts documentent différentes questions : *quoi*, *qui*, *comment*, *où aller*, *par quels états*, *dans quel ordre* et *avec quels composants*.

### Barème pour auto-évaluation
| Axe | Indicateur attendu | Points |
|---|---|---:|
| Métier | Autorité financière et statut exacts | 2 |
| Intégration | Corrélation, transport vs effet | 2 |
| Résilience | Idempotence + réconciliation | 2 |
| Transformation | Cutover et rollback sûr | 2 |
| Gouvernance | Preuve/ADR/owner/conditions | 2 |
| **Total** | **10 points** | **10** |

Une réponse qui crée une nouvelle instruction après un timeout sans preuve doit être rejetée, même si le schéma technique paraît correct.

Voir les [cours détaillés](../README.md) et les [schémas transversaux](../schemas/architecture-de-reference.md).
