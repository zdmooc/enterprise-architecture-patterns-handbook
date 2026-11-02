# Cours 101 — Event Schema Evolution · Enterprise Integration Patterns

> Cas pédagogique bancaire fictif : virement SEPA 500 EUR. Corrigé théorique, **quiz individuel non encore validé**.

## 1. Problème et intention
La banque doit gérer **Event Schema Evolution** lorsque les messages, traitements et contrats évoluent indépendamment. Un accusé de transport n'est pas un règlement financier.

**Contrat métier :** référence stable de l'ordre, messageId, correlationId, schemaVersion, deadline métier et propriétaire de chaque étape.

## 2. Scénario et HLD
```mermaid
flowchart LR
    A["Événement vN"] --> B["Schema registry et tests CI"]
    B --> C["Consumers versionnés"]
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
1. Compatibilité structurelle ne garantit pas sémantique métier.
2. La propriété de la source autoritative ne se déduit pas de la présence de Kafka, d'IBM MQ ou d'un adaptateur.
3. Pour une commande, garantir absence de double effet avec un identifiant métier durable jusqu'au point d'exécution.
4. Pour les données ou événements, tester contrats, versions et identité du producteur.
5. Prévoir backlog, métriques, rejets, purge et preuve de reprise sans divulguer les données de paiement.

## 5. Tests
- Nominal : Consumers versionnés, avec preuve observable.
- Panne : Compatibilité structurelle ne garantit pas sémantique métier.
- Redélivrance et concurrence : aucune seconde opération non voulue.
- Sécurité : refus du message non autorisé et absence de fuite dans la DLQ.
- Migration : même signification des statuts avant et après versionnement.

## 6. QCM corrigé
**Quelle conception répond correctement à Event Schema Evolution dans notre banque ?**

- **A.** Supposer que Event Schema Evolution rend le paiement exactly-once sans autre contrôle.
- **B.** Utiliser Event Schema Evolution avec Schema registry et tests CI et prouver la propriété Consumers versionnés.
- **C.** Acquitter systématiquement un message avant son traitement pour éviter toute reprise.

**Bonne réponse : B.** Compatibilité structurelle ne garantit pas sémantique métier. Le résultat doit être prouvé et les limites du pattern explicitées.

## 7. Fiche technique détaillée déjà présente dans le référentiel
[Ouvrir la source originale](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/18-enterprise-integration-patterns/08-schema-evolution/README.md)

**Enterprise Integration Pattern complémentaire**, document de référence synthétique.

#### Contexte

Un producteur versionne un événement alors que les consommateurs déploient à des cadences différentes. Il faut maîtriser les frontières de fiabilité, d'identité, de version et de rétention.

#### Architecture

```mermaid
flowchart LR
 A["Producteur vN/vN+1"] --> B["Schema Registry / contrats"] --> C["Consumers indépendants"] --> D["Quarantaine version inconnue"]
```

#### Séquence de test

```mermaid
sequenceDiagram
 participant P as Producteur
 participant X as Transport/Contrôle
 participant C as Consommateur
 P->>X: messageId, version et référence
 X->>C: livraison avec métadonnées
 C--xX: panne / refus / timeout
 X->>X: appliquer règle et conserver preuve
 X-->>P: résultat confirmé ou incident
```

#### Invariant

Évolution additive compatible et validation transitive selon politique de consommateurs.

#### Implémentation

Prévoir versions, data classification, règles de compatibilité backward/forward, période de coexistence. Protéger les métadonnées tenant, chiffrer les charges sensibles, fixer un TTL et tracer correlationId sans divulguer de secret.

#### Tests obligatoires

1. **Injection d'incident** : Supprimer champ nécessaire avant migration : CI contract bloque release.
2. **Reprise ou sécurité** : Un consumer ancien reçoit vN+1 : lit sans perdre sens ni données obligatoires.
3. Contrôle CI : schéma invalide ou non autorisé doit échouer de façon explicite.

#### Compromis et exploitation

Une compatibilité JSON de structure ne garantit pas l'équivalence sémantique métier. Prouver consumer-driven contracts et métriques de rejet par schemaVersion. Un ACK ne prouve pas que la décision métier est validée.

#### Question d'entretien

Comment limiter les effets de bord et prouver une reprise cohérente si le message est en doublon, perdu ou incompatible ?

[Catalogue](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/18-enterprise-integration-patterns/README.md) · [EDA existante](https://github.com/zdmooc/enterprise-architecture-patterns-handbook/blob/main/01-integration-patterns/04-event-driven-architecture/README.md)

[Retour à l'index](README.md)
