# Laboratoire GoF — JDK 17 sans dépendance

```bash
javac -d /tmp/gof-classes labs/java-gof/PatternsLab.java
java -cp /tmp/gof-classes PatternsLab
```

Attendu : `GOF_LAB_PASS=7/7`. Sept vérifications déterministes : choix de stratégie, factory invalide, commande, décorateur/audit, protection proxy, ordre de validation Template Method, deux observers.

Ce lab ne prouve pas de sécurité en production, de transport distribué ni de HA. Données et seuils fictifs.
