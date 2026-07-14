from typing import Iterable
import logging
from src.models import IdeaModel
from pathlib import Path
from src.const import IDEA_FILE_NAME
import interactions
import os
from dotenv import load_dotenv

IDEA_FILE = Path(IDEA_FILE_NAME)

logger = logging.getLogger(__name__)


def get_token() -> str:
    """Return the token set in the .env file."""
    load_dotenv()
    token = os.environ.get("DISCORD_TOKEN")
    assert isinstance(token, str)
    return token


def create_bot() -> interactions.Client:
    """Create a bot."""
    token = get_token()
    return interactions.Client(token=token)


def _coerce_list(item: str | int | float | list) -> list:
    """Convert `item` into a list with one member."""
    if isinstance(item, str) or isinstance(item, int) or isinstance(item, float):
        return [item]
    if isinstance(item, Iterable):
        return list(item)


def format_ideas(ideas: list[IdeaModel]) -> str:
    """Format ideas for a message."""
    return "\n~~---------------------------------------------~~\n\n".join(
        [_format_idea(idea) for idea in ideas]
    )


def _format_idea(
    idea: IdeaModel,
    include_idea_name: bool = True,
    include_category: bool = True,
    include_server: bool = False,
    include_channel: bool = False,
    include_user: bool = False,
) -> str:
    """Formats an idea for a message response."""
    headers = []
    if include_idea_name and idea.idea_name:
        headers.append(f"## 💡 Idea: {idea.idea_name}\n")
    if include_server and idea.server:
        headers.append(f"**Server:** {idea.server}")
    if include_channel and idea.channel:
        headers.append(f"**Channel:** {idea.channel}")
    if include_user and idea.user:
        headers.append(f"**User:** {idea.user}")
    if include_category and idea.category:
        headers.append(f"**Category:** {idea.category}")
    return f"""{"\n".join(headers)}

  ### Idea:
  ```
  {idea.idea}
  ```"""
