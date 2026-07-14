"""Constants."""
from dataclasses import dataclass

IDEA_FILE_NAME = "ideas.json"
DEFAULT_DB_PATH = "ideas.db"
SQLITE_CONN_PROTO = "sqlite+pysqlite:///"


@dataclass(frozen=True)
class SearchComponentIDs:
  NAME: str = "name_select"
  CATEGORY: str = "category_select"
