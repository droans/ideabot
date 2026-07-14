"""Tasks related to ideas."""

from src.database.tasks.users import validate_key_return_user
import logging
from sqlalchemy.orm import Session
from src.util import _coerce_list
from src.models import (
    IdeasTable,
    IdeaModel,
    IdeaFilterModelWithUser,
    IdeaFilterModelWithAPIKey,
)
from sqlalchemy import Engine, select, insert

logger = logging.getLogger(__name__)


def retrieve_ideas(
    engine: Engine,
    filters: IdeaFilterModelWithUser,
) -> list[IdeaModel]:
    """Retrieve ideas from database."""
    stmt = select(
        IdeasTable.server,
        IdeasTable.channel,
        IdeasTable.idea,
        IdeasTable.user,
        IdeasTable.category,
        IdeasTable.idea_name,
    )
    if filters.server and not filters.server == "All":
        server = _coerce_list(filters.server)
        stmt = stmt.where(IdeasTable.server.in_(server))
    if filters.channel and not filters.channel == "All":
        channel = _coerce_list(filters.channel)
        stmt = stmt.where(IdeasTable.channel.in_(channel))
    if filters.user and not filters.user == "All":
        user = _coerce_list(filters.user)
        stmt = stmt.where(IdeasTable.user.in_(user))
    if filters.category and not filters.category == "All":
        category = _coerce_list(filters.category)
        stmt = stmt.where(IdeasTable.category.in_(category))
    if filters.idea_name and not filters.idea_name == "All":
        name = _coerce_list(filters.idea_name)
        stmt = stmt.where(IdeasTable.idea_name.in_(name))
    if filters.idea and not filters.idea == "All":
        idea = _coerce_list(filters.idea)
        stmt = stmt.where(IdeasTable.idea.in_(idea))
    with Session(engine) as session:
        result = session.execute(stmt).all()
        return [IdeaModel.model_validate(idea._asdict()) for idea in result]


def retrieve_ideas_by_key(
    engine: Engine,
    filters: IdeaFilterModelWithAPIKey,
) -> list[IdeaModel]:
    """Return all ideas for user by API key."""
    user = validate_key_return_user(engine, filters.api_key)
    if not user:
        return []
    dumped = filters.model_dump()
    dumped.pop("api_key")
    dumped["user"] = user
    model = IdeaFilterModelWithUser.model_validate(dumped)
    return retrieve_ideas(engine, model)


def add_idea(engine: Engine, idea: IdeaModel):
    """Add an idea."""
    stmt = insert(IdeasTable)
    with Session(engine) as session:
        session.execute(stmt, [idea.model_dump()])
        session.commit()
    logger.info("Added idea to database.")
