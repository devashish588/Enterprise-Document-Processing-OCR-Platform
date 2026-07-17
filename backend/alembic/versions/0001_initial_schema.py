"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-17
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("content_type", sa.String(120), nullable=False),
        sa.Column("storage_path", sa.String(500), nullable=False),
        sa.Column("document_type", sa.String(80), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("uploaded_by_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_documents_document_type", "documents", ["document_type"])
    op.create_index("ix_documents_status", "documents", ["status"])
    op.create_table("ocr_results", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id"), unique=True), sa.Column("engine", sa.String(50), nullable=False), sa.Column("text", sa.Text(), nullable=False), sa.Column("confidence", sa.Float(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("extracted_fields", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id")), sa.Column("name", sa.String(100), nullable=False), sa.Column("value", sa.Text(), nullable=False), sa.Column("confidence", sa.Float(), nullable=False))
    op.create_index("ix_extracted_fields_document_id", "extracted_fields", ["document_id"])
    op.create_index("ix_extracted_fields_name", "extracted_fields", ["name"])
    op.create_table("validation_issues", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id")), sa.Column("field_name", sa.String(100), nullable=False), sa.Column("severity", sa.String(30), nullable=False), sa.Column("message", sa.String(500), nullable=False))
    op.create_index("ix_validation_issues_document_id", "validation_issues", ["document_id"])
    op.create_table("audit_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("actor", sa.String(255), nullable=False), sa.Column("action", sa.String(100), nullable=False), sa.Column("entity_type", sa.String(100), nullable=False), sa.Column("entity_id", sa.String(100), nullable=False), sa.Column("details", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))


def downgrade():
    for table in ("audit_logs", "validation_issues", "extracted_fields", "ocr_results", "documents", "users"):
        op.drop_table(table)

