#!/usr/bin/env bash
# gate-status-check.sh — Check and report development lifecycle gate status
# Usage: ./scripts/gate-status-check.sh [path-to-agent-todo]
#
# Reads the Gate Status table from agent.todo.md and reports:
# - Current gate (first non-Passed gate)
# - Any skipped gates
# - Overall readiness for implementation
#
# Exit codes:
#   0 — Gates 0-2 passed (or skipped), ready for implementation
#   1 — Not ready for implementation (gates incomplete)
#   2 — No gate status section found

set -euo pipefail

# Source shared library if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/lib-common.sh" ]]; then
  # shellcheck source=lib-common.sh
  source "$SCRIPT_DIR/lib-common.sh"
fi

TODO_FILE="${1:-agent.todo.md}"

if [[ ! -f "$TODO_FILE" ]]; then
  echo "ERROR: $TODO_FILE not found"
  echo "Hint: Run from the repository root or pass the path as an argument."
  exit 2
fi

# Check for Gate Status section
if ! grep -q "## Gate Status" "$TODO_FILE"; then
  echo "WARNING: No '## Gate Status' section found in $TODO_FILE"
  echo ""
  echo "This project has not initialized the development lifecycle gates."
  echo "To start, add the gate status template from:"
  echo "  common-skills/development-lifecycle-gates.md"
  exit 2
fi

echo "=== Development Lifecycle Gate Status ==="
echo ""

# Extract the gate status table (between ## Gate Status and the next ## heading)
gate_section=$(awk '/^## Gate Status/{found=1; next} /^## /{if(found) exit} found' "$TODO_FILE")

# Parse each gate row
current_gate=""
skipped_gates=""
all_pre_impl_passed=true
g3_status=""

while IFS='|' read -r _ gate name status evidence skip_reason _; do
  # Skip header and separator rows
  gate=$(echo "$gate" | xargs)
  name=$(echo "$name" | xargs)
  status=$(echo "$status" | xargs)
  skip_reason=$(echo "$skip_reason" | xargs)

  # Skip non-gate rows
  case "$gate" in
    G[0-6]) ;;
    *) continue ;;
  esac

  # Display gate status
  case "$status" in
    "Passed")
      printf "  %-4s %-16s ✅ Passed\n" "$gate" "$name"
      ;;
    "Skipped")
      printf "  %-4s %-16s ⏭  Skipped (%s)\n" "$gate" "$name" "$skip_reason"
      skipped_gates="$skipped_gates $gate"
      ;;
    "In Progress")
      printf "  %-4s %-16s 🔄 In Progress\n" "$gate" "$name"
      if [[ -z "$current_gate" ]]; then
        current_gate="$gate: $name"
      fi
      ;;
    "N/A")
      printf "  %-4s %-16s ➖ N/A\n" "$gate" "$name"
      ;;
    "Not Started")
      printf "  %-4s %-16s ⬜ Not Started\n" "$gate" "$name"
      if [[ -z "$current_gate" ]]; then
        current_gate="$gate: $name"
      fi
      ;;
    *)
      printf "  %-4s %-16s ❓ %s\n" "$gate" "$name" "$status"
      ;;
  esac

  # Check if pre-implementation gates (G0-G2) are all passed/skipped/N/A
  case "$gate" in
    G[0-2])
      case "$status" in
        "Passed"|"Skipped"|"N/A") ;;
        *) all_pre_impl_passed=false ;;
      esac
      ;;
    G3)
      g3_status="$status"
      ;;
  esac

done <<< "$gate_section"

echo ""

# Report current state
if [[ -n "$current_gate" ]]; then
  echo "Current gate: $current_gate"
else
  echo "Current gate: All gates processed"
fi

if [[ -n "$skipped_gates" ]]; then
  echo "Skipped gates:$skipped_gates"
fi

echo ""

# Gate 3 is conditional. Only block when it has started but is incomplete.
if [[ "$g3_status" == "In Progress" ]]; then
  all_pre_impl_passed=false
fi

if [[ "$g3_status" == "Not Started" ]]; then
  echo "Note: G3 is conditional. If no high-risk spike is needed, mark G3 as N/A."
  echo ""
fi

# Implementation readiness verdict
if $all_pre_impl_passed; then
  echo "✅ READY FOR IMPLEMENTATION — Gates 0–2 (and 3 if applicable) are cleared."
  exit 0
else
  echo "⛔ NOT READY FOR IMPLEMENTATION — Complete or skip pending gates first."
  echo ""
  echo "To skip a gate, the user must explicitly say 'skip to [phase]'."
  echo "See: common-skills/development-lifecycle-gates.md"
  exit 1
fi
