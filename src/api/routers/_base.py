"""Base class for routers."""

from typing import Callable
from fastapi import FastAPI
from src.database import IdeabotDatabase


class RouterBase:
    """Base class for routers."""

    def __init__(
        self,
        app: FastAPI,
        db: IdeabotDatabase,
        auth_fn: Callable,
    ) -> None:
        """Initialize routers."""
        self._db = db
        self._app = app
        self._auth_fn = auth_fn
