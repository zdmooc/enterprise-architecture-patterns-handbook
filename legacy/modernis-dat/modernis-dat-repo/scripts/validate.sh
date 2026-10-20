#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Vérification basique : fichiers clés"
for f in "$ROOT/docs/DAT.md" "$ROOT/matrices/flow-matrix.csv" "$ROOT/security/SECURITY_SHEET.md"; do
  test -f "$f" || { echo "Manquant: $f"; exit 1; }
done

echo "OK"
