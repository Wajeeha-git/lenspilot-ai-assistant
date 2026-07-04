from datetime import datetime, timezone

from sqlalchemy import String, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Provenance -- where this content came from (e.g. "LensPilot Knowledge Base v1").
    # Kept separate from `category` below, which is the retrieval-facing topic label.
    source: Mapped[str] = mapped_column(String(150), nullable=False, default="General")

    # Retrieval-facing topic label, e.g. "FAQ", "Workflow", "Error Handling".
    # Sourced from each doc's frontmatter `category:` field during ingestion.
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="General", index=True)

    # Who the content is written for, e.g. "public", "customer", "shopkeeper",
    # "admin", "internal". Informational/citation metadata -- not a hard
    # retrieval filter today (see retrieval.py for why), but stored so that
    # filtering-by-audience is a query change, not a re-ingestion.
    audience: Mapped[str] = mapped_column(String(50), nullable=False, default="public", index=True)

    # Hard access-control flag. False = never returned to /chat retrieval,
    # regardless of similarity score. Defaults to True (public) so ingestion
    # doesn't silently hide content unless a doc explicitly opts out.
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)

    # Free-text version/date string from frontmatter, e.g. "2026-07-03".
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Full raw frontmatter + original filename, kept for debugging/audit.
    doc_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    # sha256 of the raw file content -- lets ingestion skip re-inserting unchanged docs
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
