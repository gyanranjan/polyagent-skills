#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/sync-agent-todo.sh <agent.todo.md> <requirements.md> [spec.md]

Synchronizes managed traceability content into agent.todo.md:
  - Requirement IDs parsed from requirements.md
  - Design readiness snapshot parsed from spec.md (optional)

It updates/creates a managed block between:
  <!-- BEGIN AUTO-SYNC -->
  <!-- END AUTO-SYNC -->
EOF
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 1
fi

TODO_FILE="$1"
REQ_FILE="$2"
SPEC_FILE="${3:-}"

if [[ ! -f "$TODO_FILE" ]]; then
  echo "error=todo_file_not_found path=$TODO_FILE" >&2
  exit 1
fi
if [[ ! -f "$REQ_FILE" ]]; then
  echo "error=requirements_file_not_found path=$REQ_FILE" >&2
  exit 1
fi
if [[ -n "$SPEC_FILE" && ! -f "$SPEC_FILE" ]]; then
  echo "error=spec_file_not_found path=$SPEC_FILE" >&2
  exit 1
fi

tmp_block="$(mktemp)"
tmp_out="$(mktemp)"
trap 'rm -f "$tmp_block" "$tmp_out"' EXIT

today="$(date -u +%F)"
now_utc="$(date -u '+%Y-%m-%d %H:%M')"

extract_req_rows() {
  awk '
    function trim(s){ sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    /^\*\*\[REQ-[0-9]+\]\*\*/ {
      if (id != "") {
        if (title == "") title = "Requirement " id
        print "| " id " | " title " | (create issue) | Open | [owner] |"
      }
      match($0, /\[REQ-[0-9]+\]/)
      id = substr($0, RSTART+1, RLENGTH-2)
      title = ""
      next
    }
    id != "" && /^\*\*Title:\*\*/ {
      t = $0
      sub(/^\*\*Title:\*\*[[:space:]]*/, "", t)
      title = trim(t)
      next
    }
    END {
      if (id != "") {
        if (title == "") title = "Requirement " id
        print "| " id " | " title " | (create issue) | Open | [owner] |"
      }
    }
  ' "$REQ_FILE"
}

extract_design_rows() {
  local file="$1"
  awk -v src="$file" '
    BEGIN {in_section=0}
    /^##[[:space:]]+Design Readiness/ {in_section=1; next}
    /^##[[:space:]]+/ && in_section==1 {in_section=0}
    in_section==1 && /^\|/ {
      if ($0 ~ /^\|[-[:space:]\|]+\|$/) next
      n=split($0, a, "|")
      if (n < 3) next
      c1=a[2]; c2=a[3]
      gsub(/^[ \t]+|[ \t]+$/, "", c1)
      gsub(/^[ \t]+|[ \t]+$/, "", c2)
      if (c1 == "" || c1 == "Checkpoint") next
      print "| " c1 " | " c2 " | " src " |"
    }
  ' "$file"
}

{
  echo "<!-- BEGIN AUTO-SYNC -->"
  echo "## Auto-Synced Traceability (Managed)"
  echo
  echo "- Synced At (UTC): $now_utc"
  echo "- Requirements Source: $REQ_FILE"
  if [[ -n "$SPEC_FILE" ]]; then
    echo "- Spec Source: $SPEC_FILE"
  else
    echo "- Spec Source: (not provided)"
  fi
  echo
  echo "### Requirements Snapshot"
  echo
  echo "| Requirement ID | Title | GitHub Issue | Status | Owner |"
  echo "|----------------|-------|--------------|--------|-------|"
  req_rows="$(extract_req_rows)"
  if [[ -n "$req_rows" ]]; then
    echo "$req_rows"
  else
    echo "| (none) | | | | |"
  fi
  echo
  echo "### Design Readiness Snapshot"
  echo
  echo "| Checkpoint | Status | Source |"
  echo "|------------|--------|--------|"
  if [[ -n "$SPEC_FILE" ]]; then
    dr_rows="$(extract_design_rows "$SPEC_FILE")"
    if [[ -n "$dr_rows" ]]; then
      echo "$dr_rows"
    else
      echo "| (no design readiness table found) | Open | $SPEC_FILE |"
    fi
  else
    echo "| (spec not provided) | Open | - |"
  fi
  echo
  echo "<!-- END AUTO-SYNC -->"
} > "$tmp_block"

if grep -q "<!-- BEGIN AUTO-SYNC -->" "$TODO_FILE"; then
  awk -v repl="$tmp_block" '
    BEGIN {in_block=0}
    /<!-- BEGIN AUTO-SYNC -->/ {
      while ((getline line < repl) > 0) print line
      close(repl)
      in_block=1
      next
    }
    /<!-- END AUTO-SYNC -->/ {
      in_block=0
      next
    }
    in_block==0 {print}
  ' "$TODO_FILE" > "$tmp_out"
else
  cat "$TODO_FILE" > "$tmp_out"
  echo >> "$tmp_out"
  cat "$tmp_block" >> "$tmp_out"
fi

sed -E "s/^- Last Updated: .*/- Last Updated: $today/" "$tmp_out" > "$TODO_FILE"

echo "synced_todo=$TODO_FILE"
