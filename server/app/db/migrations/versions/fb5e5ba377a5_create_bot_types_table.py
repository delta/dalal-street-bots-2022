"""create bot types table

Revision ID: fb5e5ba377a5
Revises: 
Create Date: 2022-01-17 00:46:18.175906

"""
from alembic import op
import sqlalchemy as sa

from app.db.migrations.helper import timestamps


# revision identifiers, used by Alembic.
revision = "fb5e5ba377a5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    print("running up migrations for create bot types table")
    op.create_table(
        "bot_types",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, unique=True, nullable=False),
        *timestamps(),
    )
    pass


def downgrade():
    print("running down migrations for create bot types table")
    op.drop_table("bot_types")
    pass