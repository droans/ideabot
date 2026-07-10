from src.util import get_token
from interactions import Client, Intents

def create_bot() -> Client:
  """Create and return the bot."""
  bot = Client(
    intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT,
    sync_interactions=True,
    asyncio_debug=True,
    delete_unused_application_cmds=True,
  )
  return bot

def start_bot(bot: Client) -> None:
  """Start running the bot."""
  token = get_token()
  bot.start(token=token)
