# 06 — API Gateway et API Management

## Intention
Exposer des APIs de paiement à des consommateurs mobiles, web et partenaires avec un point de contrôle central. **Gateway = chemin de données/runtime** ; **API Management = gouvernance et cycle de vie** (catalogue, publication, contrats, abonnements, versions, analytics, portail développeurs). Une suite API Management peut intégrer une ou plusieurs Gateways.

## Exemple
~~~mermaid
flowchart TB
  C["Application mobile / partenaire"]
  IAM["IdP : OAuth 2.0 / OIDC"]
  G["API Gateway : TLS, JWT, quota, routage"]
  R["OpenShift Route / Ingress"]
  S["Payment API Java"]
  B["Moteur d'autorisation métier"]
  C -->|HTTPS Bearer token| G
  C <-.-> IAM
  G -->|Token validé| R
  R --> S
  S --> B
  G -.->|JWKS / introspection selon contrat| IAM
~~~

## Trois contrôles distincts
1. **Authentification** : identité vérifiée dans un parcours adapté (OIDC pour couche identité) ; OAuth 2.0 vise d'abord l'autorisation déléguée.
2. **Autorisation d'accès API** : scope, audience, destinataire, contexte, limites.
3. **Autorisation métier** : droits sur le **compte et le paiement précis**, plafond, bénéficiaire, règles de conformité et validation du paiement. Un JWT valide ne suffit jamais pour déclencher 500 €.

## Contrat exemple (fictif)
~~~http
POST /api/v1/payments
Authorization: Bearer TOKEN
Idempotency-Key: PAY-001
X-Correlation-ID: corr-01
Content-Type: application/json
~~~
Décisions à contracter : codes 201/202/4xx/5xx, statut métier, suivi, règles de réitération, schéma d'erreurs, versionnement, délai d'acceptation et délai métier d'exécution. Ne pas mettre le token ni des identifiants personnels dans les logs.

## Contrôles sécurité
- TLS en entrée ; TLS vers backend, éventuellement mTLS ; validation du certificat et renouvellement.
- JWT : signature, algorithme autorisé, iss, aud, exp, nbf, scope et rotation JWKS ; tokens opaques : introspection selon contrat.
- Rate limiting / quotas et protection contre brute force ; éviter un point unique de saturation.
- Authorization Object Level dans le service : le détenteur du token ne peut pas lire n'importe quel paymentId.
- Schémas, taille de payload, parsing, rejet de propriétés non autorisées ; revue OWASP API Top 10.
- Secrets gérés, séparation des environnements, journalisation non sensible, politiques de conservation et pistes d'audit.

## Gateway vs OpenShift Route
La Route expose et route le trafic vers le Service, mais ne constitue pas, à elle seule, la gouvernance complète d'API. Pour OpenShift, documenter la topologie (edge / reencrypt / passthrough), le termination TLS, l'identité vue par le backend et la chaîne de confiance.

## Performance et résilience
HA multi-réplicas, zones de panne, timeouts par saut, quotas pour consommateurs, métriques p95/p99, disponibilité et certificats. Un *fallback* d'une requête d'exécution ne doit jamais inventer « paiement rejeté/réussi » si statut inconnu.

## Pannes / réponses
| Cas | Comportement |
|---|---|
| Token expiré | 401 ; renouvellement géré par le client |
| Scope insuffisant | 403 |
| Quota dépassé | 429 ; Retry-After si applicable |
| Backend lent | 504 / erreur contractuelle ; statut financier à vérifier |
| Clé idempotente répétée | Acheminer vers même intention métier |

## API Management : livrables d'architecture
Catalogue, contrats OpenAPI, exposition/consommateurs, politiques, versions, dépréciations, portail développeur, tests de sécurité, observabilité et ownership. L'outillage peut être IBM API Connect, Kong, Apigee, Azure APIM, etc. : **aucun choix produit CAPS n'est revendiqué**.

## Questions d'entretien / critères
- OIDC vs OAuth2 vs JWT ? Couche d'identité / cadre d'autorisation / format de jeton.
- 401 vs 403 vs 429 ? Non authentifié / non autorisé / quota.
- API Gateway remplace-t-elle les contrôles métier ? **Non**.
- Quels contrôles protègent un POST de paiement contre répétition ? Clé d'idempotence et unicité dans le système métier, pas seulement quota Gateway.

Sources : [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html), [OWASP API Security Top 10](https://api-security.owasp.org/editions/2023/en/0x11-t10/).
