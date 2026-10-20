# V4 — Rapport de consolidation et limites de preuve (20/10/2026)

## Livrables commités sur la branche

- Itération 1 : huit matrices de sélection réécrites avec les liens exacts (enterprise, applicative, data, resilience, security, cloud hybride, SRE, legacy).
- Itération 2 : huit fiches Enterprise Integration Patterns et leur index.
- Itération 3 : onze fiches Java/GoF et un laboratoire Java 17 contenant sept contrôles.
- Itération 4 : cinq fiches Decision Management et cinq Platform Engineering.
- Itération 5 : trois cas transversaux, le guide V4, README, audit et CI mis à jour.

**Total : 151 fiches du socle V3 + 29 fiches ajoutées = 180.** Trois cas ne sont pas comptés comme patterns.

## Contrôles réalisés

| Contrôle | Résultat | Limite |
|---|---|---|
| Arbre GitHub récursif des fiches et cardinalités des 15 familles | **180/180 PASS** | Contrôle de structure seulement |
| Liens des huit matrices corrigées | **PASS** | Vérification de la présence des chemins cibles |
| Liens des 29 fiches, de leurs index et des trois cas | **PASS** | Vérification de la présence des chemins cibles |
| Présence de deux diagrammes Mermaid par nouvelle fiche | **PASS** | Les diagrammes ne sont pas des résultats runtime |
| Liens du README, du guide V4 et des notices labs | **PASS** | Pas de validation éditoriale externe |
| `javac` + `java PatternsLab` sur copie localement identique à GitHub | **GOF_LAB_PASS=7/7** | Environnement local JDK, pas CI GitHub |
| Correspondance du Git blob du laboratoire compilé | **4719ea03f5943e91b4a7c33a64f241d76f6eb5c7** | Atteste les octets du lab Java seulement |
| GitHub Actions Architecture labs sur branche/PR | **FAIL / non validé** | Échec constaté ; les logs du job sont indisponibles au connecteur |
| GitHub Actions Architecture labs sur `main` avant branche | **Échecs préexistants** | Cause exacte non déterminée ; ne pas attribuer automatiquement à l'infrastructure |

## Sortie / décision de fusion

**PR EN REVUE — NE PAS FUSIONNER AVANT ÉLUCIDATION DU JOB CI.**

Lire les annotations GitHub Actions depuis l'interface, ou exécuter la validation suivante après un clone local :

```bash
python scripts/audit-patterns.py
python -m unittest discover -s labs/idempotency -v
python -m unittest discover -s labs/ai-rag-guardrails -v
python -m unittest discover -s labs/java-openshift-modernization -v
mkdir -p /tmp/gof-classes
javac -d /tmp/gof-classes labs/java-gof/PatternsLab.java
java -cp /tmp/gof-classes PatternsLab
```

Ces référentiels et labs contiennent des cas synthétiques. Ils ne prouvent ni déploiement client, ni usage de logiciels propriétaires, ni disponibilité multi-site physique.
