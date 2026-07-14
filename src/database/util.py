"""Database utility functions."""

from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
import secrets
import hashlib
import logging
from src.models import IdeasTable, UserTable
from sqlalchemy import Engine, Index

SALT = 12
logger = logging.getLogger(__name__)


def hash_key(key: str):
    """Hashes and salts the key passed."""
    result = hashlib.sha256(key.encode("utf-8")).hexdigest()
    del key
    return result


def add_user(engine: Engine, name: str, admin: bool) -> str:
    """Add user and key."""
    key = secrets.token_urlsafe(32)
    _insert = insert(UserTable)
    stmt = _insert.on_conflict_do_update(
        index_elements=["name"],
        set_={
            "name": _insert.excluded.name,
            "apikey": _insert.excluded.apikey,
        },
    )
    data = {"name": name, "apikey": hash_key(key), "admin": admin}
    with Session(engine) as session:
        session.execute(stmt, [data])
        session.commit()
    return key


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
