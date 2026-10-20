# Matrice de flux (extrait)

| Source | Zone | Destination | Zone | Proto | Port | Auth | Chiffrement | Justification | Owner | Criticité |
|---|---|---|---|---|---:|---|---|---|---|---|
| Portail-RH | DMZ | API-Gateway | APP | HTTPS | 443 | OIDC | TLS | Accès utilisateurs internes | AppTeam-RH | Gold |
| CRM-Interne | APP | Rules-Engine | APP | HTTPS | 8443 | RBAC | mTLS | Appels règles métier | AppTeam-CRM | Gold |
| Services | APP | Oracle | DATA | TCP | 1521 | Wallet | TDE | Accès base finance | DBA-Team | Gold |
| Services | APP | S3 | DATA | HTTPS | 443 | IAM | TLS | Stockage documents/exports | Platform-Team | Silver |
