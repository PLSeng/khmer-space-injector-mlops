FROM python:3.11-slim

WORKDIR /app

# System deps (psycopg binary usually OK without build tools, but keep minimal)
RUN pip install --no-cache-dir -U pip

# Copy only dependency files first for caching
COPY pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir .

# Copy app code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini

EXPOSE 8000

# Recommended env defaults (override in compose / cloud)
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]