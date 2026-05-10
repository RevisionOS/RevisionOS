"""add module public sharing flag

Revision ID: 7b8c9d0e1f2a
Revises: 6a7b8c9d1e2f, 6d7e8f9a0b1c
Create Date: 2026-05-10 01:15:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7b8c9d0e1f2a"
down_revision: Union[str, Sequence[str], None] = ("6a7b8c9d1e2f", "6d7e8f9a0b1c")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return any(column["name"] == column_name for column in inspector.get_columns(table_name))


def _has_index(table_name: str, index_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return any(index["name"] == index_name for index in inspector.get_indexes(table_name))


def upgrade() -> None:
    if not _has_column("modules", "is_public"):
        op.add_column(
            "modules",
            sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.false()),
        )
    if not _has_index("modules", "ix_modules_is_public"):
        op.create_index("ix_modules_is_public", "modules", ["is_public"], unique=False)


def downgrade() -> None:
    if _has_index("modules", "ix_modules_is_public"):
        op.drop_index("ix_modules_is_public", table_name="modules")
    if _has_column("modules", "is_public"):
        op.drop_column("modules", "is_public")
