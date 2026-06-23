#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -f ".env" ]; then
  set -a
  # shellcheck disable=SC1091
  source ".env"
  set +a
elif [ -f "/Users/apple/Desktop/UoB/Final-Project/multimodal-rag/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "/Users/apple/Desktop/UoB/Final-Project/multimodal-rag/.env"
  set +a
fi

export GEMINI_TEXT_MODEL="${GEMINI_TEXT_MODEL:-${GEMINI_MODEL:-gemini-2.5-flash}}"
export GEMINI_VISION_MODEL="${GEMINI_VISION_MODEL:-${GEMINI_MODEL:-gemini-2.5-flash}}"
export GEMINI_EMBEDDING_MODEL="${GEMINI_EMBEDDING_MODEL:-gemini-embedding-001}"
export DISABLE_GEMINI="${DISABLE_GEMINI:-false}"

source ".venv/bin/activate"
uvicorn backend.app.main:app --host "${BACKEND_HOST:-127.0.0.1}" --port "${BACKEND_PORT:-8899}"

