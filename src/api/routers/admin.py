"""Router for idea management."""

from src.database.tasks import add_user

from typing import Callable
from src.database import IdeabotDatabase
from fastapi import FastAPI, APIRouter, Depends
from src.api.routers._base import RouterBase
import logging


logger = logging.getLogger(__name__)


class AdminRouter(RouterBase):
    """Router for admin."""

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
            prefix="/admin",
            tags=["admin"],
            dependencies=[Depends(auth_fn)],
        )
        logger.info("Finished setting up idea router.")

        def insert_user(
            user_name: str,
            admin: bool = False,
            user: dict = Depends(self._auth_fn),
        ) -> str:
            """Create a new user."""
            logger.info(f"Got add_users request with user {user}")
            return add_user(self._db.engine, user_name, admin)

        self.router.add_api_route(
            "/add_user",
            endpoint=insert_user,
            methods=["POST"],
        )
