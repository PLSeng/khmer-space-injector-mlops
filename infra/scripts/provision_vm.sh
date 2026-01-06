#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/ubuntu/khmer-space-injector-mlops"
APP_USER="ubuntu"

echo "==> Updating packages"
sudo apt-get update -y
sudo apt-get install -y git curl ca-certificates nginx

echo "==> Installing Python"
sudo apt-get install -y python3 python3-venv python3-pip

echo "==> Installing Node.js 20 (for Vite build)"
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

echo "==> Done. Next:"
echo "  1) git clone your repo into $REPO_DIR"
echo "  2) create $REPO_DIR/.env"
echo "  3) run infra/scripts/deploy.sh"
