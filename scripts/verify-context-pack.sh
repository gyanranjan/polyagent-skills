#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/verify-context-pack.sh <context-pack.md>

Validation checks:
  - required section headings exist
  - Design Readiness table includes required checkpoints
  - basic traceability signal exists (REQ-* or explicit missing note)
EOF
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

PACK="$1"
if [[ ! -f "$PACK" ]]; then
  echo "FAIL file_not_found: $PACK"
  exit 1
fi

required_sections=(
  "^## Session Start$"
  "^## Context Snapshot$"
  "^## Goals and Non-Goals$"
  "^## Active Decisions$"
  "^## Architecture and Runtime$"
  "^## Data and Storage$"
  "^## Observability Baseline$"
  "^## Design Readiness$"
  "^## Current Execution Plan$"
  "^## Open Questions and Risks$"
  "^## Traceability$"
)

failures=0
for pattern in "${required_sections[@]}"; do
  if ! rg -n "$pattern" "$PACK" >/dev/null; then
    echo "FAIL missing_section pattern=$pattern file=$PACK"
    failures=$((failures + 1))
  fi
done

for checkpoint in "Architecture pattern" "Language/runtime" "Database strategy" "Logging/observability baseline"; do
  if ! rg -n "$checkpoint" "$PACK" >/dev/null; then
    echo "FAIL missing_design_checkpoint checkpoint=\"$checkpoint\" file=$PACK"
    failures=$((failures + 1))
  fi
done

if ! rg -n "REQ-[0-9]+|missing requirements" -i "$PACK" >/dev/null; then
  echo "FAIL missing_traceability_signal file=$PACK"
  failures=$((failures + 1))
fi

if [[ "$failures" -gt 0 ]]; then
  echo "context_pack_verification=failed count=$failures"
  exit 1
fi

echo "context_pack_verification=passed file=$PACK"
