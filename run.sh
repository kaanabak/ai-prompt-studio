#!/usr/bin/env bash
# One-click launcher for macOS and Linux.
# Creates a virtualenv, installs dependencies, starts PromptForge in the
# background, waits for it to become healthy, then opens it in your browser.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR=".venv"
PORT="${PROMPTFORGE_PORT:-5000}"
URL="http://127.0.0.1:${PORT}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python 3 was not found. Install it from https://www.python.org/downloads/ and try again." >&2
  exit 1
fi

if [ ! -x "${VENV_DIR}/bin/python" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"${VENV_DIR}/bin/python" -m pip install --disable-pip-version-check -q -r requirements.txt

# Start the server in the background and remember its PID.
"${VENV_DIR}/bin/python" app.py &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT

echo "Starting PromptForge (PID ${SERVER_PID})..."

ready=""
for _ in $(seq 1 40); do
  if curl --silent --fail "${URL}/health" >/dev/null 2>&1; then
    ready="1"
    break
  fi
  sleep 0.25
done

if [ -z "$ready" ]; then
  echo "PromptForge did not become ready at ${URL}." >&2
  echo "Close any other app using port ${PORT}, then try again." >&2
  exit 1
fi

trap - EXIT # hand the process off; don't kill it when this script exits

if command -v open >/dev/null 2>&1; then
  open "$URL"                     # macOS
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL"                 # Linux desktops
else
  echo "PromptForge is running at ${URL}"
fi

echo "PromptForge is running at ${URL} (PID ${SERVER_PID}). Press Ctrl+C in that process, or run 'kill ${SERVER_PID}', to stop it."
wait "$SERVER_PID"
