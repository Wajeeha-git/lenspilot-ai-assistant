"""
Ingestion pipeline: read LensPilot docs from disk, parse metadata, chunk by
section/meaning, embed, and store in Postgres.

Run directly:
    python ingestion/ingest.py

Or trigger via the admin endpoint POST /ingest (see app/api/routes.py).

Supported file types: .md, .txt, .html, .pdf
Reruns are safe: each file's content is hashed, and files whose content
hasn't changed since the last run are skipped (no duplicate documents).

Metadata: .md/.txt files may start with a simple frontmatter block:

    ---
    title: FAQ - Customer
    category: FAQ
    audience: customer
    source: LensPilot Knowledge Base v1
    version: 2026-07-03
    public: true
    ---
    # body starts here...

Any field can be omitted -- ingestion falls back to a filename-based guess
for title/category, and to "public"/True for audience/is_public. This is a
small hand-rolled parser (not YAML) so no new dependency is needed for five
flat key: value lines.
"""
import hashlib
import logging
import os
import re
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


# ---------- Frontmatter ----------

def parse_frontmatter(raw_text: str) -> tuple[dict, str]:
    """
    Split a leading '---\\n...\\n---' block into a metadata dict, returning
    (metadata, remaining_body). If there's no frontmatter block, returns
    ({}, raw_text) unchanged.
    """
    if not raw_text.startswith("---"):
        return {}, raw_text

    parts = raw_text.split("---", 2)
    if len(parts) < 3:
        return {}, raw_text

    _, frontmatter_block, body = parts
    metadata: dict = {}
    for line in frontmatter_block.strip().splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.lower() in ("true", "false"):
            metadata[key] = value.lower() == "true"
        else:
            metadata[key] = value

    return metadata, body.strip()


# ---------- Chunking ----------

def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[str]:
    """
    Simple word-based chunking with overlap. Used directly as a fallback for
    plain (non-heading) text, and internally by chunk_markdown() to split
    any single section that's still too large on its own.
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


def chunk_markdown(body: str, max_words: int | None = None, overlap_words: int | None = None) -> list[str]:
    """
    Chunk by meaning rather than pure word count: split on '## ' headings so
    each topic/FAQ-question stays together as one chunk (an FAQ answer is
    never split mid-sentence just because a size threshold was crossed). A
    section is only sub-chunked with chunk_text() if it's larger than
    max_words on its own -- and even then, the heading is kept on every
    sub-chunk so retrieval still has topic context.

    max_words/overlap_words default to settings.CHUNK_SIZE_WORDS /
    CHUNK_OVERLAP_WORDS, tuned around the ~256-512 token (~190-380 word)
    target range.
    """
    max_w = max_words or settings.CHUNK_SIZE_WORDS
    overlap_w = overlap_words or settings.CHUNK_OVERLAP_WORDS

    body = body.strip()
    if not body:
        return []

    if "\n## " not in ("\n" + body):
        # No sub-headings at all -- just chunk the whole thing by size.
        return chunk_text(body, chunk_size=max_w, overlap=overlap_w)

    raw_sections = re.split(r"(?=^## )", body, flags=re.MULTILINE)

    chunks: list[str] = []
    for idx, section in enumerate(raw_sections):
        section = section.strip()
        if not section:
            continue

        if idx == 0:
            # This fragment covers everything before the first "## " heading.
            # If it's just the "# Title" line with no additional prose below
            # it, there's no retrievable content here -- skip it.
            lines = [l for l in section.splitlines() if l.strip()]
            if len(lines) <= 1 and lines[0].lstrip().startswith("# "):
                continue
        word_count = len(section.split())
        if word_count == 0:
            continue

        if word_count <= max_w:
            chunks.append(section)
            continue

        heading_match = re.match(r"^(## [^\n]*\n)", section)
        heading = heading_match.group(1) if heading_match else ""
        remainder = section[len(heading):] if heading else section
        for sub in chunk_text(remainder, chunk_size=max_w, overlap=overlap_w):
            chunks.append(f"{heading}{sub}".strip())

    return chunks


# ---------- Main ingestion ----------

_ACRONYMS = {"Ai": "AI", "Faq": "FAQ", "Qr": "QR"}


def filename_to_title(filename: str) -> str:
    """Fallback title if frontmatter has no `title:` -- 'faq_customer.md' -> 'Faq Customer' -> 'FAQ Customer'."""
    stem = os.path.splitext(filename)[0]
    words = stem.replace("_", " ").replace("-", " ").title().split()
    words = [_ACRONYMS.get(w, w) for w in words]
    return " ".join(words)


def guess_category(filename: str) -> str:
    """Fallback category if frontmatter has no `category:`."""
    name = filename.lower()
    if "faq" in name:
        return "FAQ"
    if "error" in name or "troubleshoot" in name:
        return "Error Handling"
    if "polic" in name:
        return "Policy"
    if "pric" in name:
        return "Pricing"
    if "role" in name:
        return "User Roles"
    if "workflow" in name:
        return "Workflow"
    if "technolog" in name:
        return "Technologies"
    if "feature" in name:
        return "AI Features"
    if "business" in name or "rules" in name:
        return "Business Rules"
    if "compan" in name:
        return "Company Info"
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

            raw_text = extract_text(path)
            metadata, body = parse_frontmatter(raw_text)
            chunks = chunk_markdown(body)
            if not chunks:
                logger.warning("No text extracted from %s, skipping", filename)
                continue

            is_public = metadata.get("public", True)
            if isinstance(is_public, str):
                is_public = is_public.strip().lower() != "false"

            doc = Document(
                title=metadata.get("title") or filename_to_title(filename),
                source=metadata.get("source", "LensPilot Knowledge Base"),
                category=metadata.get("category") or guess_category(filename),
                audience=metadata.get("audience", "public"),
                is_public=bool(is_public),
                version=metadata.get("version"),
                doc_metadata={"filename": filename, **metadata},
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
            logger.info(
                "Ingested %s -> %d chunks (category=%s, audience=%s, public=%s)",
                filename, len(chunks), doc.category, doc.audience, doc.is_public,
            )

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
