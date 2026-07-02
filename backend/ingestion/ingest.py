"""
Ingestion pipeline: read LensPilot docs from disk, chunk them, embed them,
and store them in Postgres.

Run directly:
    python ingestion/ingest.py

Or trigger via the admin endpoint POST /ingest (see app/api/routes.py).

Supported file types: .md, .txt, .html, .pdf
Reruns are safe: each file's content is hashed, and files whose content
hasn't changed since the last run are skipped (no duplicate documents).
"""
import hashlib
import logging
import os
import sys

# Allow running this file directly with `python ingestion/ingest.py`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.document import Document
from app.models.chunk import Chunk
from app.services.embeddings import embed_texts
from app.core.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("ingest")


# ---------- Text extraction ----------

def extract_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext in (".md", ".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    if ext == ".html":
        from bs4 import BeautifulSoup
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        return soup.get_text(separator="\n")

    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    raise ValueError(f"Unsupported file type: {ext}")


# ---------- Chunking ----------

def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[str]:
    """
    Simple word-based chunking with overlap. Good enough for FAQ/policy/product
    docs; swap for a smarter splitter later if needed (e.g. by headings).
    """
    size = chunk_size or settings.CHUNK_SIZE_WORDS
    ov = overlap or settings.CHUNK_OVERLAP_WORDS

    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    while start < len(words):
        end = start + size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk.strip())
        if end >= len(words):
            break
        start = end - ov  # step forward, but overlap the last `ov` words
    return chunks


# ---------- Main ingestion ----------

def guess_source_category(filename: str) -> str:
    name = filename.lower()
    if "faq" in name:
        return "FAQ"
    if "polic" in name:
        return "Policy"
    if "pric" in name:
        return "Pricing"
    if "support" in name:
        return "Support"
    return "Product"


def run_ingestion(docs_dir: str | None = None) -> dict:
    directory = docs_dir or settings.INGESTION_DOCS_DIR
    directory = os.path.abspath(directory)

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Docs directory not found: {directory}")

    db = SessionLocal()
    inserted_docs = 0
    skipped_docs = 0
    inserted_chunks = 0

    try:
        for filename in sorted(os.listdir(directory)):
            path = os.path.join(directory, filename)
            if not os.path.isfile(path):
                continue
            ext = os.path.splitext(filename)[1].lower()
            if ext not in (".md", ".txt", ".html", ".pdf"):
                continue

            raw_bytes = open(path, "rb").read()
            content_hash = hashlib.sha256(raw_bytes).hexdigest()

            existing = db.query(Document).filter_by(content_hash=content_hash).first()
            if existing:
                logger.info("Skipping unchanged doc: %s", filename)
                skipped_docs += 1
                continue

            text = extract_text(path)
            chunks = chunk_text(text)
            if not chunks:
                logger.warning("No text extracted from %s, skipping", filename)
                continue

            doc = Document(
                title=os.path.splitext(filename)[0].replace("_", " ").title(),
                source=guess_source_category(filename),
                doc_metadata={"filename": filename},
                content_hash=content_hash,
            )
            db.add(doc)
            db.flush()  # get doc.id before inserting chunks

            embeddings = embed_texts(chunks)
            for i, (chunk_str, vec) in enumerate(zip(chunks, embeddings)):
                db.add(Chunk(document_id=doc.id, chunk_index=i, text=chunk_str, embedding=vec))
                inserted_chunks += 1

            db.commit()
            inserted_docs += 1
            logger.info("Ingested %s -> %d chunks", filename, len(chunks))

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    summary = {
        "documents_inserted": inserted_docs,
        "documents_skipped_unchanged": skipped_docs,
        "chunks_inserted": inserted_chunks,
    }
    logger.info("Ingestion summary: %s", summary)
    return summary


if __name__ == "__main__":
    run_ingestion()
