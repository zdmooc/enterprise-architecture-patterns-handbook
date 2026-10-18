# Lab complet — Java HTTP multi-stage Docker + Kubernetes/OpenShift

**Projet de démonstration, entièrement fictif.** Ce service Java HTTP utilise le module JDK \`jdk.httpserver\`. Il ne dépend d'aucun WAR/EAR, framework, système bancaire ou broker ; il **ne remplace pas** une validation du runtime Java/JEE historique. Il permet de démontrer concrètement les patterns : OCI multi-stage, non-root, UID arbitraire, configuration externe, Deployment multi-répliqué, probes, Service, réseau, SCC, PDB, HPA, Route et rollout.

## Fichiers

- [src/ExampleServer.java](src/ExampleServer.java) : endpoints \`/health/startup\`, \`/health/live\`, \`/health/ready\`, \`/api/status\` et gestion SIGTERM.
- [Dockerfile](Dockerfile) : compilation JDK puis runtime JRE, utilisateur non-root.
- [manifests/base](manifests/base/kustomization.yaml) : ConfigMap, SA, Deployment, Service, PDB et NetworkPolicies.
- [overlays/openshift](manifests/overlays/openshift/kustomization.yaml) : ajoute une Route edge HTTPS ; **backend HTTP** d'exemple.
- [manifests/optional/hpa.yaml](manifests/optional/hpa.yaml) : HPA si métriques disponibles.
- [test_lab.py](test_lab.py) : tests de validation YAML et invariants de sécurité (dépend de PyYAML).

## Option A — exécuter sans Docker/Kubernetes (test Java pur)

~~~bash
mkdir -p /tmp/java-modernization-lab
javac --add-modules jdk.httpserver -d /tmp/java-modernization-lab src/ExampleServer.java
java --add-modules jdk.httpserver -cp /tmp/java-modernization-lab ExampleServer
# Dans un autre terminal :
curl -i http://localhost:8080/health/live
curl -i http://localhost:8080/health/ready
curl -i http://localhost:8080/api/status
~~~

Pour arrêter, \`Ctrl+C\` envoie SIGTERM au processus lancé depuis le terminal sur systèmes usuels, permettant d'observer le shutdown hook.

## Option B — Docker local

~~~bash
docker build -t java-modernization-demo:local .
docker run --rm --name java-modernization-demo -p 8080:8080 --read-only --tmpfs /tmp:rw,mode=1777 java-modernization-demo:local
curl -fsS http://localhost:8080/api/status
~~~

Tester UID arbitraire localement si possible :

~~~bash
docker run --rm -p 8081:8080 --user 123456:0 --read-only --tmpfs /tmp:rw,mode=1777 java-modernization-demo:local
curl -fsS http://localhost:8081/health/ready
~~~

## Option C — Kubernetes (kind ou cluster compatible)

1. Construire/pousser une image accessible au cluster ou la charger avec \`kind load docker-image java-modernization-demo:local --name <cluster>\`.
2. Créer un namespace dédié \`java-modernization-demo\`.
3. **Remplacer** \`registry.example.invalid/demo/java-modernization:replace-with-your-image\` dans \`deployment.yaml\` par l'image locale accessible ou une image digest signée du registry choisi.
4. Valider les fichiers puis appliquer la base :

~~~bash
kubectl create namespace java-modernization-demo
kubectl kustomize manifests/base
kubectl apply --dry-run=client -k manifests/base
kubectl apply -k manifests/base
kubectl -n java-modernization-demo rollout status deployment/java-modernization-demo --timeout=180s
kubectl -n java-modernization-demo get deploy,pod,svc,pdb,networkpolicy
kubectl -n java-modernization-demo port-forward svc/java-modernization-demo 8080:8080
~~~

**Attention au réseau :** les NetworkPolicies default-deny sont incluses et autorisent uniquement les Pods portant \`role: demo-client\` dans ce namespace et (sur OpenShift) le namespace ingress selon label standard. Un test client applicatif dans Kubernetes doit respecter cette étiquette. Le port-forward est un chemin administratif et **ne prouve pas** le contrôle des NetworkPolicies. Un cluster kind mono-nœud ne valide pas la HA.

## Option D — OpenShift

~~~bash
oc new-project java-modernization-demo
oc kustomize manifests/overlays/openshift
oc apply --dry-run=client -k manifests/overlays/openshift
oc apply -k manifests/overlays/openshift
oc -n java-modernization-demo rollout status deployment/java-modernization-demo --timeout=180s
oc -n java-modernization-demo get deploy,pod,svc,route,pdb,networkpolicy
oc -n java-modernization-demo get pod -l app=java-modernization-demo -o wide
~~~

**Route d'exemple :** TLS **edge** avec HTTP entre routeur et Pod. En production, envisager \`reencrypt\` + **vrai HTTPS backend** et CA de destination ; ne pas changer seulement le mot \`edge\` en \`reencrypt\`.

**OpenShift SCC :** aucune UID fixe n'est spécifiée dans le Pod et l'image accepte un UID arbitraire. Le \`USER 10001\` de l'image sert en Docker local ; la politique admission OpenShift peut assigner un autre UID. Ne pas accorder \`anyuid\` pour contourner un problème d'image.

### HPA facultatif (pas par défaut)

~~~bash
kubectl -n java-modernization-demo apply -f manifests/optional/hpa.yaml
kubectl -n java-modernization-demo get hpa
~~~

Le HPA a besoin des métriques et de la capacité. L'application simulée ne sollicite aucune DB externe ; l'autoscaling n'atteste pas une capacité bancaire réelle.

## Validation sans cluster et tests

Installer la dépendance d'analyse YAML dans un environnement isolé :

~~~bash
python -m pip install "PyYAML>=6,<7"
python -m unittest discover -s labs/java-openshift-modernization -v
~~~

Ces tests vérifient des invariants **statiques des manifests**, pas l'admission effective OpenShift ni les garanties du core financier.

## Scénarios de panne à répéter dans un lab autorisé

| Incident | Observation à effectuer |
|---|---|
| Supprimer un Pod | Deployment en recrée un ; Service cible les Ready |
| HTTP \`/health/ready\` temporairement KO | Pod retiré du Service sans faux statut bancaire |
| \`oc rollout restart\` | Nouveau Pod startup, ancien en drain SIGTERM |
| Une NetworkPolicy empêche accès | Vérifier CNI/labels/ports et faire un test depuis vrai Pod client |
| Pod forcé sous UID aléatoire | Aucune écriture interdite et processus fonctionnel |
| CPU/mémoire limités | Mesurer OOM, throttling, p95/p99 |
| Node tué | Pas de HA prétendue sur cluster mono-nœud |

**Aucun script ne supprime ni ne modifie automatiquement un cluster.** Les commandes de mutation sont à exécuter explicitement dans un projet de lab maîtrisé.

© 2026 Zidane Djamal.
