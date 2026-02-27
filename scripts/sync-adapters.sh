#!/bin/bash
# sync-adapters.sh — Regenerate skill lists in all adapter files
#
# Scans skills/*/SKILL.md for names and descriptions,
# then updates the "Available Skills" section in each adapter.
#
# Usage: ./scripts/sync-adapters.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$REPO_DIR/skills"

echo "=== Syncing adapters with skill library ==="

# Build skill list from SKILL.md frontmatter
SKILL_LIST=""
for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    skill_file="$skill_dir/SKILL.md"

    if [ ! -f "$skill_file" ]; then
        echo "  Warning: No SKILL.md in $skill_name, skipping"
        continue
    fi

    # Extract description from YAML frontmatter (first line of description)
    description=$(awk '/^description:/{found=1; sub(/^description: *>? */, ""); if(length>0) print; next} found && /^  /{sub(/^  /, ""); print; next} found{exit}' "$skill_file" | head -1 | cut -c1-80)

    if [ -z "$description" ]; then
        description="(no description)"
    fi

    SKILL_LIST="${SKILL_LIST}- \`skills/${skill_name}/\` — ${description}\n"
    echo "  Found: $skill_name"
done

echo ""
echo "Skills found: $(echo -e "$SKILL_LIST" | grep -c "^-" || true)"
echo ""

# For now, print the generated list
# Full auto-replacement can be added when adapter format stabilizes
echo "Generated skill list:"
echo "---"
echo -e "$SKILL_LIST"
echo "---"
echo ""
echo "Copy the above into each adapter's 'Available Skills' section."
echo "Auto-replacement will be added in a future version (see RFC template)."
