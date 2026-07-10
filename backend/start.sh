#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e
echo "Running database migrations..."
alembic upgrade head
echo "Enabling pgvector extension..."
python -c "
import os
from sqlalchemy import create_engine, text
db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/lenspilot_ai')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
engine = create_engine(db_url)
with engine.connect() as conn:
    conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector;'))
    conn.commit()
"
echo "Running ingestion pipeline..."
python ingestion/ingest.py
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
