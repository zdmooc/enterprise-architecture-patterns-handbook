#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT/dist"
mkdir -p "$DIST"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc n'est pas installé. Installez pandoc puis relancez."
  exit 1
fi

pandoc "$ROOT/docs/DAT.md" -o "$DIST/ModernIS_DAT.pdf"   --metadata title="ModernIS DAT"   --toc --number-sections

echo "OK: $DIST/ModernIS_DAT.pdf"
