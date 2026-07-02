from datetime import datetime, timezone

from sqlalchemy import String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # e.g. "FAQ", "Policy", "Product", "Pricing", "Support"
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="General")
    # arbitrary extra info: original filename, category, version, etc.
    doc_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    # sha256 of the raw file content -- lets ingestion skip re-inserting unchanged docs
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
