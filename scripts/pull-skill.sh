#!/bin/bash
# pull-skill.sh — Pull a skill from skills.sh and convert to portable format
#
# Usage: ./scripts/pull-skill.sh <skill-url-or-name>
#
# This script:
# 1. Downloads the .skill file from skills.sh
# 2. Extracts it (skill files are ZIP archives)
# 3. Places it in skills/<name>/
# 4. Flags any agent-specific syntax for manual review

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

SKILL_INPUT="${1:?Usage: $0 <skill-url-or-name>}"

echo "=== Pull skill from skills.sh ==="

# Determine if input is URL or name
if [[ "$SKILL_INPUT" == http* ]]; then
    SKILL_URL="$SKILL_INPUT"
    SKILL_NAME=$(basename "$SKILL_INPUT" .skill)
else
    SKILL_NAME="$SKILL_INPUT"
    SKILL_URL="https://skills.sh/download/${SKILL_NAME}.skill"
fi

DEST="$REPO_DIR/skills/$SKILL_NAME"
TEMP_DIR=$(mktemp -d)

echo "Skill:       $SKILL_NAME"
echo "Destination: $DEST"
echo ""

# Download
echo "Downloading..."
if command -v curl &> /dev/null; then
    curl -sL "$SKILL_URL" -o "$TEMP_DIR/$SKILL_NAME.skill" || {
        echo "Error: Could not download from $SKILL_URL"
        echo "You may need to download manually and place in $DEST/"
        rm -rf "$TEMP_DIR"
        exit 1
    }
elif command -v wget &> /dev/null; then
    wget -q "$SKILL_URL" -O "$TEMP_DIR/$SKILL_NAME.skill" || {
        echo "Error: Could not download from $SKILL_URL"
        rm -rf "$TEMP_DIR"
        exit 1
    }
fi

# Extract (.skill files are ZIP archives)
echo "Extracting..."
mkdir -p "$TEMP_DIR/extracted"
unzip -q "$TEMP_DIR/$SKILL_NAME.skill" -d "$TEMP_DIR/extracted" 2>/dev/null || {
    echo "Note: File may not be a ZIP. Treating as plain SKILL.md."
    mkdir -p "$TEMP_DIR/extracted"
    cp "$TEMP_DIR/$SKILL_NAME.skill" "$TEMP_DIR/extracted/SKILL.md"
}

# Copy to destination
echo "Installing to $DEST..."
mkdir -p "$DEST/references"
cp -r "$TEMP_DIR/extracted/"* "$DEST/"

# Check for agent-specific syntax
echo ""
echo "=== Portability Check ==="

ISSUES=0
if [ -f "$DEST/SKILL.md" ]; then
    # Check for Claude-specific patterns
    if grep -qiE '(</?(tool|function|artifact|antml))|(/slash-command)|(@file)' "$DEST/SKILL.md"; then
        echo "⚠️  Found potential Claude-specific syntax in SKILL.md"
        echo "   Review and replace with portable alternatives."
        ISSUES=$((ISSUES + 1))
    fi

    # Check for absolute paths
    if grep -qE '(/mnt/|/home/|/tmp/|C:\\)' "$DEST/SKILL.md"; then
        echo "⚠️  Found absolute paths in SKILL.md"
        echo "   Replace with relative paths."
        ISSUES=$((ISSUES + 1))
    fi

    # Check for missing frontmatter
    if ! head -1 "$DEST/SKILL.md" | grep -q "^---"; then
        echo "⚠️  Missing YAML frontmatter"
        echo "   Add name, description, tags, version fields."
        ISSUES=$((ISSUES + 1))
    fi
fi

if [ "$ISSUES" -eq 0 ]; then
    echo "✓ No portability issues detected"
else
    echo ""
    echo "$ISSUES issue(s) found — review $DEST/SKILL.md before using"
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "=== Done ==="
echo "Skill installed at: $DEST/"
echo "Run ./scripts/sync-adapters.sh to update adapter files."
