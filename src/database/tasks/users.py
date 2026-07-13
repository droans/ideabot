"""Tasks related to users."""
from sqlalchemy.orm import Session
from src.models import UserTable
from sqlalchemy import select, Engine
from src.database.util import hash_key

def validate_key_return_user(engine: Engine, key: str) -> str | None:
  """Returns the user that a key belongs to."""
  hash_salted_key = hash_key(key)
  del key
  stmt = select(UserTable.name).where(
    UserTable.apikey == hash_salted_key
  )
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

  