#!/bin/bash
# lib-common.sh — Shared functions for polyagent install/uninstall scripts
#
# Source this file from other scripts:
#   source "$(dirname "${BASH_SOURCE[0]}")/lib-common.sh"
#
# Requires the caller to set:
#   REPO_DIR          — path to the polyagent-skills repo root
#   BACKUP_DIR        — path for backups (timestamped)
#   MANIFEST_FILE     — path to the manifest file
#   MANAGED_TAG       — identifier for the installer (e.g. "install-global-all.sh")
#   MANAGED_MARKER_KEY — key used in ownership markers (default: "polyagent-managed-by")

# Guard: only load once
if [ "${_LIB_COMMON_LOADED:-}" = "true" ]; then
    return 0
fi
_LIB_COMMON_LOADED="true"

MANAGED_MARKER_KEY="${MANAGED_MARKER_KEY:-polyagent-managed-by}"
BACKUP_CREATED="false"

# --- Manifest helpers ---

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

# --- Backup helpers ---

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

# --- SKILL.md frontmatter parsing ---

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

# --- Skill installation ---

install_normalized_skills_copy() {
    local source_skills="$1"
    local source_common="$2"
    local target_skills="$3"
    local target_common="$4"
    local skill_name src_dir dst_dir

    backup_if_exists "$target_skills"
    mkdir -p "$target_skills"
    mark_dir_managed "$target_skills"
    record_manifest "$target_skills" "dir"

    for src_dir in "$source_skills"/*; do
        [ -d "$src_dir" ] || continue
        skill_name="$(basename "$src_dir")"
        dst_dir="$target_skills/$skill_name"
        mkdir -p "$dst_dir"
        cp -a "$src_dir/." "$dst_dir/"
        if [ -f "$src_dir/SKILL.md" ]; then
            normalize_skill_markdown "$src_dir/SKILL.md" "$dst_dir/SKILL.md" "$skill_name"
        fi
        echo "  Installed skill: $skill_name -> $target_skills"
    done

    backup_if_exists "$target_common"
    mkdir -p "$target_common"
    cp -a "$source_common/." "$target_common/"
    mark_dir_managed "$target_common"
    record_manifest "$target_common" "dir"
    echo "  Installed common skills -> $target_common"
}
