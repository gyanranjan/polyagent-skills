#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/design-readiness-check.sh [--allow-open] <doc1.md> [doc2.md ...]

Checks each document for a "Design Readiness" section and validates required checkpoints:
  - Architecture pattern
  - Language/runtime
  - Database strategy
  - Logging/observability baseline

Default behavior fails if any required checkpoint is Open or missing.
Use --allow-open to only validate structure and presence.
EOF
}

ALLOW_OPEN="no"
if [[ "${1:-}" == "--allow-open" ]]; then
  ALLOW_OPEN="yes"
  shift
fi

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

failures=0

trim() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

extract_design_section() {
  local file="$1"
  awk '
    BEGIN {in_section=0}
    /^##[[:space:]]+Design Readiness/ {in_section=1; next}
    /^##[[:space:]]+/ && in_section==1 {in_section=0}
    in_section==1 {print}
  ' "$file"
}

for file in "$@"; do
  if [[ ! -f "$file" ]]; then
    echo "FAIL file_not_found: $file"
    failures=$((failures + 1))
    continue
  fi

  section="$(extract_design_section "$file")"
  if [[ -z "$section" ]]; then
    echo "FAIL missing_design_readiness_section: $file"
    failures=$((failures + 1))
    continue
  fi

  arch_status=""
  lang_status=""
  db_status=""
  log_status=""

  while IFS= read -r line; do
    [[ "$line" =~ ^\| ]] || continue
    [[ "$line" =~ ^\|[-[:space:]\|]+\|$ ]] && continue

    col1="$(trim "$(echo "$line" | awk -F'|' '{print $2}')")"
    col2="$(trim "$(echo "$line" | awk -F'|' '{print $3}')")"
    [[ -z "$col1" || -z "$col2" ]] && continue

    lc1="$(echo "$col1" | tr '[:upper:]' '[:lower:]')"
    lc2="$(echo "$col2" | tr '[:upper:]' '[:lower:]')"

    case "$lc1" in
      *architecture*pattern*) arch_status="$lc2" ;;
      *language*runtime*) lang_status="$lc2" ;;
      *database*strategy*) db_status="$lc2" ;;
      *logging*observability*baseline*) log_status="$lc2" ;;
    esac
  done <<< "$section"

  missing=0
  [[ -z "$arch_status" ]] && { echo "FAIL missing_checkpoint(architecture pattern): $file"; missing=1; }
  [[ -z "$lang_status" ]] && { echo "FAIL missing_checkpoint(language/runtime): $file"; missing=1; }
  [[ -z "$db_status" ]] && { echo "FAIL missing_checkpoint(database strategy): $file"; missing=1; }
  [[ -z "$log_status" ]] && { echo "FAIL missing_checkpoint(logging/observability baseline): $file"; missing=1; }

  if [[ "$missing" -eq 1 ]]; then
    failures=$((failures + 1))
    continue
  fi

  if [[ "$ALLOW_OPEN" == "no" ]]; then
    open_count=0
    for status in "$arch_status" "$lang_status" "$db_status" "$log_status"; do
      if [[ "$status" == *open* ]]; then
        open_count=$((open_count + 1))
      fi
    done
    if [[ "$open_count" -gt 0 ]]; then
      echo "FAIL open_checkpoints=$open_count: $file"
      failures=$((failures + 1))
      continue
    fi
  fi

  echo "PASS design_readiness: $file"
done

if [[ "$failures" -gt 0 ]]; then
  echo "design_readiness_check=failed count=$failures"
  exit 1
fi

echo "design_readiness_check=passed"
