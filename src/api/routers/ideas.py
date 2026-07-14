"""Router for idea management."""

from src.database.tasks import retrieve_ideas, add_idea
from src.models import IdeaFilterModelWithUser, IdeaModel
from typing import Callable
from src.database import IdeabotDatabase
from fastapi import FastAPI, APIRouter, Depends
from src.api.routers._base import RouterBase
import logging


logger = logging.getLogger(__name__)


class IdeasRouter(RouterBase):
    """Router for ideas."""

    def __init__(
        self,
        app: FastAPI,
        db: IdeabotDatabase,
        auth_fn: Callable,
    ) -> None:
        """Initialize class."""
        super().__init__(app, db, auth_fn)
        logger.info("Setting up idea router.")
        self.router = APIRouter(
            prefix="/ideas",
            tags=["ideas"],
            dependencies=[Depends(auth_fn)],
        )
        logger.info("Finished setting up idea router.")

        def get_ideas(
            idea_name: str | list[str] | None = None,
            category: str | list[str] | None = None,
            server_name: str | list[str] | None = None,
            channel_name: str | list[str] | None = None,
            user: str = Depends(self._auth_fn),
        ) -> list[IdeaModel]:
            """Retrieve all ideas."""
            logger.info(f"Got get_ideas request with user {user}")
            filter = IdeaFilterModelWithUser(
                server=server_name,
                channel=channel_name,
                user=user,
                idea_name=idea_name,
                category=category,
            )
            return retrieve_ideas(self._db.engine, filter)

        self.router.add_api_route(
            "/get",
            endpoint=get_ideas,
            methods=["GET"],
        )

        def create_idea(
            idea: str,
            idea_name: str | None = None,
            category: str | None = None,
            server_name: str | None = None,
            channel_name: str | None = None,
            user: str = Depends(self._auth_fn),
        ) -> None:
            """Create an idea."""
            model = IdeaModel(
                idea=idea,
                user=user,
                server=server_name,
                category=category,
                channel=channel_name,
                idea_name=idea_name,
            )
            add_idea(self._db.engine, model)

        self.router.add_api_route(
            "/create",
            endpoint=create_idea,
            methods=["POST"],
        )
