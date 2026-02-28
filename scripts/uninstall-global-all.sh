#!/bin/bash
# uninstall-global-all.sh - Remove only files managed by global installers
#
# Usage:
#   ./scripts/uninstall-global-all.sh [--dry-run]
#
# Behavior:
# - Reads installer manifests written by:
#   - scripts/install-global-all.sh
#   - scripts/install-openclaw-global.sh
# - Removes only paths listed in manifests and only when ownership markers match.

set -euo pipefail

DRY_RUN="false"
if [ "${1:-}" = "--dry-run" ]; then
    DRY_RUN="true"
fi

GLOBAL_ROOT="${POLYAGENT_HOME:-$HOME/.polyagent-skills}"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"

GLOBAL_MANIFEST="$GLOBAL_ROOT/.global-install-manifest"
OPENCLAW_MANIFEST="$OPENCLAW_HOME/.openclaw-install-manifest"
MANAGED_MARKER_KEY="polyagent-managed-by"

remove_path() {
    local path="$1"
    if [ "$DRY_RUN" = "true" ]; then
        echo "  [dry-run] rm -rf $path"
    else
        rm -rf "$path"
        echo "  Removed: $path"
    fi
}

maybe_remove_entry() {
    local path="$1"
    local kind="$2"
    local tag="$3"

    [ -n "$path" ] || return 0
    [ -n "$kind" ] || return 0
    [ -n "$tag" ] || return 0

    case "$kind" in
        file)
            if [ -f "$path" ] && grep -q "$MANAGED_MARKER_KEY: $tag" "$path"; then
                remove_path "$path"
            else
                echo "  Skipped (unmanaged/missing file): $path"
            fi
            ;;
        dir)
            if [ -d "$path" ] && [ -f "$path/.polyagent-managed" ] && grep -q "$MANAGED_MARKER_KEY: $tag" "$path/.polyagent-managed"; then
                remove_path "$path"
            else
                echo "  Skipped (unmanaged/missing dir): $path"
            fi
            ;;
        symlink)
            if [ -L "$path" ]; then
                remove_path "$path"
            else
                echo "  Skipped (missing symlink): $path"
            fi
            ;;
        *)
            echo "  Skipped (unknown entry kind '$kind'): $path"
            ;;
    esac
}

process_manifest() {
    local manifest="$1"
    local path kind tag

    if [ ! -f "$manifest" ]; then
        echo "Manifest not found: $manifest"
        return 0
    fi

    echo "Processing manifest: $manifest"
    while IFS=$'\t' read -r path kind tag; do
        [ -z "${path:-}" ] && continue
        case "$path" in
            \#*) continue ;;
        esac
        maybe_remove_entry "$path" "$kind" "$tag"
    done < "$manifest"

    if [ "$DRY_RUN" = "true" ]; then
        echo "  [dry-run] rm -f $manifest"
    else
        rm -f "$manifest"
        echo "  Removed manifest: $manifest"
    fi
}

echo "=== polyagent global uninstall ==="
echo "Dry run: $DRY_RUN"
echo ""

process_manifest "$GLOBAL_MANIFEST"
echo ""
process_manifest "$OPENCLAW_MANIFEST"
echo ""
echo "Done."
echo "Only manifest-managed paths were targeted."
