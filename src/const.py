"""Constants."""

from dataclasses import dataclass

IDEA_FILE_NAME = "ideas.json"
DEFAULT_DB_PATH = "ideas.db"
SQLITE_CONN_PROTO = "sqlite+pysqlite:///"


@dataclass(frozen=True)
class ForgetComponentIDs:
    IDEA: str = "idea_forget"
    NAME: str = "name_forget"
    SERVER: str = "server_forget"
    CHANNEL: str = "channel_forget"
    CATEGORY: str = "category_forget"


@dataclass(frozen=True)
class SearchComponentIDs:
    NAME: str = "name_select"
    CATEGORY: str = "category_select"
