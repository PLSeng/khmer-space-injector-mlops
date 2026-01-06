#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/ubuntu/khmer-space-injector-mlops"
APP_USER="ubuntu"
DOMAIN="khmer-space-injector.duckdns.org"

echo "==> Deploy starting..."

if [ ! -d "$REPO_DIR/.git" ]; then
  echo "ERROR: $REPO_DIR is not a git repo. Clone it first:"
  echo "  git clone <YOUR_GITHUB_REPO_URL> $REPO_DIR"
  exit 1
fi

cd "$REPO_DIR"
echo "==> Pull latest"
git pull

echo "==> Ensure .env exists"
if [ ! -f "$REPO_DIR/.env" ]; then
  echo "ERROR: Missing $REPO_DIR/.env"
  echo "Create it from .env.example and set DATABASE_URL + artifact paths."
  exit 1
fi

echo "==> Setup Python venv"
if [ ! -d "$REPO_DIR/.venv" ]; then
  python3 -m venv "$REPO_DIR/.venv"
fi

echo "==> Install API deps"
"$REPO_DIR/.venv/bin/pip" install --upgrade pip
"$REPO_DIR/.venv/bin/pip" install -r "$REPO_DIR/apps/api/requirements.txt"

echo "==> Run DB migrations (optional)"
if [ -f "$REPO_DIR/apps/api/alembic.ini" ]; then
  bash "$REPO_DIR/infra/scripts/db_migrate.sh" || true
else
  echo "Skipping migrations: alembic.ini not found"
fi

echo "==> Build frontend"
cd "$REPO_DIR/apps/frontend"
npm ci
npm run build

echo "==> Install Nginx site config"
sudo cp "$REPO_DIR/infra/nginx/default.conf" /etc/nginx/sites-available/khmer-space-injector
sudo ln -sf /etc/nginx/sites-available/khmer-space-injector /etc/nginx/sites-enabled/khmer-space-injector
sudo rm -f /etc/nginx/sites-enabled/default || true

sudo nginx -t
sudo systemctl restart nginx

echo "==> Install/Update systemd service for FastAPI"
sudo cp "$REPO_DIR/infra/systemd/fastapi.service" /etc/systemd/system/fastapi.service
sudo systemctl daemon-reload
sudo systemctl enable --now fastapi
sudo systemctl restart fastapi

echo "==> Deploy complete!"
echo "Check:"
echo "  curl -i http://127.0.0.1:8000/health"
echo "  curl -i http://$DOMAIN/health"
