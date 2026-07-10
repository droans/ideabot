import re
from src.util import save_idea
from typing import cast
from src.models import IdeaModel
import logging
from interactions import Client, Listener, Guild, Message
from interactions.api.events import MessageCreate

logger = logging.getLogger(__name__)

async def on_message(event: MessageCreate) -> None:
  """Receive bot mentions"""
  logger.info("On message.")
  message = event.message
  users = []
  async for user in message.mention_users:
    users.append(user.id)
  bot_user = event.client.user.id
  logger.info(f"Bot user {bot_user} {"" if bot_user in users else "not"} in users {users}")
  if bot_user not in users:
    return
  logger.info(f"Got message {message}")
  if message.author.bot:
    logger.info("Got bot message, ignoring")
    return
  
  original_message = await message.fetch_referenced_message()
  if original_message:
    _save_replied_message(original_message=original_message, reply=message, bot_user_id=int(bot_user))
    logger.info(original_message.content)
    await message.add_reaction("\U0001F44D")

def add_mention_listener(bot: Client) -> Listener:
  """Subscribes the mention listener to the bot."""
  listen_func = Listener.create("MessageCreate")
  result = listen_func(on_message)
  bot.add_listener(result)
  return result
  
def _save_replied_message(original_message: Message, reply: Message, bot_user_id: int) -> None:
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
  if not user_name:
    raise ValueError("Can't discern user name")
  category, name = parse_category_and_idea_name_from_reply(reply.content, bot_user_id)
  idea_model = IdeaModel(
      server=server_name,
      channel=channel_name,
      idea=idea,
      user=user_name,
      category=category,
      idea_name=name,
  )
  save_idea(idea_model)

def parse_category_and_idea_name_from_reply(reply_content: str, bot_user_id: int) -> tuple[str | None, str | None]:
  """Parses a reply to determine the name and category."""
  regex = re.compile(rf"\<@{bot_user_id}\>")
  reply_content = regex.sub("", reply_content).strip()

  logger.info(f"Parsing category, name for {reply_content}")
  if not len(reply_content):
    logger.info("No category, idea name passed")
    return None, None
  if "," not in reply_content:
    logger.info(f"Category: {reply_content}")
    return reply_content, None
  result = tuple(reply_content.split(",", maxsplit=1))
  print(f"Category: {result[0]}, idea name: {result[1]}")
  return cast(tuple[str | None, str | None], result)