"""Database utility functions."""

from src.database.tasks.users import add_user

import logging
from src.models import IdeasTable, UserTable
from sqlalchemy import Engine, Index

SALT = 12
logger = logging.getLogger(__name__)


def create_idea_table(engine: Engine) -> None:
    """Create idea table."""
    tbl = IdeasTable
    tbl.__table__.create(engine)  # ty:ignore[unresolved-attribute]
    Index("IDX_USER_SERVER_CHANNEL", "user", "server", "channel")
    Index("IDX_USER", "user")
    Index("IDX_USER_SERVER_CHANNEL_CATEGORY", "user", "server", "channel", "category")
    Index("IDX_USER_SERVER_CHANNEL_NAME", "user", "server", "channel", "name")


def create_user_table(engine: Engine) -> str:
    """Create user table and populate with admin account."""
    tbl = UserTable
    tbl.__table__.create(engine)  # ty:ignore[unresolved-attribute]
    return add_user(
        engine=engine,
        name="admin",
        admin=True,
    )
