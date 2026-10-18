"""Read-only QA for the 55 pattern fiches, Mermaid diagrams, links and anonymization.

Usage: python scripts/audit-patterns.py
No web access, no cluster mutation.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = [
    ("integration", ROOT / "01-integration-patterns", "*/README.md", 10),
    ("ai", ROOT / "08-ai-architecture-patterns", "[0-9][0-9]-*/README.md", 15),
    ("platform", ROOT / "09-containerization-kubernetes-openshift-patterns",
     "[0-9][0-9]-*/*/README.md", 30),
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
    for p in markdown_files:
        data = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT)
        diagrams += sum(1 for line in data.splitlines() if line.strip() in MERMAID_FENCES)
        if data.count(FENCE) % 2 != 0:
            errors.append(f"Unbalanced Markdown code fences: {rel}")
        for expression in BANNED:
            hit = expression.search(data)
            if hit:
                errors.append(f"Company/client name in {rel}: {hit.group()}")
        for link in LINK_RE.findall(data):
            if link.startswith(("http:", "https:", "mailto:", "#", "data:")):
                continue
            clean = link.split("#")[0].split("?")[0]
            target = (p.parent / clean).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f"Broken relative link: {rel}: {link}")

    counts = {}
    for label, folder, pattern, expected in FAMILIES:
        cards = list(folder.glob(pattern))
        counts[label] = len(cards)
        if len(cards) != expected:
            errors.append(f"Expected {expected} {label} patterns, got {len(cards)}")
        for card in cards:
            text = card.read_text(encoding="utf-8")
            n = sum(1 for line in text.splitlines() if line.strip() in MERMAID_FENCES)
            if n < 2:
                errors.append(f"Less than 2 diagrams: {card.relative_to(ROOT)}")

    print(f"Files: {len(markdown_files)} | diagrams: {diagrams} | patterns: {counts}")
    if errors:
        for message in errors[:50]:
            print("FAIL:", message)
        print(f"FAILED: {len(errors)} issues")
        return 1
    print("PASS: 55 fiches, Mermaid sources, internal links, restricted company names")
    return 0


if __name__ == "__main__":
    sys.exit(audit())
