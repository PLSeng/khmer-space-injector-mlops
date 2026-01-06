FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (psycopg + build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install deps first (better caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy API source
COPY app/ /app/app/

# Copy model artifacts (checkpoint + vocab + config)
# If you decide NOT to commit artifacts, remove this block and mount them at runtime.
COPY artifacts/ /app/artifacts/

# Default env paths (can be overridden)
ENV MODEL_CHECKPOINT_PATH=/app/artifacts/checkpoint.pt \
    VOCAB_PATH=/app/artifacts/vocab.json \
    MODEL_CONFIG_PATH=/app/artifacts/config.json

EXPOSE 8000

# Healthcheck hits the internal API
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
