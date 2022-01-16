"""A bunch of utility functions to help with alembic migrations"""

from typing import Tuple

import sqlalchemy as sa
from sqlalchemy import func


def timestamps() -> Tuple[sa.Column, sa.Column]:
    """A utility function which creates "created_at" and "updated_at"
    columns to the given table."""

    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )
