"""create logs table

Revision ID: 976573dc98f2
Revises: ca482b679fc1
Create Date: 2022-01-17 01:28:09.873809

"""
import enum
import logging

import sqlalchemy as sa
from alembic import op

from app.db.migrations.helper import timestamps

# revision identifiers, used by Alembic.
revision = "976573dc98f2"
down_revision = "ca482b679fc1"
branch_labels = None
depends_on = None


class LogLevel(enum.Enum):
    INFO = 1
    DEBUG = 2
    WARN = 3
    ERROR = 4


def upgrade():
    logging.info("running up migrations for create logs table")
    op.create_table(
        "logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("log", sa.Text(length=4096), nullable=False),
        sa.Column(
            "bot_id",
            sa.Integer,
            sa.ForeignKey("bots.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "level",
            sa.types.Enum(LogLevel),
            nullable=False,
        ),
        *timestamps(),
    )


def downgrade():
    logging.info("running down migrations for create logs table")
    op.drop_table("logs")
