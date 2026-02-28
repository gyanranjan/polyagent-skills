#!/bin/bash
# install-openclaw-global.sh — Install polyagent skills into OpenClaw global paths
#
# Usage:
#   ./scripts/install-openclaw-global.sh [copy|link]
#
# Examples:
#   ./scripts/install-openclaw-global.sh copy   # Copy + normalize SKILL.md frontmatter
#   ./scripts/install-openclaw-global.sh link   # Symlink skills, but still normalize SKILL.md
#
# Note: Both modes normalize SKILL.md frontmatter because OpenClaw's parser
# requires single-line frontmatter keys (see KNOWN_ISSUES.md KI-007).
# In link mode, skills/ and common-skills/ are symlinked for live editing,
# but each SKILL.md is replaced with a normalized copy.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

MODE="${1:-copy}"
if [ "$MODE" != "copy" ] && [ "$MODE" != "link" ]; then
    echo "Error: mode must be 'copy' or 'link'"
    echo "Usage: $0 [copy|link]"
    exit 1
fi

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
TARGET_SKILLS_DIR="$OPENCLAW_HOME/skills"
TARGET_COMMON_DIR="$OPENCLAW_HOME/common-skills"
SOURCE_SKILLS_DIR="$REPO_DIR/skills"
SOURCE_COMMON_DIR="$REPO_DIR/common-skills"
BACKUP_DIR="$OPENCLAW_HOME/.polyagent-backup/$(date +%Y%m%d_%H%M%S)"
MANIFEST_FILE="$OPENCLAW_HOME/.openclaw-install-manifest"
MANAGED_TAG="install-openclaw-global.sh"

# shellcheck source=lib-common.sh
source "$SCRIPT_DIR/lib-common.sh"

echo "=== polyagent-skills -> OpenClaw global installer ==="
echo "Mode:          $MODE"
echo "OpenClaw home: $OPENCLAW_HOME"
echo ""

mkdir -p "$OPENCLAW_HOME"
printf "# openclaw install manifest\n# format: <path>\\t<kind>\\t<tag>\n" > "$MANIFEST_FILE"

install_link_mode() {
    echo "Installing in link mode (with frontmatter normalization)..."
    mkdir -p "$OPENCLAW_HOME"

    backup_if_exists "$TARGET_SKILLS_DIR"
    backup_if_exists "$TARGET_COMMON_DIR"

    # Copy (not symlink) so we can normalize SKILL.md in place.
    # OpenClaw's parser requires single-line frontmatter (KI-007).
    install_normalized_skills_copy "$SOURCE_SKILLS_DIR" "$SOURCE_COMMON_DIR" "$TARGET_SKILLS_DIR" "$TARGET_COMMON_DIR"

    echo "  Note: link mode still copies and normalizes for OpenClaw parser compatibility."
    echo "  For live-editing with symlinks, use install-global-all.sh link (shared library"
    echo "  is symlinked; OpenClaw still gets a normalized copy)."
}

if [ "$MODE" = "copy" ]; then
    echo "Installing in copy mode..."
    install_normalized_skills_copy "$SOURCE_SKILLS_DIR" "$SOURCE_COMMON_DIR" "$TARGET_SKILLS_DIR" "$TARGET_COMMON_DIR"
else
    install_link_mode
fi

echo ""
echo "=== Installation complete ==="
echo "Manifest: $MANIFEST_FILE"
echo "Next steps:"
echo "  1) Restart OpenClaw gateway (or run a new agent session)."
echo "  2) Verify with: openclaw skills list | grep -i 'requirement-study\|repo-bootstrap\|remote-ops'"
echo "  3) Check readiness with: openclaw skills check"
