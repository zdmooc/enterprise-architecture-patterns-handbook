# Cours 109 — Data Vault · Architecture des données

> Banque fictive · reporting sur des paiements SEPA de 500 EUR. **Corrigé théorique, quiz individuel non encore validé.**

## 1. Problème et résultat attendu
Plusieurs applications et systèmes analytiques réutilisent les données de paiements. Notre architecture doit produire une information fiable **sans confondre vue dérivée et source autoritative**.

Avec **Data Vault**, nous cherchons à obtenir : historique traçable.

## 2. Schéma fonctionnel
```mermaid
flowchart LR
    A["Identités métier"] --> B["Hubs / liens / satellites"]
    B --> C["Historique traçable"]
    D["Contrôle accès / qualité / provenance"] --> B
    C --> E["Usage métier / analytique sous contrat"]
```

**Invariant principal :** Séparer clé métier, relations et changements dans le temps.

## 3. Contrats à définir
1. **Ownership** : qui est propriétaire de chaque fait, qui le corrige et qui autorise sa consommation ?
2. **Schéma** : identifiants, grain, type, contraintes d'unicité, sémantique des statuts et évolution des versions.
3. **Qualité** : contrôles de complétude, unicité, validité, cohérence temporelle et règles de rejet.
4. **Fraîcheur et SLA/SLO** : délai de publication mesuré, corrections tardives et indication d'obsolescence.
5. **Sécurité** : classification, masquage, limitation de finalité, contrôle par sujet et période de rétention.
6. **Provenance** : source et transformations, version du calcul, responsable et traçabilité des rectifications.

## 4. Séquence illustrative
```mermaid
sequenceDiagram
    participant S as Source autoritative
    participant P as Pipeline ou produit de données
    participant C as Consommateur
    S->>P: fait métier / changement versionné
    P->>P: contrôler qualité et provenance
    P-->>C: jeu ou événement validé + fraîcheur
    alt donnée manquante ou obsolète
       C->>P: demande d'explication
       P->>S: vérifier état et origine
       S-->>P: preuve ou anomalie à traiter
    end
```

## 5. Tests et décisions
- Test nominal : les données publiées conservent un sens métier vérifié et une provenance.
- Test de schéma : un changement incompatible provoque erreur ou version contrôlée.
- Test de retard : la source est plus récente que la projection ; la fraîcheur est visible et la décision critique consulte l'autorité.
- Test sécurité : un utilisateur non autorisé ne peut lire ni ligne sensible, ni donnée brute.
- Test de qualité : doublons, champs manquants et valeurs invalides sont mesurés et traités explicitement.
- Test de reprise : pipeline interrompu puis relancé sans double comptage ni perte indétectée.

## 6. QCM corrigé
**Quelle décision prendre pour appliquer Data Vault ?**
- **A.** Utiliser une vue analytique pour déclencher un règlement sans vérifier la source.
- **B.** Supprimer les contrôles de provenance et d'accès aux données clients.
- **C.** Mettre en œuvre Data Vault en préservant ownership, qualité, fraîcheur et traçabilité.

**Réponse : C.** Séparer clé métier, relations et changements dans le temps. Les preuves incluent qualité, contrat de données et lignée, pas simplement une exécution réussie du job.

## 7. Fiche technique détaillée du référentiel
[Consulter la fiche d'origine](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/12-data-architecture-patterns/08-data-vault/README.md)

> **Famille : Architecture de données** · SI fictif · Pattern conceptuel, à valider par contrats et tests. Aucun établissement réel n'est décrit.

#### 1. Problème et contexte

Les sources changent souvent de schéma et les exigences d'audit imposent l'historisation.

**Solution :** Modéliser hubs, links et satellites pour gérer clés métier, associations et attributs historisés.

#### 2. Architecture — diagramme logique

~~~mermaid
flowchart LR
    A["Clés métier : hubs"] --> B["Relations : links"] --> C["Historique : satellites"]
~~~

#### Exemple métier

Une relation fictive client–contrat est historisée sans réécrire les sources de vérité.

**Non-garantie :** Schéma complexe appliqué à une petite application CRUD sans besoin analytique.

#### 3. Séquence nominale et frontières

~~~mermaid
sequenceDiagram
    actor U as Acteur métier fictif
    participant A as Clés métier : hubs
    participant B as Relations : links
    participant C as Historique : satellites
    U->>A: Requête ou besoin métier
    A->>B: Contrat et référence stable
    B->>C: Traitement et résultat autorisé
    C-->>B: Réponse / état connu
    B-->>A: Résultat contrôlé
    A-->>U: Information justifiée
~~~

Le diagramme est volontairement **logique** : dans une implémentation réelle, certaines transitions sont asynchrones, et un accusé technique ne vaut pas validation financière.

#### 4. Méthode d'implémentation

1. Définir les responsabilités de chaque composant et la source de vérité des données.
2. Spécifier contrats d'entrée/sortie, clés, sémantique des statuts, ownership et versions.
3. Séparer règles métier, déploiement, stockage et infrastructures ; documenter la transaction locale.
4. Préparer un cas nominal et deux défaillances : crash entre écriture et réponse, puis données obsolètes/incohérentes.
5. Valider migration, réversibilité, coût, latence p99, exploitation et protection des informations.

#### 5. Décisions et compromis

- **Quand choisir :** lorsque le problème suivant est réel : Les sources changent souvent de schéma et les exigences d'audit imposent l'historisation.
- **Invariant à protéger :** Traçabilité source/historique et rejouabilité de chargement testées.
- **Alternative :** privilégier une architecture monolithique simple ou un modèle de données direct si le coût du pattern dépasse son intérêt.
- **Anti-pattern :** Schéma complexe appliqué à une petite application CRUD sans besoin analytique.
- **Architecture d'intégration :** pour les messages répétés, prévoir Outbox et consommateur idempotent si le contrat le justifie ; ne pas inventer d'exactly-once métier.

#### 6. Modes de panne — diagnostic et actions

| Injection | Comportement attendu |
|---|---|
| Réponse perdue après traitement | Interroger le statut via une référence stable, aucune mutation supplémentaire aveugle |
| Changement de contrat incompatible | Contract tests bloquent la promotion ; conserver version compatible |
| Donnée de référence ancienne | Marquer la fraîcheur et consulter la source autoritative pour décisions critiques |
| Consommateur temporairement hors service | Backpressure/rejeu selon rétention, sans doublon d'effet métier |

#### 7. Plan de qualification et preuve

- Test domaine : valider l'invariant indépendamment du réseau et du framework.
- Test contrat : démontrer compatibilité et versionnement des interfaces et événements.
- Test concurrence : deux requêtes simultanées sur la même référence ne contournent pas les règles.
- Test reprise : isoler panne locale, stockage et consommateur externe ; vérifier que les états restent explicables.
- Test qualité/sécurité : ACL, minimisation, conservation, chiffrement et observabilité.
- **Preuve d'acceptation :** Traçabilité source/historique et rejouabilité de chargement testées.

#### 8. Question d'entretien

**Quand « Data Vault / Historized Integration » est-il pertinent, et quel risque ne règle-t-il pas ?**

Réponse : Modéliser hubs, links et satellites pour gérer clés métier, associations et attributs historisés. Toutefois, schéma complexe appliqué à une petite application CRUD sans besoin analytique.

#### 9. Liens de navigation

- [Index de la famille](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/12-data-architecture-patterns/README.md)
- [Cas d'étude inter-domaines](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/12-data-architecture-patterns/CASE_STUDY.md)
- [Matrice de choix](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/12-data-architecture-patterns/DECISION_MATRIX.md)
- [Patterns d'intégration déjà documentés](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/01-integration-patterns/01-request-response/README.md)

[Retour au programme](README.md)
