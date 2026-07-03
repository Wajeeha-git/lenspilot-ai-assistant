"""
Similarity search over the chunks table using pgvector.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.document import Document
from app.core.config import settings
from app.services.embeddings import embed_text


def retrieve_relevant_chunks(db: Session, question: str, top_k: int | None = None) -> list[dict]:
    """
    Embed the question and find the top_k most similar chunks in Postgres.
    Returns a list of dicts ready to feed into the prompt builder and to
    return to the client as "sources".

    Hard filter: only documents with is_public=True are ever eligible for
    retrieval here. This is the actual enforcement of the public/internal
    distinction in the knowledge base -- a document marked internal-only
    (public: false in its frontmatter) will never surface in a /chat
    answer, regardless of similarity score. `category` and `audience` are
    returned as informational metadata (for citation transparency and
    future filtering) but are not hard-filtered by default, since a
    legitimate question can reasonably span audiences (e.g. anyone asking
    "what can shopkeepers do").
    """
    k = top_k or settings.RETRIEVAL_TOP_K
    query_embedding = embed_text(question)

    stmt = (
        select(
            Chunk.id,
            Chunk.text,
            Document.id.label("document_id"),
            Document.title.label("document_title"),
            Document.category,
            Document.audience,
            Document.source,
            Chunk.embedding.cosine_distance(query_embedding).label("distance"),
        )
        .join(Document, Chunk.document_id == Document.id)
        .where(Document.is_public.is_(True))
        .order_by("distance")
        .limit(k)
    )

    rows = db.execute(stmt).all()

    results = []
    for row in rows:
        results.append(
            {
                "chunk_id": row.id,
                "text": row.text,
                "document_id": row.document_id,
                "document_title": row.document_title,
                "category": row.category,
                "audience": row.audience,
                "source": row.source,
                # cosine distance -> similarity score in [0, 1], higher = more similar
                "similarity": round(1 - float(row.distance), 4),
            }
        )
    return results
