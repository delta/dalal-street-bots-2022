"""create bot types table

Revision ID: fb5e5ba377a5
Revises:
Create Date: 2022-01-17 00:46:18.175906

"""
import sqlalchemy as sa
from alembic import op

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
        sa.Column("name", sa.String(255), nullable=False, length=255),
        *timestamps(),
    )


def downgrade():
    print("running down migrations for create bot types table")
    op.drop_table("bot_types")
