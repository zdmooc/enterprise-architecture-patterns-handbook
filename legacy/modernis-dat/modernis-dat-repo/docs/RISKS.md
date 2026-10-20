# Registre des risques (exemple)

| ID | Risque | Probabilité | Impact | Mitigation | Owner |
|---|---|---:|---:|---|---|
| R1 | Flux non maîtrisés en prod | M | H | Matrice flux + validation SSI + tests | Architecte/SSI |
| R2 | Sous-dimensionnement | M | H | Modèle capacité + tests charge + marge | Architecte/RUN |
| R3 | Dépendance Oracle (latence, contention) | M | M | Profiling, pool tuning, tests, DBA | DBA |
| R4 | Complexité IAM/SSO | M | H | ADR + POC OIDC + rollback | Architecte |
| R5 | DRP non testé | L | H | Exercices DRP planifiés + preuves | RUN |
