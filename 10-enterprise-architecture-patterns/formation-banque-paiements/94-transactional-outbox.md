# Cours 94 — Transactional Outbox · Enterprise Integration Patterns

> Cas pédagogique bancaire fictif : virement SEPA 500 EUR. Corrigé théorique, **quiz individuel non encore validé**.

## 1. Problème et intention
La banque doit gérer **Transactional Outbox** lorsque les messages, traitements et contrats évoluent indépendamment. Un accusé de transport n'est pas un règlement financier.

**Contrat métier :** référence stable de l'ordre, messageId, correlationId, schemaVersion, deadline métier et propriétaire de chaque étape.

## 2. Scénario et HLD
```mermaid
flowchart LR
    A["Transaction SQL ORDERS + OUTBOX"] --> B["Worker relay"]
    B --> C["Broker MQ / Kafka"]
    B -.-> D["Panne, doublon ou contrat invalide"]
    D --> E["Résultat inconnu / quarantaine / reprise"]
```

**Choix architecturaux :** préciser unités de travail, rétention, idempotence, décision sur délai dépassé, ACL et observabilité.

## 3. Séquence de qualification
```mermaid
sequenceDiagram
    participant A as Source
    participant B as Pattern
    participant C as Cible autoritative
    A->>B: événement 500 EUR / identifiant stable
    B->>C: opération sous contrat
    C-->>B: résultat attesté
    B--xA: réponse perdue ou incident
    A->>B: réessai contrôlé / statut
    B->>C: vérifier résultat existant
    C-->>B: déjà traité ou UNKNOWN
    B-->>A: décision explicitée
```

## 4. Invariants et risques
1. Message publié plusieurs fois : consommer de façon idempotente.
2. La propriété de la source autoritative ne se déduit pas de la présence de Kafka, d'IBM MQ ou d'un adaptateur.
3. Pour une commande, garantir absence de double effet avec un identifiant métier durable jusqu'au point d'exécution.
4. Pour les données ou événements, tester contrats, versions et identité du producteur.
5. Prévoir backlog, métriques, rejets, purge et preuve de reprise sans divulguer les données de paiement.

## 5. Tests
- Nominal : Broker MQ / Kafka, avec preuve observable.
- Panne : Message publié plusieurs fois : consommer de façon idempotente.
- Redélivrance et concurrence : aucune seconde opération non voulue.
- Sécurité : refus du message non autorisé et absence de fuite dans la DLQ.
- Migration : même signification des statuts avant et après versionnement.

## 6. QCM corrigé
**Quelle conception répond correctement à Transactional Outbox dans notre banque ?**

- **A.** Supposer que Transactional Outbox rend le paiement exactly-once sans autre contrôle.
- **B.** Utiliser Transactional Outbox avec Worker relay et prouver la propriété Broker MQ / Kafka.
- **C.** Acquitter systématiquement un message avant son traitement pour éviter toute reprise.

**Bonne réponse : B.** Message publié plusieurs fois : consommer de façon idempotente. Le résultat doit être prouvé et les limites du pattern explicitées.

## 7. Fiche technique détaillée déjà présente dans le référentiel
[Ouvrir la source originale](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/18-enterprise-integration-patterns/01-transactional-outbox/README.md)

**Famille : Enterprise Integration Patterns.** Exemple indépendant, aucun système client réel.

#### Problème et forces

Une transaction modifie la base puis doit notifier d'autres services : une publication directe après COMMIT peut être perdue. Les systèmes distribués redélivrent, échouent partiellement et possèdent des propriétaires de transaction différents.

#### Architecture

```mermaid
flowchart LR
 A["Service métier"] --> B["Transaction SQL : domaine + OUTBOX"] --> C["Relay vers broker"] --> D["Réconciliation de livraison"]
```

#### Séquence de panne à maîtriser

```mermaid
sequenceDiagram
 participant A as Source
 participant B as Coordination
 participant C as Cible
 A->>B: messageId + correlationId + version
 B->>C: effet ou transmission contrôlée
 C--xB: délai / réponse perdue
 B->>B: relire état durable et invariant
 B-->>A: résultat confirmé ou incertain
```

#### Invariant contractuel

Clé de l'événement stable, unicité de publication logique et index sur statut/nextAttemptAt.

#### Conception et arbitrages

Transaction locale métier+outbox, polling relay ou CDC, publication avec clé d'agrégat et ACK broker avant marquage livré. Prévoir contrat de compatibilité, ownership, audit et métriques avant le déploiement. Alternatives : traitement synchrone simple lorsque toléré, broker managé ou consolidation en monolithe si la distribution n'est pas justifiée.

#### Tests de défaillance exigés

1. **Panne après effet :** Crash immédiatement après COMMIT avant publication ; un relay reprend le même eventId.
2. **Panne ou concurrence :** Broker momentanément indisponible : backlog durable, retries bornés et alerte lag.
3. **Sécurité :** schéma non reconnu, utilisateur non autorisé et charge malformée doivent être rejetés et journalisés sans fuite de données.

#### Limites et exploitation

Ne garantit pas livraison unique du transport : les consommateurs restent idempotents. Mesurer backlog, publication et duplications; purger seulement après rétention contrôlée.

#### Question d'entretien

Comment démontrez-vous la sémantique métier malgré doublons, reprises et pertes de réponses ? Répondez par clé stable, état durable, invariant, tests injectés et preuve de replay.

[Catalogue EIP](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/18-enterprise-integration-patterns/README.md) · [Intégration existante](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/01-integration-patterns/04-event-driven-architecture/README.md)

[Retour à l'index](README.md)
