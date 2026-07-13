from src.database.tasks import add_idea
from src.database import IdeabotDatabase
from sqlalchemy import Engine
import re
from typing import cast
from src.models import IdeaModel
import logging
from interactions import Client, Listener, Guild, Message
from interactions.api.events import MessageCreate

logger = logging.getLogger(__name__)

class MentionsListener:
  """Class for component listener."""

  def __init__(self, bot: Client, db: IdeabotDatabase):
    """Initialize class."""
    self._bot = bot
    self._db = db
    self.add_mention_listener()
    logger.info("Initialized mentions listener.")

  async def on_message(self, event: MessageCreate) -> None:
    """Receive bot mentions"""
    message = event.message
    users = []
    async for user in message.mention_users:
      users.append(user.id)
    bot_user = event.client.user.id
    logger.debug(f"Bot user {bot_user} {"" if bot_user in users else "not"} in users {users}")
    if bot_user not in users:
      return
    logger.debug(f"Got message {message}")
    if message.author.bot:
      logger.debug("Got bot message, ignoring")
      return
    bot_mention_prefix = f"<@{bot_user}>"
    if not message.content.strip().startswith(bot_mention_prefix):
      logger.debug("Bot may have been mentioned but message wasn't for bot, ignoring.")
      return
    
    original_message = await message.fetch_referenced_message()
    if original_message:
      _save_replied_message(self._bot, original_message=original_message, reply=message, bot_user_id=int(bot_user), engine=self._db.engine)
      logger.debug(original_message.content)
      await message.add_reaction("\U0001F44D")


  def add_mention_listener(self) -> Listener:
    """Subscribes the mention listener to the bot."""
    listen_func = Listener.create("MessageCreate")
    result = listen_func(self.on_message)
    self._bot.add_listener(result)
    logger.info("Added mentions listener.")
    return result
  
def _save_replied_message(bot: Client, original_message: Message, reply: Message, bot_user_id: int, engine: Engine) -> None:
  """Save idea from a reply."""
  guild = reply.guild
  server_name = guild.name if isinstance(guild, Guild) else ""
  channel = reply.channel
  if channel and isinstance(channel.name, str):
    channel_name = channel.name
  else:
    channel_name = ""
  user = reply.author
  user_name = user.global_name
  idea = original_message.content
  mentions = find_mentions(bot, reply.content, bot_user_id)
  cleaned_reply = clear_all_mentions(reply.content)
  if not user_name:
    raise ValueError("Can't discern user name")
  category, name = parse_category_and_idea_name_from_reply(cleaned_reply, bot_user_id)
  idea_model = IdeaModel(
      server=server_name,
      channel=channel_name,
      idea=idea,
      user=user_name,
      category=category,
      idea_name=name,
  )
  add_idea(engine, idea_model)
  logger.info(f"Got mentions {mentions}")
  for mention in mentions:
    logger.info(f"Adding mention {mention}")
    idea_model.user = mention
    add_idea(engine, idea_model)

def parse_category_and_idea_name_from_reply(reply_content: str, bot_user_id: int) -> tuple[str | None, str | None]:
  """Parses a reply to determine the name and category."""
  regex = re.compile(rf"\<@{bot_user_id}\>")
  reply_content = regex.sub("", reply_content).strip()

  logger.debug(f"Parsing category, name for {reply_content}")
  if not len(reply_content):
    logger.debug("No category, idea name passed")
    return None, None
  if "," not in reply_content:
    logger.debug(f"Category: {reply_content}")
    return reply_content, None
  result = tuple(reply_content.split(",", maxsplit=1))
  print(f"Category: {result[0]}, idea name: {result[1]}")
  return cast(tuple[str | None, str | None], result)

def clear_all_mentions(reply_content: str) -> str:
  """Clears mentions from replies."""
  pattern = re.compile(r"(?: {0,1}?\<@)(\d+)(?:\> {0,1}?)")
  return pattern.sub("", reply_content)

def find_mentions(bot: Client, reply_content: str, bot_user_id: int) -> list[str]:
  """Find all user mentions."""
  logger.info(f"Finding all mentions in {reply_content}")
  pattern = re.compile(r"(?:\<@)(\d+)(?:\>)")
  reply_content = reply_content.replace(f"<@{bot_user_id}>", "")
  user_ids = pattern.findall(reply_content)
  logger.info(f"Found user IDs {user_ids}")
  result = [bot.get_user(user_id) for user_id in user_ids]
  logger.info(f"All mentions: {result}")
  return [user.global_name for user in result if user and user.global_name]
