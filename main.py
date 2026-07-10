from src.listeners import add_component_listener, add_mention_listener
import logging
from src.commands import (
  remember_idea_config,
  fetch_ideas_config,
  search_ideas_categories_config,
  search_ideas_names_config
)
from src.bot import create_bot
from src.util import get_token

logging.basicConfig(
  format="%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
  level=logging.INFO,
)
logger = logging.getLogger(__name__)

logger.info("Commands imported.")
logger.info("Creating bot.")
bot = create_bot()
logger.info("Adding listener.")
add_component_listener(bot)
add_mention_listener(bot)
logger.info("Listener added.")
logger.info("Starting bot up.")
bot.start(token=get_token())

