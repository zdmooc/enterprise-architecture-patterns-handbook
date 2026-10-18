# 08 — Data Vault / Historized Integration

> **Famille : Architecture de données** · SI fictif · Pattern conceptuel, à valider par contrats et tests. Aucun établissement réel n'est décrit.

## 1. Problème et contexte

Les sources changent souvent de schéma et les exigences d'audit imposent l'historisation.

**Solution :** Modéliser hubs, links et satellites pour gérer clés métier, associations et attributs historisés.

## 2. Architecture — diagramme logique

~~~mermaid
flowchart LR
    A["Clés métier : hubs"] --> B["Relations : links"] --> C["Historique : satellites"]
~~~

### Exemple métier

Une relation fictive client–contrat est historisée sans réécrire les sources de vérité.

**Non-garantie :** Schéma complexe appliqué à une petite application CRUD sans besoin analytique.

## 3. Séquence nominale et frontières

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

## 4. Méthode d'implémentation

1. Définir les responsabilités de chaque composant et la source de vérité des données.
2. Spécifier contrats d'entrée/sortie, clés, sémantique des statuts, ownership et versions.
3. Séparer règles métier, déploiement, stockage et infrastructures ; documenter la transaction locale.
4. Préparer un cas nominal et deux défaillances : crash entre écriture et réponse, puis données obsolètes/incohérentes.
5. Valider migration, réversibilité, coût, latence p99, exploitation et protection des informations.

## 5. Décisions et compromis

- **Quand choisir :** lorsque le problème suivant est réel : Les sources changent souvent de schéma et les exigences d'audit imposent l'historisation.
- **Invariant à protéger :** Traçabilité source/historique et rejouabilité de chargement testées.
- **Alternative :** privilégier une architecture monolithique simple ou un modèle de données direct si le coût du pattern dépasse son intérêt.
- **Anti-pattern :** Schéma complexe appliqué à une petite application CRUD sans besoin analytique.
- **Architecture d'intégration :** pour les messages répétés, prévoir Outbox et consommateur idempotent si le contrat le justifie ; ne pas inventer d'exactly-once métier.

## 6. Modes de panne — diagnostic et actions

| Injection | Comportement attendu |
|---|---|
| Réponse perdue après traitement | Interroger le statut via une référence stable, aucune mutation supplémentaire aveugle |
| Changement de contrat incompatible | Contract tests bloquent la promotion ; conserver version compatible |
| Donnée de référence ancienne | Marquer la fraîcheur et consulter la source autoritative pour décisions critiques |
| Consommateur temporairement hors service | Backpressure/rejeu selon rétention, sans doublon d'effet métier |

## 7. Plan de qualification et preuve

- Test domaine : valider l'invariant indépendamment du réseau et du framework.
- Test contrat : démontrer compatibilité et versionnement des interfaces et événements.
- Test concurrence : deux requêtes simultanées sur la même référence ne contournent pas les règles.
- Test reprise : isoler panne locale, stockage et consommateur externe ; vérifier que les états restent explicables.
- Test qualité/sécurité : ACL, minimisation, conservation, chiffrement et observabilité.
- **Preuve d'acceptation :** Traçabilité source/historique et rejouabilité de chargement testées.

## 8. Question d'entretien

**Quand « Data Vault / Historized Integration » est-il pertinent, et quel risque ne règle-t-il pas ?**

Réponse : Modéliser hubs, links et satellites pour gérer clés métier, associations et attributs historisés. Toutefois, schéma complexe appliqué à une petite application CRUD sans besoin analytique.

## 9. Liens de navigation

- [Index de la famille](../README.md)
- [Cas d'étude inter-domaines](../CASE_STUDY.md)
- [Matrice de choix](../DECISION_MATRIX.md)
- [Patterns d'intégration déjà documentés](../../01-integration-patterns/01-request-response/README.md)
