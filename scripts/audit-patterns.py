"""Read-only QA: 151 architecture pattern fiches, Mermaid sources, links and anonymization.

Usage: python scripts/audit-patterns.py
Does not write files, contact networks or access a cluster.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = [
    ("integration", "01-integration-patterns", "*/README.md", 10),
    ("ai", "08-ai-architecture-patterns", "[0-9][0-9]-*/README.md", 15),
    ("platform", "09-containerization-kubernetes-openshift-patterns", "[0-9][0-9]-*/*/README.md", 30),
    ("enterprise", "10-enterprise-architecture-patterns", "[0-9][0-9]-*/README.md", 12),
    ("application", "11-application-software-patterns", "[0-9][0-9]-*/README.md", 15),
    ("data", "12-data-architecture-patterns", "[0-9][0-9]-*/README.md", 12),
    ("resilience", "13-resilience-distributed-systems-patterns", "[0-9][0-9]-*/README.md", 15),
    ("security", "14-security-zero-trust-patterns", "[0-9][0-9]-*/README.md", 12),
    ("cloud", "15-cloud-hybrid-architecture-patterns", "[0-9][0-9]-*/README.md", 10),
    ("sre", "16-performance-sre-patterns", "[0-9][0-9]-*/README.md", 10),
    ("modernization", "17-legacy-modernization-patterns", "[0-9][0-9]-*/README.md", 10),
]
BANNED = [
    re.compile(r"\bCAPS\b"),
    re.compile(r"\bBPCE\b"),
    re.compile(r"\bSTET\b"),
    re.compile(r"\bFIS\b"),
    re.compile(r"\bWero\b"),
    re.compile(r"\bMAIF\b"),
    re.compile(r"Cr[eé]dit Agricole", re.IGNORECASE),
]
LINK_RE = re.compile(r"\]\(([^)\s]+)")
FENCE = "~" * 3
MERMAID_FENCES = (FENCE + "mermaid", chr(96) * 3 + "mermaid")


def audit() -> int:
    errors: list[str] = []
    diagrams = 0
    markdown_files = list(ROOT.rglob("*.md"))
    for file in markdown_files:
        data = file.read_text(encoding="utf-8")
        rel = file.relative_to(ROOT)
        diagrams += sum(1 for line in data.splitlines() if line.strip() in MERMAID_FENCES)
        if data.count(FENCE) % 2:
            errors.append(f"Unbalanced Markdown code fences: {rel}")
        for expression in BANNED:
            for hit in expression.finditer(data):
                line = data[:hit.start()].count("\n") + 1
                errors.append(f"Client name: {rel}:{line}, text={hit.group()}")
        for link in LINK_RE.findall(data):
            if link.startswith(("http:", "https:", "mailto:", "#", "data:")):
                continue
            target = (file.parent / link.split("#")[0].split("?")[0]).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f"Broken relative link: {rel} -> {link}")

    counts = {}
    for label, folder, pattern, expected in FAMILIES:
        cards = list((ROOT / folder).glob(pattern))
        counts[label] = len(cards)
        if len(cards) != expected:
            errors.append(f"Expected {expected} {label} patterns, found {len(cards)}")
        for card in cards:
            content = card.read_text(encoding="utf-8")
            n = sum(1 for line in content.splitlines() if line.strip() in MERMAID_FENCES)
            if n < 2:
                errors.append(f"Less than two diagrams: {card.relative_to(ROOT)}")
    if sum(counts.values()) != 151:
        errors.append(f"Expected 151 pattern fiches, found {sum(counts.values())}")
    print(f"Markdown files: {len(markdown_files)} | Mermaid diagrams: {diagrams} | family counts: {counts}")
    if errors:
        for e in errors[:80]:
            print("FAIL:", e)
        print(f"FAILED: {len(errors)} issues")
        return 1
    print("PASS: 151 fiches, diagrams, relative links and restricted client names")
    return 0


if __name__ == "__main__":
    sys.exit(audit())
