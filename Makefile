# Root Makefile for khmer-space-injector-mlops
# Works best in:
# - Linux/macOS shells
# - Windows PowerShell (using: make <target>)
#
# NOTE: On Windows, ensure you have GNU Make installed (e.g., via Git Bash, MSYS2, or Chocolatey).

.PHONY: help api-install api-test api-run api-format fe-install fe-test fe-dev fe-build ci-local clean

help:
	@echo "Targets:"
	@echo "  api-install   Install API dependencies"
	@echo "  api-test      Run API tests (pytest)"
	@echo "  api-run       Run API locally (uvicorn --reload)"
	@echo "  fe-install    Install Frontend dependencies (npm ci)"
	@echo "  fe-test       Run Frontend tests (npm test)"
	@echo "  fe-dev        Run Frontend dev server"
	@echo "  fe-build      Build Frontend (Vite)"
	@echo "  ci-local      Run local checks similar to CI"
	@echo "  clean         Remove common caches"

# -------------------------
# API (FastAPI)
# -------------------------

api-install:
	cd apps/api && python -m pip install --upgrade pip && pip install -r requirements.txt

api-test:
	cd apps/api && pytest

api-run:
	cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


# (Optional) formatting placeholder (does nothing unless you add ruff/black later)
api-format:
	@echo "No formatter configured yet. Add ruff/black to requirements.txt then update this target."


# -------------------------
# Frontend (React + Vite)
# -------------------------

fe-install:
	cd apps/frontend && npm ci

fe-test:
	cd apps/frontend && npm test

fe-dev:
	cd apps/frontend && npm run dev

fe-build:
	cd apps/frontend && npm run build


# -------------------------
# Convenience
# -------------------------

ci-local:
	@echo "Running API tests..."
	$(MAKE) api-test
	@echo "Frontend tests/build are optional until implemented."
	@echo "If available, run: make fe-test && make fe-build"

clean:
	# Python caches
	@if exist apps\\api\\__pycache__ rmdir /s /q apps\\api\\__pycache__
	@if exist apps\\api\\.pytest_cache rmdir /s /q apps\\api\\.pytest_cache
	@if exist apps\\api\\.mypy_cache rmdir /s /q apps\\api\\.mypy_cache
	@if exist apps\\api\\.ruff_cache rmdir /s /q apps\\api\\.ruff_cache
	# Node caches
	@if exist apps\\frontend\\node_modules rmdir /s /q apps\\frontend\\node_modules
	@if exist apps\\frontend\\dist rmdir /s /q apps\\frontend\\dist
