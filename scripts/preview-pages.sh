#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${NOTESBRIDGE_PREVIEW_PORT:-4173}"
HOST="${NOTESBRIDGE_PREVIEW_HOST:-127.0.0.1}"
URL="http://$HOST:$PORT"
SERVER_PID=""

cleanup() {
    if [[ -n "$SERVER_PID" ]]; then
        kill "$SERVER_PID" >/dev/null 2>&1 || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}

trap cleanup EXIT

if ! lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    python3 -m http.server "$PORT" --bind "$HOST" --directory "$ROOT_DIR/site" >/tmp/notesbridge-preview.log 2>&1 &
    SERVER_PID="$!"
    sleep 1
fi

"$ROOT_DIR/scripts/playwright-cli.sh" open "$URL" --headed
