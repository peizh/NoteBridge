#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEFAULT_SKILL_WRAPPER="${CODEX_HOME:-$HOME/.codex}/skills/playwright/scripts/playwright_cli.sh"
NODE_BIN_DIR=""

resolve_node_bin_dir() {
    local candidate=""

    for formula in node@22 node@20; do
        if command -v brew >/dev/null 2>&1; then
            candidate="$(brew --prefix "$formula" 2>/dev/null || true)"
            if [[ -n "$candidate" && -x "$candidate/bin/node" && -x "$candidate/bin/npx" ]]; then
                NODE_BIN_DIR="$candidate/bin"
                return 0
            fi
        fi
    done

    if command -v node >/dev/null 2>&1; then
        local version major
        version="$(node --version 2>/dev/null || true)"
        major="${version#v}"
        major="${major%%.*}"
        if [[ -n "$major" && "$major" -ge 18 ]]; then
            NODE_BIN_DIR="$(dirname "$(command -v node)")"
            return 0
        fi
    fi

    return 1
}

resolve_node_bin_dir || {
    cat >&2 <<'EOF'
Playwright CLI requires Node.js 18 or newer.

Install a supported Homebrew runtime, then re-run:
  brew install node@22
EOF
    exit 1
}

if [[ -x "$DEFAULT_SKILL_WRAPPER" ]]; then
    exec env PATH="$NODE_BIN_DIR:$PATH" "$DEFAULT_SKILL_WRAPPER" "$@"
fi

exec env PATH="$NODE_BIN_DIR:$PATH" npx --yes --package @playwright/cli playwright-cli "$@"
