#!/bin/sh
set -e
echo "Running database migrations..."
alembic upgrade head
echo "Enabling pgvector extension..."
python3 setup_pgvector.py
echo "Running ingestion pipeline..."
python3 ingestion/ingest.py
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
