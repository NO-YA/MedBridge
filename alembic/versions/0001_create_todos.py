"""create todos table

Revision ID: 0001_create_todos
Revises: 
Create Date: 2025-12-15 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_todos'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "todo",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("task", sa.Text(), nullable=False),
        sa.Column("done", sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()),
    )


def downgrade() -> None:
    op.drop_table("todo")
