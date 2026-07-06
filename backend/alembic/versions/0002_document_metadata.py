"""add category, audience, is_public, version to documents

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-03
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "documents",
        sa.Column("category", sa.String(100), nullable=False, server_default="General"),
    )
    op.add_column(
        "documents",
        sa.Column("audience", sa.String(50), nullable=False, server_default="public"),
    )
    op.add_column(
        "documents",
        sa.Column("is_public", sa.Boolean, nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "documents",
        sa.Column("version", sa.String(50), nullable=True),
    )
    op.create_index("ix_documents_category", "documents", ["category"])
    op.create_index("ix_documents_audience", "documents", ["audience"])
    op.create_index("ix_documents_is_public", "documents", ["is_public"])
    op.alter_column("documents", "source", type_=sa.String(150))


def downgrade():
    op.drop_index("ix_documents_is_public", table_name="documents")
    op.drop_index("ix_documents_audience", table_name="documents")
    op.drop_index("ix_documents_category", table_name="documents")
    op.drop_column("documents", "version")
    op.drop_column("documents", "is_public")
    op.drop_column("documents", "audience")
    op.drop_column("documents", "category")
    op.alter_column("documents", "source", type_=sa.String(100))
