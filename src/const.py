"""Constants."""

from dataclasses import dataclass

IDEA_FILE_NAME = "ideas.json"
DEFAULT_DB_PATH = "ideas.db"
SQLITE_CONN_PROTO = "sqlite+pysqlite:///"


@dataclass(frozen=True)
class DeleteComponentIDs:
    IDEA: str = "idea_delete"
    NAME: str = "name_delete"
    SERVER: str = "server_delete"
    CHANNEL: str = "channel_delete"
    CATEGORY: str = "category_delete"


@dataclass(frozen=True)
class SearchComponentIDs:
    NAME: str = "name_select"
    CATEGORY: str = "category_select"
