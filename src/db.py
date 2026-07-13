from src.util import _coerce_list
from typing import cast
from sqlalchemy.orm import Session
import logging
from pathlib import Path
from src.const import SQLITE_CONN_PROTO, DEFAULT_DB_PATH
from sqlalchemy import create_engine, Index, insert, Engine, select
from src.models import IdeaModel, IdeasTable

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


def retrieve_ideas(
  engine: Engine,
  server: str | list[str] | None = None,
  channel: str | list[str] | None = None,
  user: str | list[str] | None = None,
  category: str | list[str] | None = None,
  name: str | list[str] | None = None,
):
  """Retrieve ideas from database."""
  stmt = select(
    IdeasTable.server,
    IdeasTable.channel,
    IdeasTable.idea,
    IdeasTable.user,
    IdeasTable.category,
    IdeasTable.idea_name,
  )
  if server and not server == "All":
    server = _coerce_list(server)
    stmt = stmt.where(
      IdeasTable.server.in_(server)
    )
  if channel and not channel == "All":
    channel = _coerce_list(channel)
    stmt = stmt.where(
      IdeasTable.channel.in_(channel)
    )
  if user and not user == "All":
    user = _coerce_list(user)
    stmt = stmt.where(
      IdeasTable.user.in_(user)
    )
  if category and not category == "All":
    category = _coerce_list(category)
    stmt = stmt.where(
      IdeasTable.category.in_(category)
    )
  if name and not name == "All":
    name = _coerce_list(name)
    stmt = stmt.where(
      IdeasTable.idea_name.in_(name)
    )
  with Session(engine) as session:
    result = session.execute(stmt).all()
    logger.info([idea._asdict() for idea in result])
    return [IdeaModel.model_validate(idea._asdict()) for idea in result]


def add_idea(engine: Engine, idea: IdeaModel):
  """Add an idea."""
  stmt = insert(IdeasTable)
  with Session(engine) as session:
    session.execute(stmt, [idea.model_dump()])
    session.commit()
  logger.info("Added idea to database.")
