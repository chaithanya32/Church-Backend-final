"""add volunteers and attendance_codes tables

Revision ID: 7f991e783000
Revises: 46aaa1c819a9
Create Date: 2025-08-04 17:32:43.651908
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7f991e783000'
down_revision: Union[str, Sequence[str], None] = '46aaa1c819a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Tables already exist, no changes needed
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # Do nothing since we didn't create anything
    pass
