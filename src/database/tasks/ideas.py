"""Tasks related to ideas."""
import logging
from sqlalchemy.orm import Session
from src.util import _coerce_list
from src.models import IdeasTable, IdeaModel
from sqlalchemy import Engine, select, insert

logger = logging.getLogger(__name__)

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
