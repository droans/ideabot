import logging
from src.models import IdeaModel
import json
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

def save_idea(idea: IdeaModel) -> None:
  """Saves an idea to the ideas JSON file."""
  ideas = get_ideas() + [idea]
  json_ideas = [idea.model_dump() for idea in ideas]
  with open(IDEA_FILE, "w") as f:
    f.write(json.dumps(json_ideas, indent=4))



  
def get_ideas() -> list[IdeaModel]:
  """Retrieve the ideas stored."""
  create_idea_file_if_not_exists()
  with open(IDEA_FILE) as f:
    data = json.loads(f.read())
    return [IdeaModel.model_validate(idea) for idea in data]


def create_idea_file_if_not_exists():
  """Create the idea file if it does not exist yet."""
  if not IDEA_FILE.exists():
    # Create an empty file
    with open(IDEA_FILE, "w") as f:
      f.write("[]")

