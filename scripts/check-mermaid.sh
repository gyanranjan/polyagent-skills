#!/usr/bin/env bash
set -euo pipefail

if command -v mmdc >/dev/null 2>&1; then
  echo "mermaid_cli_installed=yes"
  mmdc --version
else
  echo "mermaid_cli_installed=no"
  echo "hint=install with: npm install -g @mermaid-js/mermaid-cli"
fi
