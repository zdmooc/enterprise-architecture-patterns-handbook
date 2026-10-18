# 07 — Aggregate / Consistency Boundary

> **Famille : Architecture applicative** · SI fictif · Pattern conceptuel, à valider par contrats et tests. Aucun établissement réel n'est décrit.

## 1. Problème et contexte

Plusieurs entités modifiées séparément peuvent violer un invariant métier.

**Solution :** Choisir un agrégat qui protège ses invariants dans une transaction locale, avec identifiants et version.

## 2. Architecture — diagramme logique

~~~mermaid
flowchart LR
    A["Commande validée"] --> B["Agrégat et contraintes"] --> C["Commit atomique"]
~~~

### Exemple métier

Une réservation fictive ne doit pas dépasser la limite définie dans l'agrégat concerné.

**Non-garantie :** Agrégat géant verrouille toute la base.

## 3. Séquence nominale et frontières

~~~mermaid
sequenceDiagram
    actor U as Acteur métier fictif
    participant A as Commande validée
    participant B as Agrégat et contraintes
    participant C as Commit atomique
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

- **Quand choisir :** lorsque le problème suivant est réel : Plusieurs entités modifiées séparément peuvent violer un invariant métier.
- **Invariant à protéger :** Deux commandes concurrentes n'enfreignent pas la limite.
- **Alternative :** privilégier une architecture monolithique simple ou un modèle de données direct si le coût du pattern dépasse son intérêt.
- **Anti-pattern :** Agrégat géant verrouille toute la base.
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
- **Preuve d'acceptation :** Deux commandes concurrentes n'enfreignent pas la limite.

## 8. Question d'entretien

**Quand « Aggregate / Consistency Boundary » est-il pertinent, et quel risque ne règle-t-il pas ?**

Réponse : Choisir un agrégat qui protège ses invariants dans une transaction locale, avec identifiants et version. Toutefois, agrégat géant verrouille toute la base.

## 9. Liens de navigation

- [Index de la famille](../README.md)
- [Cas d'étude inter-domaines](../CASE_STUDY.md)
- [Matrice de choix](../DECISION_MATRIX.md)
- [Patterns d'intégration déjà documentés](../../01-integration-patterns/01-request-response/README.md)
