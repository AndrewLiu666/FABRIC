#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

python -B -u fabric/run_fabric.py \
  --experiment both \
  --run-name "${1:?usage: scripts/run_both.sh RUN_NAME}" \
  --execute
