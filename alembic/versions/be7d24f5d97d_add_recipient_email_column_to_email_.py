"""Add recipient_email column to email_notifications

Revision ID: be7d24f5d97d
Revises: 89bf52a43af0
Create Date: 2025-08-02 11:54:05.699588
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'be7d24f5d97d'
down_revision = '89bf52a43af0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add only the columns that don't already exist in the DB
    with op.batch_alter_table("email_notifications") as batch_op:
        batch_op.add_column(sa.Column('recipient_email', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('subject', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('body', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('status', sa.String(), nullable=False))
        # Do NOT add 'user_id' if it's already in the table

    with op.batch_alter_table("email_notifications") as batch_op:
        batch_op.alter_column('user_id', existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column('was_present', existing_type=sa.Boolean(), nullable=False)


def downgrade() -> None:
    op.drop_constraint('email_notifications_user_id_fkey', 'email_notifications', type_='foreignkey')
    op.drop_column('email_notifications', 'user_id')
    op.drop_column('email_notifications', 'status')
    op.drop_column('email_notifications', 'body')
    op.drop_column('email_notifications', 'subject')
    op.drop_column('email_notifications', 'recipient_email')
