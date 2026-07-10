"""Fetch ideas."""
from src.util import get_ideas

from src.models import IdeaModel
from interactions import SlashContext, SlashCommandOption, OptionType, SlashCommand

async def fetch_ideas(
  ctx: SlashContext,
  idea_name: str | None = None,
  # server: str | None = None,
  # user: str | None = None,
  category: str | None = None,
) -> None:
  """Fetch ideas."""
  user = ctx.user.global_name
  server = ctx.guild
  channel = ctx.channel
  server_name = server.name if server and isinstance(server.name, str) else None
  channel_name = channel.name if channel and isinstance(channel.name, str) else None
  ideas = filter_ideas(
    server=server_name,
    channel=channel_name,
    user=user,
    category=category,
    name=idea_name
  )
  result = "\n~~---------------------------------------------~~\n\n".join([_format_idea(idea) for idea in ideas])
  await ctx.send(result)

_fetch_ideas_options = [
  SlashCommandOption(
  name="category",
  description="Category",
  type=OptionType.STRING,
  required=False,
  ),
  SlashCommandOption(
  name="idea_name",
  description="Idea name",
  type=OptionType.STRING,
  required=False,
  )
]
fetch_ideas_config = SlashCommand(
  name="remember",
  description="Fetch my ideas",
  options=_fetch_ideas_options,  # ty:ignore[invalid-argument-type]
  callback=fetch_ideas,
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

def filter_ideas(
  server: str | None = None,
  channel: str | None = None,
  user: str | None = None,
  category: str | None = None,
  name: str | None = None,
  ) -> list[IdeaModel]:
  """Returns all filtered ideas."""
  ideas = get_ideas()
  if server:
    ideas = [idea for idea in ideas if idea.server == server]
  if channel:
    ideas = [idea for idea in ideas if idea.channel == channel]
  if user:
    ideas = [idea for idea in ideas if idea.user == user]
  if category:
    ideas = [idea for idea in ideas if idea.category == category]
  if name:
    ideas = [idea for idea in ideas if idea.idea_name == name]
  return ideas
