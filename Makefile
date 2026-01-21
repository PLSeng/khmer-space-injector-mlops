# Root Makefile for khmer-space-injector-mlops
# Works best in:
# - Linux/macOS shells
# - Windows PowerShell (using: make <target>)
#
# NOTE: On Windows, ensure you have GNU Make installed (e.g., via Git Bash, MSYS2, or Chocolatey).

.PHONY: help api-install deploy
COMPOSE = docker compose -f infra/docker-compose.yml

help:
	@echo "Targets:"
	@echo "  api-install   Install API dependencies"
	@echo "  deploy        Deploy using Docker Compose"

# -------------------------
# API (FastAPI)
# -------------------------

api-install:
	python -m pip install --upgrade pip
	conda install -y -c conda-forge numpy scipy scikit-learn
	pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
	pip install -r ./apps/api/requirements.txt

deploy: down build up ps

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build --no-cache

up:
	$(COMPOSE) up -d

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f

# First-time SSL issuance (run once)
ssl:
	$(COMPOSE) run --rm certbot certonly \
		--webroot \
		--webroot-path=/var/www/certbot \
		-d khmer-space-injector.duckdns.org \
		--email you@example.com \
		--agree-tos \
		--no-eff-email

# Renew SSL certs (safe to run anytime)
renew:
	$(COMPOSE) run --rm certbot renew
	$(COMPOSE) restart nginx

nginx-reload:
	$(COMPOSE) exec nginx nginx -s reload

provision-vm:
	@set -eu; \
	sudo apt-get update; \
	sudo apt-get install -y nginx ca-certificates curl gnupg; \
	\
	sudo install -m 0755 -d /etc/apt/keyrings; \
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg; \
	sudo chmod a+r /etc/apt/keyrings/docker.gpg; \
	\
	codename="$$(. /etc/os-release && echo $$VERSION_CODENAME)"; \
	arch="$$(dpkg --print-architecture)"; \
	echo "deb [arch=$$arch signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $$codename stable" \
	| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null; \
	\
	sudo apt-get update; \
	sudo apt-get install -y docker-compose-plugin; \
	docker compose version


restart-services:
	docker compose -f infra/docker-compose.yml restart
	sudo systemctl restart nginx
