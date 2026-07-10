"""Fetch ideas."""
from src.util import filter_ideas, format_ideas

from interactions import SlashContext, SlashCommandOption, OptionType, SlashCommand

async def fetch_ideas(
  ctx: SlashContext,
  idea_name: str | None = None,
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
  await ctx.send(format_ideas(ideas))

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

