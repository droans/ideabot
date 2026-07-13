import json
from src.database.tasks import retrieve_ideas
from src.models import IdeaFilterModelWithUser
from interactions import Client, SlashContext, File, SlashCommand, SlashCommandOption, OptionType
from src.database import IdeabotDatabase

class DumpIdeas:
  """Class to hold function to dump ideas."""
  def __init__(self, db: IdeabotDatabase, bot: Client) -> None:
    """Initialize class."""
    self._db = db
    _dump_ideas_options = [
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
      ),
      SlashCommandOption(
        name="all_servers",
        description="Dump ideas from all servers",
        type=OptionType.BOOLEAN,
        required=False,
      ),
      SlashCommandOption(
        name="all_channels",
        description="Dump ideas from all channels",
        type=OptionType.BOOLEAN,
        required=False,
      ),
    ]
    dump_ideas_config = SlashCommand(
      name="dump",
      description="Dump my ideas",
      options=_dump_ideas_options,  # ty:ignore[invalid-argument-type]
      callback=self.dump_ideas,
    )
    bot.add_command(dump_ideas_config)

  async def dump_ideas(
    self,
    ctx: SlashContext,
    idea_name: str | list[str] | None = None,
    category: str | list[str] | None = None,
    all_servers: bool = False,
    all_channels: bool = False,
  ) -> None:
    """Dump all ideas to a JSON file and send as attachment."""
    user = ctx.user.global_name
    if not user:
      raise ValueError("Cannot determine user!")
    filter = IdeaFilterModelWithUser(user=user)
    server = ctx.guild
    channel = ctx.channel
    server_name = server.name if server and isinstance(server.name, str) else None
    channel_name = channel.name if channel and isinstance(channel.name, str) else None
    if idea_name:
      filter.idea_name = idea_name
    if category:
      filter.category = category
    if not server_name and not all_servers:
      raise ValueError("Cannot get server name!")
    if not channel_name and not all_channels:
      raise ValueError("Cannot get channel name!")
    if not all_servers:
      filter.server = server_name
    if not all_channels:
      filter.channel = channel_name
    data = retrieve_ideas(self._db.engine, filter)
    dumped = json.dumps([idea.model_dump() for idea in data])
    with open("/tmp/ideas.json", "w") as f:
      f.write(dumped)
    await ctx.send(content="Here's your 💩.",file=File(file="/tmp/ideas.json"))