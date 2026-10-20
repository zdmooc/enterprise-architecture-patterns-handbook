# Cahier des charges — API Management (exemple)

## 1. Objectif
Mettre en place un socle API Management pour publier, sécuriser et gouverner les API internes/externes.

## 2. Exigences fonctionnelles
- Catalogue API + portail développeur
- Gestion cycle de vie (versioning, dépréciation)
- Policies : auth, rate limit, quotas, IP allow-list
- Observabilité : métriques, logs, tracing

## 3. Exigences techniques
- Déploiement OpenShift (operator/helm) ou service managé
- HA, montée en charge, multi-environnements
- Intégration OIDC (IAM entreprise/Keycloak)

## 4. Sécurité
- TLS, gestion des certificats, journaux d’audit
- Support mTLS (optionnel), WAF (optionnel)

## 5. Critères d’évaluation
- Couverture fonctionnelle
- Exploitabilité (RUN), support éditeur
- Coût (licence + infra), time-to-value
