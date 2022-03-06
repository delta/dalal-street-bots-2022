"""add_server_bot_id_to_bots

Revision ID: caf85e6ee2c7
Revises: 976573dc98f2
Create Date: 2022-03-05 09:56:17.324327

"""
import logging

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "caf85e6ee2c7"
down_revision = "976573dc98f2"
branch_labels = None
depends_on = None


def upgrade():
    logging.info("running up migrations for add_server_bot_id_to_bots")
    op.add_column(
        "bots", sa.Column("server_bot_id", sa.Integer, nullable=False, unique=True)
    )


def downgrade():
    logging.info("running down migrations for add_server_bot_id_to_bots")
    op.drop_column("bots", "server_bot_id")
