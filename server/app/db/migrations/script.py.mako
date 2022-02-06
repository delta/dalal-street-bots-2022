"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import logging
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    logging.info("running up migrations for ${message}")
    ${upgrades if upgrades else "pass"}


def downgrade():
    logging.info("running down migrations for ${message}")
    ${downgrades if downgrades else "pass"}
