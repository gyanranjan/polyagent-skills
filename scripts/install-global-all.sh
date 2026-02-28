#!/bin/bash
# install-global-all.sh - One-time global install for Codex, Kiro, Gemini, OpenClaw
#
# Usage:
#   ./scripts/install-global-all.sh [copy|link]
#
# Notes:
# - "copy" (default): copies normalized skills into ~/.polyagent-skills and ~/.openclaw/skills
# - "link": symlinks ~/.polyagent-skills/{skills,common-skills} to this repo and still
#   creates a normalized copy for OpenClaw under ~/.openclaw/skills (required by OpenClaw parser)
#
# WARNING: This script replaces global agent config files (~/.codex/AGENTS.md,
# ~/.kiro/specs/polyagent-skills.md, ~/.gemini/instructions.md). Existing files
# are backed up before replacement.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
MODE="${1:-copy}"

if [ "$MODE" != "copy" ] && [ "$MODE" != "link" ]; then
    echo "Error: mode must be 'copy' or 'link'"
    echo "Usage: $0 [copy|link]"
    exit 1
fi

GLOBAL_ROOT="${POLYAGENT_HOME:-$HOME/.polyagent-skills}"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"

GLOBAL_SKILLS_DIR="$GLOBAL_ROOT/skills"
GLOBAL_COMMON_DIR="$GLOBAL_ROOT/common-skills"
OPENCLAW_SKILLS_DIR="$OPENCLAW_HOME/skills"
OPENCLAW_COMMON_DIR="$OPENCLAW_HOME/common-skills"

BACKUP_DIR="$HOME/.polyagent-backup/$(date +%Y%m%d_%H%M%S)"
MANIFEST_FILE="$GLOBAL_ROOT/.global-install-manifest"
MANAGED_TAG="install-global-all.sh"

# shellcheck source=lib-common.sh
source "$SCRIPT_DIR/lib-common.sh"

mkdir -p "$GLOBAL_ROOT" "$OPENCLAW_HOME" "$HOME/.codex" "$HOME/.kiro/specs" "$HOME/.gemini"
mkdir -p "$(dirname "$MANIFEST_FILE")"
printf "# polyagent global install manifest\n# format: <path>\\t<kind>\\t<tag>\n" > "$MANIFEST_FILE"

write_codex_global_instructions() {
    local path="$HOME/.codex/AGENTS.md"
    if [ -e "$path" ]; then
        echo "  Note: Existing $path will be backed up and replaced."
    fi
    backup_if_exists "$path"
    cat > "$path" <<EOF
<!-- $MANAGED_MARKER_KEY: $MANAGED_TAG -->
# Agent Instructions - polyagent-skills (global)

You have access to a portable skill library in:
- \`$GLOBAL_SKILLS_DIR\`
- \`$GLOBAL_COMMON_DIR\`

When you receive a task:
1. Check \`$GLOBAL_SKILLS_DIR\` for a matching skill by reading each SKILL.md description.
2. Read the full SKILL.md for the matched skill.
3. Follow its Process steps in order.
4. Apply referenced common-skills from \`$GLOBAL_COMMON_DIR\`.
5. Deliver in the specified Output Format.
EOF
    record_manifest "$path" "file"
    echo "  Wrote Codex global config: $path"
}

write_kiro_global_instructions() {
    local path="$HOME/.kiro/specs/polyagent-skills.md"
    if [ -e "$path" ]; then
        echo "  Note: Existing $path will be backed up and replaced."
    fi
    backup_if_exists "$path"
    cat > "$path" <<EOF
<!-- $MANAGED_MARKER_KEY: $MANAGED_TAG -->
# Skill Library Integration - polyagent-skills (global)

When working on tasks, check this global skills directory for a matching skill:
- \`$GLOBAL_SKILLS_DIR\`

Each skill has a \`SKILL.md\` with step-by-step instructions to follow.
Shared conventions are in:
- \`$GLOBAL_COMMON_DIR\`

Usage:
1. Match the user's task to a skill.
2. Read the skill's SKILL.md fully.
3. Follow the Process steps.
4. Apply common-skills when referenced.
5. Deliver in the specified format.
EOF
    record_manifest "$path" "file"
    echo "  Wrote Kiro global config: $path"
}

write_gemini_global_instructions() {
    local path="$HOME/.gemini/instructions.md"
    if [ -e "$path" ]; then
        echo "  Note: Existing $path will be backed up and replaced."
    fi
    backup_if_exists "$path"
    cat > "$path" <<EOF
<!-- $MANAGED_MARKER_KEY: $MANAGED_TAG -->
# Agent Instructions - polyagent-skills (global)

You have access to a global portable skill library:
- \`$GLOBAL_SKILLS_DIR\`
- \`$GLOBAL_COMMON_DIR\`

For any task, first check \`$GLOBAL_SKILLS_DIR\` for a matching skill.
Read its SKILL.md and follow the instructions.
Apply common-skills when referenced from \`$GLOBAL_COMMON_DIR\`.
EOF
    record_manifest "$path" "file"
    echo "  Wrote Gemini global config: $path"
}

echo "=== polyagent global installer ==="
echo "Mode: $MODE"
echo "Global root: $GLOBAL_ROOT"
echo "OpenClaw home: $OPENCLAW_HOME"
echo ""

if [ "$MODE" = "copy" ]; then
    echo "Installing shared global library (copy mode)..."
    install_normalized_skills_copy "$REPO_DIR/skills" "$REPO_DIR/common-skills" "$GLOBAL_SKILLS_DIR" "$GLOBAL_COMMON_DIR"
else
    echo "Installing shared global library (link mode)..."
    backup_if_exists "$GLOBAL_SKILLS_DIR"
    backup_if_exists "$GLOBAL_COMMON_DIR"
    ln -s "$REPO_DIR/skills" "$GLOBAL_SKILLS_DIR"
    ln -s "$REPO_DIR/common-skills" "$GLOBAL_COMMON_DIR"
    record_manifest "$GLOBAL_SKILLS_DIR" "symlink"
    record_manifest "$GLOBAL_COMMON_DIR" "symlink"
    echo "  Linked: $GLOBAL_SKILLS_DIR -> $REPO_DIR/skills"
    echo "  Linked: $GLOBAL_COMMON_DIR -> $REPO_DIR/common-skills"
fi

echo ""
echo "Installing OpenClaw global skills (normalized copy — required by OpenClaw parser)..."
install_normalized_skills_copy "$REPO_DIR/skills" "$REPO_DIR/common-skills" "$OPENCLAW_SKILLS_DIR" "$OPENCLAW_COMMON_DIR"

echo ""
echo "Writing global agent configs..."
echo "  (Existing config files will be backed up before replacement.)"
write_codex_global_instructions
write_kiro_global_instructions
write_gemini_global_instructions

echo ""
echo "=== Done ==="
echo "Manifest: $MANIFEST_FILE"
echo "Per-project installer is unchanged: ./scripts/install-to-project.sh"
echo "Uninstall safely with: ./scripts/uninstall-global-all.sh --dry-run"
echo ""
echo "Verify:"
echo "  openclaw skills list | grep -i 'requirement-study\|repo-bootstrap\|remote-ops'"
echo "  openclaw skills check"
echo ""
echo "If OpenClaw gateway is running, restart it to reload skills."
