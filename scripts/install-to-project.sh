#!/bin/bash
# install-to-project.sh — Install polyagent-skills into a target project
#
# Usage:
#   ./scripts/install-to-project.sh /path/to/project [agent|all]
#
# Examples:
#   ./scripts/install-to-project.sh ~/my-app all          # All adapters
#   ./scripts/install-to-project.sh ~/my-app claude-code   # Claude Code only
#   ./scripts/install-to-project.sh ~/my-app codex         # Codex only

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

PROJECT_DIR="${1:?Usage: $0 <project-dir> <agent|all>}"
AGENT="${2:-all}"

# Validate project directory
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory '$PROJECT_DIR' does not exist."
    exit 1
fi

echo "=== polyagent-skills installer ==="
echo "Project: $PROJECT_DIR"
echo "Agent:   $AGENT"
echo ""

# Backup existing files
backup_if_exists() {
    local file="$1"
    if [ -e "$file" ]; then
        local backup_dir="$PROJECT_DIR/.polyagent-backup/$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_dir"
        cp -r "$file" "$backup_dir/"
        echo "  Backed up: $file → $backup_dir/"
    fi
}

# Copy skills and common-skills
echo "Copying skill library..."
mkdir -p "$PROJECT_DIR/skills"
mkdir -p "$PROJECT_DIR/common-skills"
cp -r "$REPO_DIR/skills/"* "$PROJECT_DIR/skills/"
cp -r "$REPO_DIR/common-skills/"* "$PROJECT_DIR/common-skills/"
echo "  ✓ Skills and common-skills copied"

# Install adapter(s)
install_adapter() {
    local agent_name="$1"
    echo "Installing adapter: $agent_name"

    case "$agent_name" in
        claude-code)
            backup_if_exists "$PROJECT_DIR/CLAUDE.md"
            cp "$REPO_DIR/adapters/claude-code/CLAUDE.md" "$PROJECT_DIR/CLAUDE.md"
            echo "  ✓ CLAUDE.md installed"
            ;;
        codex)
            backup_if_exists "$PROJECT_DIR/AGENTS.md"
            cp "$REPO_DIR/adapters/codex/AGENTS.md" "$PROJECT_DIR/AGENTS.md"
            echo "  ✓ AGENTS.md installed"
            ;;
        kiro)
            backup_if_exists "$PROJECT_DIR/.kiro"
            mkdir -p "$PROJECT_DIR/.kiro/specs"
            cp "$REPO_DIR/adapters/kiro/.kiro/specs/polyagent-skills.md" "$PROJECT_DIR/.kiro/specs/"
            echo "  ✓ .kiro/specs/polyagent-skills.md installed"
            ;;
        gemini)
            backup_if_exists "$PROJECT_DIR/.gemini"
            mkdir -p "$PROJECT_DIR/.gemini"
            cp "$REPO_DIR/adapters/gemini/.gemini/instructions.md" "$PROJECT_DIR/.gemini/"
            echo "  ✓ .gemini/instructions.md installed"
            ;;
        cursor)
            backup_if_exists "$PROJECT_DIR/.cursor"
            mkdir -p "$PROJECT_DIR/.cursor"
            cp "$REPO_DIR/adapters/cursor/.cursor/rules.md" "$PROJECT_DIR/.cursor/"
            echo "  ✓ .cursor/rules.md installed"
            ;;
        *)
            echo "  ✗ Unknown agent: $agent_name"
            echo "  Supported: claude-code, codex, kiro, gemini, cursor, all"
            return 1
            ;;
    esac
}

if [ "$AGENT" = "all" ]; then
    for a in claude-code codex kiro gemini cursor; do
        install_adapter "$a"
    done
else
    install_adapter "$AGENT"
fi

echo ""
echo "=== Installation complete ==="
echo "Open $PROJECT_DIR in your agent — skills are ready to use."
