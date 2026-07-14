from src.database.util import create_idea_table, create_user_table
from typing import cast
import logging
from pathlib import Path
from src.const import SQLITE_CONN_PROTO, DEFAULT_DB_PATH
from sqlalchemy import create_engine, Engine

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
        logger.debug("Creating table at {tbl}")
        self._create_engine()
        create_idea_table(self.engine)
        admin_token = create_user_table(self.engine)
        logger.info(f"⚠️⚠️⚠️ Admin token: `{admin_token}` ⚠️⚠️⚠️")
        del admin_token
