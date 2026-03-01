#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/init-requirement-issues.sh <requirements.md> <owner/repo> [--apply]

Behavior:
  - Parses REQ IDs and titles from the requirement markdown file.
  - Default mode is dry-run (prints commands).
  - With --apply, creates GitHub issues via gh CLI.

Expected requirement block:
  **[REQ-001]** Functional
  **Title:** User can log in
EOF
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 1
fi

REQ_FILE="$1"
REPO="$2"
MODE="${3:-}"

if [[ ! -f "$REQ_FILE" ]]; then
  echo "error=requirements_file_not_found path=$REQ_FILE" >&2
  exit 1
fi

APPLY="no"
if [[ "$MODE" == "--apply" ]]; then
  APPLY="yes"
elif [[ -n "$MODE" ]]; then
  echo "error=unknown_mode mode=$MODE" >&2
  usage
  exit 1
fi

if [[ "$APPLY" == "yes" ]] && ! command -v gh >/dev/null 2>&1; then
  echo "error=gh_not_found; install GitHub CLI or run dry-run mode" >&2
  exit 1
fi

extract_pairs() {
  awk '
    function trim(s){ sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    /^\*\*\[REQ-[0-9]+\]\*\*/ {
      if (id != "") {
        if (title == "") title = "Requirement " id
        print id "|" title
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
        print id "|" title
      }
    }
  ' "$REQ_FILE"
}

COUNT=0
while IFS='|' read -r req_id req_title; do
  [[ -z "$req_id" ]] && continue
  COUNT=$((COUNT + 1))

  issue_title="$req_id: $req_title"
  issue_body=$(
    cat <<EOF
Auto-generated from requirement document.

- Requirement ID: $req_id
- Source file: $REQ_FILE

Please add acceptance criteria, labels, and milestone.
EOF
  )

  if [[ "$APPLY" == "yes" ]]; then
    gh issue create \
      --repo "$REPO" \
      --title "$issue_title" \
      --body "$issue_body" \
      --label "type:req"
  else
    printf 'gh issue create --repo %q --title %q --body %q --label %q\n' \
      "$REPO" "$issue_title" "$issue_body" "type:req"
  fi
done < <(extract_pairs)

if [[ "$COUNT" -eq 0 ]]; then
  echo "warning=no_req_ids_found in $REQ_FILE"
else
  echo "parsed_requirements=$COUNT mode=$APPLY"
fi
