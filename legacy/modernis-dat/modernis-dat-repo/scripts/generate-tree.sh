#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
( cd "$ROOT" && find . -maxdepth 3 -type f | sort ) > "$ROOT/docs/TREE.txt"
echo "OK: docs/TREE.txt"
