"""Add code_type to attendance_codes

Revision ID: 22ef2ff11688
Revises: 053e0faf9926
Create Date: 2025-08-19 17:05:40.230520
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '22ef2ff11688'
down_revision: Union[str, Sequence[str], None] = '053e0faf9926'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add code_type column."""
    op.add_column(
        "attendance_codes",
        sa.Column("code_type", sa.String(length=10), nullable=False, server_default="in")
    )


def downgrade() -> None:
    """Downgrade schema: remove code_type column."""
    op.drop_column("attendance_codes", "code_type")
