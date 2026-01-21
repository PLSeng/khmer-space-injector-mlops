#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/ubuntu/khmer-space-injector-mlops"

cd "$REPO_DIR/apps/api"
"$REPO_DIR/.venv/bin/python" -m alembic upgrade head
