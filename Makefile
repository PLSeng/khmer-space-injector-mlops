# Root Makefile for khmer-space-injector-mlops
# Works best in:
# - Linux/macOS shells
# - Windows PowerShell (using: make <target>)
#
# NOTE: On Windows, ensure you have GNU Make installed (e.g., via Git Bash, MSYS2, or Chocolatey).

.PHONY: help api-install deploy

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

deploy:
	docker compose -f infra/docker-compose.yml down
	docker compose -f infra/docker-compose.yml build --no-cache
	docker compose -f infra/docker-compose.yml up -d
	docker compose -f infra/docker-compose.yml ps

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
