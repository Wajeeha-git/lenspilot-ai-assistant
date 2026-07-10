import os
from sqlalchemy import create_engine, text

db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/lenspilot_ai')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector;'))
        conn.commit()
    print("pgvector extension enabled successfully")
except Exception as e:
    print(f"Warning: Could not enable pgvector: {e}")
