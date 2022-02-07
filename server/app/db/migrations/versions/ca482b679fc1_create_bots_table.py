"""create bots table

Revision ID: ca482b679fc1
Revises: fb5e5ba377a5
Create Date: 2022-01-17 01:23:25.555091

"""
import logging

import sqlalchemy as sa
from alembic import op

from app.db.migrations.helper import timestamps

# revision identifiers, used by Alembic.
revision = "ca482b679fc1"
down_revision = "fb5e5ba377a5"
branch_labels = None
depends_on = None


def upgrade():
    logging.info("running up migrations for create bots table")
    op.create_table(
        "bots",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column(
            "bot_type",
            sa.Integer,
            sa.ForeignKey("bot_types.id", ondelete="CASCADE"),
            nullable=False,
        ),
        *timestamps(),
    )


def downgrade():
    logging.info("running down migrations for create bots table")
    op.drop_table("bots")
