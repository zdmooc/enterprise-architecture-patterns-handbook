# LLD ML Serving

## Objet
Décrire un pattern de service d’inférence exposé via API interne ou service mesh ultérieur.

## Cas d’usage MayaBank
- scoring enrichi
- aide au pricing
- classification documentaire
- génération de recommandations internes

## Points d’architecture
- service plutôt stateless avec dépendances externes
- exposition via Kong
- métriques de latence, erreurs et coût à suivre
- IAM/OIDC pour appels applicatifs ou opérateur

## Statut
Documenté en V1, semi-exécutable futur.
