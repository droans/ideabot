from typing import cast
import logging
from pathlib import Path
from src.const import SQLITE_CONN_PROTO, DEFAULT_DB_PATH
from sqlalchemy import create_engine, Index, Engine
from src.models import IdeasTable

logger = logging.getLogger(__name__)
class IdeabotDatabase:
  _engine: Engine | None = None
  def __init__(self, db_path: str = DEFAULT_DB_PATH):
    self._db_path = db_path
    if not Path(self._db_path).exists():
      # Database not yet created
      self.initialize_db()
    self._create_engine()

  @property
  def engine(self) -> Engine:
    if not self._engine:
      self._create_engine()
    return cast(Engine, self._engine)

  def _create_engine(self) -> None:
      """Creates the engine and the connection to the database if it does not exit."""
      if not self._engine:
          self._engine = create_engine(f"{SQLITE_CONN_PROTO}{self._db_path}")
          self._connection = self._engine.connect()


  def initialize_db(self):
    """Initialize database if it does not yet exist."""
    logger.info("Creating table at {tbl}")
    self._create_engine()
    tbl = IdeasTable
    logger.info(dir(tbl))
    tbl.__table__.create(self._engine)  # ty:ignore[unresolved-attribute]
    Index("IDX_USER_SERVER_CHANNEL", "user", "server", "channel")
    Index("IDX_USER", "user")
    Index("IDX_USER_SERVER_CHANNEL_CATEGORY", "user", "server", "channel", "category")
    Index("IDX_USER_SERVER_CHANNEL_NAME", "user", "server", "channel", "name")
