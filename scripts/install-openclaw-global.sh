#!/bin/bash
# install-openclaw-global.sh — Install polyagent skills into OpenClaw global paths
#
# Usage:
#   ./scripts/install-openclaw-global.sh [copy|link]
#
# Examples:
#   ./scripts/install-openclaw-global.sh copy   # Copy + normalize SKILL.md frontmatter
#   ./scripts/install-openclaw-global.sh link   # Symlink skills/common-skills for live editing

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
BACKUP_CREATED="false"
MANIFEST_FILE="$OPENCLAW_HOME/.openclaw-install-manifest"
MANAGED_TAG="install-openclaw-global.sh"
MANAGED_MARKER_KEY="polyagent-managed-by"

echo "=== polyagent-skills → OpenClaw global installer ==="
echo "Mode:          $MODE"
echo "OpenClaw home: $OPENCLAW_HOME"
echo ""

mkdir -p "$OPENCLAW_HOME"
printf "# openclaw install manifest\n# format: <path>\\t<kind>\\t<tag>\n" > "$MANIFEST_FILE"

record_manifest() {
    local path="$1"
    local kind="$2"
    printf "%s\t%s\t%s\n" "$path" "$kind" "$MANAGED_TAG" >> "$MANIFEST_FILE"
}

mark_dir_managed() {
    local dir="$1"
    cat > "$dir/.polyagent-managed" <<EOF
$MANAGED_MARKER_KEY: $MANAGED_TAG
source-repo: $REPO_DIR
EOF
}

backup_if_exists() {
    local path="$1"
    local safe_name target
    if [ -e "$path" ] || [ -L "$path" ]; then
        if [ "$BACKUP_CREATED" = "false" ]; then
            mkdir -p "$BACKUP_DIR"
            BACKUP_CREATED="true"
        fi
        safe_name="${path#/}"
        safe_name="${safe_name//\//__}"
        target="$BACKUP_DIR/$safe_name"
        mv "$path" "$target"
        echo "  Backed up: $path -> $target"
    fi
}

extract_skill_name() {
    local src="$1"
    sed -n 's/^name:[[:space:]]*//p' "$src" | head -n 1
}

extract_skill_description() {
    local src="$1"
    awk '
BEGIN{fm=0;seen=0;block=0;desc=""}
/^---$/{
  if(!seen){seen=1;fm=1;next}
  if(fm){fm=0;exit}
}
fm{
  if($0 ~ /^description:[[:space:]]*>/){block=1;next}
  if(block){
    if($0 ~ /^[A-Za-z0-9_-]+:[[:space:]]*/){block=0}
    else{
      line=$0
      sub(/^[[:space:]]+/, "", line)
      if(line!="") desc=desc line " "
      next
    }
  }
  if($0 ~ /^description:[[:space:]]*/){
    line=$0
    sub(/^description:[[:space:]]*/, "", line)
    desc=line
  }
}
END{
  gsub(/[[:space:]]+$/, "", desc)
  print desc
}' "$src"
}

extract_skill_body() {
    local src="$1"
    awk '
BEGIN{fm=0;seen=0}
NR==1 && $0=="---"{seen=1;fm=1;next}
fm && $0=="---"{fm=0;next}
!fm{print}
' "$src"
}

normalize_skill_markdown() {
    local src="$1"
    local dst="$2"
    local fallback_name="$3"
    local name description body esc_description

    name="$(extract_skill_name "$src")"
    if [ -z "$name" ]; then
        name="$fallback_name"
    fi

    description="$(extract_skill_description "$src")"
    if [ -z "$description" ]; then
        description="Portable polyagent skill: $name"
    fi

    body="$(extract_skill_body "$src")"
    esc_description="${description//\\/\\\\}"
    esc_description="${esc_description//\"/\\\"}"

    {
        echo "---"
        echo "name: $name"
        echo "description: \"$esc_description\""
        echo "---"
        echo ""
        printf "%s\n" "$body"
    } > "$dst"
}

install_copy_mode() {
    echo "Installing in copy mode..."
    mkdir -p "$TARGET_SKILLS_DIR"
    mark_dir_managed "$TARGET_SKILLS_DIR"
    record_manifest "$TARGET_SKILLS_DIR" "dir"

    for src_dir in "$SOURCE_SKILLS_DIR"/*; do
        [ -d "$src_dir" ] || continue
        skill_name="$(basename "$src_dir")"
        dst_dir="$TARGET_SKILLS_DIR/$skill_name"

        backup_if_exists "$dst_dir"
        mkdir -p "$dst_dir"
        cp -a "$src_dir/." "$dst_dir/"

        if [ -f "$dst_dir/SKILL.md" ]; then
            normalize_skill_markdown "$src_dir/SKILL.md" "$dst_dir/SKILL.md" "$skill_name"
        fi
        echo "  ✓ Installed skill: $skill_name"
    done

    backup_if_exists "$TARGET_COMMON_DIR"
    mkdir -p "$TARGET_COMMON_DIR"
    cp -a "$SOURCE_COMMON_DIR/." "$TARGET_COMMON_DIR/"
    mark_dir_managed "$TARGET_COMMON_DIR"
    record_manifest "$TARGET_COMMON_DIR" "dir"
    echo "  ✓ Installed: $TARGET_COMMON_DIR"
}

install_link_mode() {
    echo "Installing in link mode..."
    mkdir -p "$OPENCLAW_HOME"

    backup_if_exists "$TARGET_SKILLS_DIR"
    backup_if_exists "$TARGET_COMMON_DIR"

    ln -s "$SOURCE_SKILLS_DIR" "$TARGET_SKILLS_DIR"
    ln -s "$SOURCE_COMMON_DIR" "$TARGET_COMMON_DIR"
    record_manifest "$TARGET_SKILLS_DIR" "symlink"
    record_manifest "$TARGET_COMMON_DIR" "symlink"

    echo "  ✓ Linked: $TARGET_SKILLS_DIR -> $SOURCE_SKILLS_DIR"
    echo "  ✓ Linked: $TARGET_COMMON_DIR -> $SOURCE_COMMON_DIR"
    echo "  ! Note: link mode does not normalize SKILL.md frontmatter."
}

if [ "$MODE" = "copy" ]; then
    install_copy_mode
else
    install_link_mode
fi

echo ""
echo "=== Installation complete ==="
echo "Manifest: $MANIFEST_FILE"
echo "Next steps:"
echo "  1) Restart OpenClaw gateway (or run a new agent session)."
echo "  2) Verify with: openclaw skills list | rg -i 'requirement-study|repo-bootstrap|remote-ops'"
echo "  3) Check readiness with: openclaw skills check"
