from src.database import IdeabotDatabase
from src.listeners import ComponentsListener, MentionsListener
import logging
from src.commands import (
  FetchIdeas,
  RememberIdea,
  SearchIdeas,
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
logger.info("Creating DB.")
db = IdeabotDatabase()
logger.info("DB Created.")
logger.info("Adding commands...")
fetch_command = FetchIdeas(db, bot)
save_idea_command = RememberIdea(db, bot)
search_idea_command = SearchIdeas(db, bot)
logger.info("Adding listeners...")
components_listener = ComponentsListener(bot, db)
mentions_listener = MentionsListener(bot, db)
logger.info("Listeners added.")
logger.info("Starting bot up.")
bot.start(token=get_token())

