#!/bin/sh
set -e

echo "Enabling pgvector extension..."
python3 setup_pgvector.py || echo "Warning: pgvector setup command failed; migrations will verify database readiness."

echo "Running database migrations..."
alembic upgrade head

if [ "${RUN_INGEST_ON_STARTUP:-true}" = "true" ]; then
  if [ -n "$GEMINI_API_KEY" ]; then
    echo "Running ingestion pipeline..."
    python3 ingestion/ingest.py || echo "Warning: ingestion failed; start the service and retry ingestion from /api/v1/ingest after checking secrets/logs."
  else
    echo "Skipping ingestion because GEMINI_API_KEY is not set."
  fi
else
  echo "Skipping ingestion because RUN_INGEST_ON_STARTUP is not true."
fi

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
