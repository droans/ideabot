"""Main API class."""
from src.api.routers import IdeasRouter, AdminRouter
from src.database.tasks.users import validate_key_return_user, validate_key_for_admin
from fastapi.security import APIKeyHeader
from fastapi import FastAPI, Security, HTTPException, status
from src.database import IdeabotDatabase

import logging
logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="Authorization")

class IdeabotAPI:
  """Main class for API management."""

  def __init__(self, app: FastAPI, db: IdeabotDatabase) -> None:
    """Initialize class."""
    self._db = db
    self._app = app

  def setup_routers(self) -> None:
    """Setup routers."""
    logger.info("Setting up routers.")
    self.ideas_router = IdeasRouter(app=self._app, db=self._db, auth_fn=self.get_user)
    self._app.include_router(self.ideas_router.router)
    self.admin_router = AdminRouter(app=self._app, db=self._db, auth_fn=self.get_admin)
    self._app.include_router(self.admin_router.router)
    logger.info("Finished setting up routers.")

  def start_api(self) -> FastAPI:
    """Start serving api."""
    self.setup_routers()
    return self._app

  def get_user(self, api_key_header: str = Security(api_key_header)) -> str:
    """Checks if user is authorized and returns the user or raises an exception."""
    if not api_key_header.startswith("Bearer "):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token not provided in proper format."
      )
    key = api_key_header.split("Bearer ")[1]
    user = validate_key_return_user(self._db.engine, key)
    if user:
      return user
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Missing or invalid token."
    )

  def get_admin(self, api_key_header: str = Security(api_key_header)) -> str:
    """Checks if user is admin and returns the user or raises an exception."""
    if not api_key_header.startswith("Bearer "):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token not provided in proper format."
      )
    key = api_key_header.split("Bearer ")[1]
    user = validate_key_return_user(self._db.engine, key)
    admin = validate_key_for_admin(self._db.engine, key)
    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid token."
      )
    if not admin:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Requires admin."
      )
    return user