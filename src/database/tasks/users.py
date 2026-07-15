"""Tasks related to users."""

import hashlib
from sqlalchemy.dialects.sqlite import insert
import secrets

from sqlalchemy.orm import Session
from src.models import UserTable
from sqlalchemy import select, Engine


def validate_key_return_user(engine: Engine, key: str) -> str | None:
    """Returns the user that a key belongs to."""
    hash_salted_key = hash_key(key)
    del key
    stmt = select(UserTable.name).where(UserTable.apikey == hash_salted_key)
    with Session(engine) as session:
        result = session.execute(stmt).one_or_none()
        return result[0] if result else None


def validate_key_for_admin(engine: Engine, key: str) -> bool:
    """Validate the key is for an admin."""
    hash_salted_key = hash_key(key)
    del key
    stmt = select(UserTable.name, UserTable.admin).where(
        UserTable.apikey == hash_salted_key
    )
    with Session(engine) as session:
        result = session.execute(stmt).one_or_none()
    if not result:
        return False
    return result._asdict()["admin"]


def hash_key(key: str):
    """Hashes and salts the key passed."""
    result = hashlib.sha256(key.encode("utf-8")).hexdigest()
    del key
    return result


def add_user(engine: Engine, name: str, admin: bool, add_api_key: bool = False) -> str:
    """Add user and key."""
    _insert = insert(UserTable)
    key = secrets.token_urlsafe(32)
    stmt = _insert.on_conflict_do_update(
        index_elements=["name"],
        set_={
            "name": _insert.excluded.name,
            **({"apikey": _insert.excluded.apikey,} if add_api_key else {}),
        },
    )
    data = {"name": name, "apikey": hash_key(key), "admin": admin}
    with Session(engine) as session:
        session.execute(stmt, [data])
        session.commit()
    return key
