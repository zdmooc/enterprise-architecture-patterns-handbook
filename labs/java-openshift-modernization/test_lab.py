"""Static YAML and Java-lab checks; pip install PyYAML>=6,<7.

No cluster access and no network calls. This is not OpenShift admission testing.
"""
import pathlib
import re
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT / "manifests" / "base"


def resources(filename):
    return [x for x in yaml.safe_load_all((BASE / filename).read_text(encoding="utf8")) if x]


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.deployment = resources("deployment.yaml")[0]
        self.container = self.deployment["spec"]["template"]["spec"]["containers"][0]

    def test_every_yaml_parses(self):
        files = list((ROOT / "manifests").rglob("*.yaml"))
        self.assertGreaterEqual(len(files), 9)
        for path in files:
            with self.subTest(file=path.name):
                self.assertTrue(list(yaml.safe_load_all(path.read_text(encoding="utf8"))))

    def test_deployment_has_three_replicas(self):
        self.assertEqual(self.deployment["spec"]["replicas"], 3)

    def test_label_selectors_match(self):
        selector = self.deployment["spec"]["selector"]["matchLabels"]
        labels = self.deployment["spec"]["template"]["metadata"]["labels"]
        self.assertEqual(selector, labels)

    def test_nonroot_no_privilege_escalation(self):
        sec = self.container["securityContext"]
        self.assertTrue(sec["runAsNonRoot"])
        self.assertFalse(sec["allowPrivilegeEscalation"])
        self.assertEqual(sec["capabilities"]["drop"], ["ALL"])
        self.assertNotIn("runAsUser", sec)

    def test_readonly_root_filesystem_and_tmp_mount(self):
        self.assertTrue(self.container["securityContext"]["readOnlyRootFilesystem"])
        mounts = {x["mountPath"] for x in self.container["volumeMounts"]}
        self.assertIn("/tmp", mounts)

    def test_startup_ready_live_have_distinct_paths(self):
        probes = [self.container[x]["httpGet"]["path"] for x in
                  ("startupProbe", "readinessProbe", "livenessProbe")]
        self.assertEqual(len(set(probes)), 3)

    def test_liveness_not_bound_to_external_core(self):
        self.assertEqual(self.container["livenessProbe"]["httpGet"]["path"], "/health/live")

    def test_resources_have_requests_and_memory_limit(self):
        res = self.container["resources"]
        self.assertIn("memory", res["requests"])
        self.assertIn("cpu", res["requests"])
        self.assertIn("memory", res["limits"])

    def test_pdb_allows_one_voluntary_eviction(self):
        self.assertEqual(resources("pdb.yaml")[0]["spec"]["minAvailable"], 2)

    def test_default_deny_and_explicit_ingress(self):
        netpol = resources("networkpolicy.yaml")
        self.assertEqual(len(netpol), 3)
        self.assertEqual(set(netpol[0]["spec"]["policyTypes"]), {"Ingress", "Egress"})
        self.assertEqual(netpol[0]["spec"]["podSelector"], {})
        self.assertIn("ingress", netpol[1]["spec"])
        self.assertEqual(netpol[2]["metadata"]["name"], "allow-demo-client-egress")
        self.assertIn("egress", netpol[2]["spec"])

    def test_config_is_external_to_image(self):
        env = self.container["env"]
        self.assertTrue(any("valueFrom" in x for x in env))
        self.assertIn("configmap.yaml", (BASE / "kustomization.yaml").read_text())

    def test_route_uses_edge_with_http_backend(self):
        route = yaml.safe_load((ROOT / "manifests/overlays/openshift/route.yaml").read_text())
        self.assertEqual(route["spec"]["tls"]["termination"], "edge")
        self.assertEqual(route["spec"]["port"]["targetPort"], "http")

    def test_no_hardcoded_real_registry_credentials(self):
        manifest = (BASE / "deployment.yaml").read_text()
        self.assertIn("registry.example.invalid", manifest)
        self.assertNotIn("password:", manifest.lower())
        self.assertNotIn("token:", manifest.lower())

    def test_java_health_endpoints_match_manifests(self):
        source = (ROOT / "src/ExampleServer.java").read_text()
        for path in ("/health/startup", "/health/ready", "/health/live"):
            self.assertIn('"' + path + '"', source)

    def test_dockerfile_has_nonroot_and_multistage(self):
        text = (ROOT / "Dockerfile").read_text()
        self.assertRegex(text, r"(?i)FROM.*AS compile")
        self.assertGreaterEqual(len(re.findall(r"(?m)^FROM ", text)), 2)
        self.assertIn("USER 10001", text)
        self.assertIn("COPY --from=compile", text)


if __name__ == "__main__":
    unittest.main()
