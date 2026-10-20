# Parties prenantes & RACI (exemple)

## Acteurs
- **Métiers (RH/CRM/Finance)** : expression besoin, validation fonctionnelle
- **Chef de projet technique** : planning, coordination, MEP
- **Architecte technique** : conception cible, validation, arbitrages, documentation
- **Sécurité (RSSI / équipe SSI)** : exigences, validation matrice flux, audits
- **Réseau** : DMZ, FW, DNS, LB, egress
- **DBA** : Oracle, performances, sauvegardes
- **RUN/Exploitation** : supervision, incidents, astreinte, DRP
- **Équipe Dev** : build, packaging, tests, qualité

## RACI (extrait)
| Activité | Métier | CP Tech | Architecte | SSI | RUN | Réseau | DBA |
|---|---|---|---|---|---|---|---|
| Cadrage / périmètre | R | A | C | C | C | C | C |
| DAT & vues archi | C | C | A/R | C | C | C | C |
| Matrice de flux | C | C | A/R | A/R | C | R | C |
| NFR & SLO/SLI | C | C | A/R | C | A/R | C | C |
| DRP/DRCP | C | C | A/R | C | A/R | C | C |
| Validation Go/NoGo MEP | A | A/R | C | C | A/R | C | C |
