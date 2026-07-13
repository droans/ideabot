from src.database.tasks import retrieve_ideas
from src.database import IdeabotDatabase
import logging
from interactions import StringSelectMenu, SlashContext, SlashCommand, Client
from src.models import IdeaModel, IdeaFilterModelWithUser

logger = logging.getLogger(__name__)

class SearchIdeas:
  """Class to hold function to search ideas."""
  def __init__(self, db: IdeabotDatabase, bot: Client):
    """Initialize class."""
    self._db = db
    search_ideas_categories_config = SlashCommand(
      name="search",
      description="Search my ideas",
      callback=self.search_ideas_by_category,
      sub_cmd_name="categories",
      sub_cmd_description="Search by category"
    )
    search_ideas_names_config = SlashCommand(
      name="search",
      description="Search my ideas",
      callback=self.search_ideas_by_name,
      sub_cmd_name="name",
      sub_cmd_description="Search by name"
    )
    bot.add_command(search_ideas_categories_config)
    bot.add_command(search_ideas_names_config)
  async def search_ideas_by_name(
    self,
    ctx: SlashContext
  ) -> None:
    """Search ideas."""
    user = ctx.user.global_name
    server = ctx.guild
    channel = ctx.channel
    server_name = server.name if server and isinstance(server.name, str) else None
    channel_name = channel.name if channel and isinstance(channel.name, str) else None
    filter = IdeaFilterModelWithUser(
      server=server_name,
      channel=channel_name,
      user=user,
    )
    ideas = retrieve_ideas(
      self._db.engine,
      filter
    )
    component = create_name_search_form(ideas)
    await ctx.send("Search your ideas", components=component)


  async def search_ideas_by_category(
    self,
    ctx: SlashContext
  ) -> None:
    """Search ideas."""
    user = ctx.user.global_name
    server = ctx.guild
    channel = ctx.channel
    server_name = server.name if server and isinstance(server.name, str) else None
    channel_name = channel.name if channel and isinstance(channel.name, str) else None
    filter = IdeaFilterModelWithUser(
      server=server_name,
      channel=channel_name,
      user=user,
    )
    ideas = retrieve_ideas(
      self._db.engine,
      filter,
    )
    component = create_category_search_form(ideas)
    await ctx.send("Search your ideas", components=component)


def create_name_search_form(ideas: list[IdeaModel]) -> StringSelectMenu:
  """Creates a form for the user to filter which items to select."""
  names = ["All"]
  _all_names = [idea.idea_name for idea in ideas if idea.idea_name]
  for idea in ideas:
    name = idea.idea_name
    if name and name not in names:
      names.append(name)
  return StringSelectMenu(
    *names,
    placeholder="Select Name",
    min_values=0,
    max_values=len(names),
    custom_id="name_select"
  )

  
def create_category_search_form(ideas: list[IdeaModel]) -> StringSelectMenu:
  """Creates a form for the user to filter which items to select."""
  categories = ["All"]
  _all_categories = [idea.category for idea in ideas if idea.category]
  for idea in ideas:
    category = idea.category
    if category and category not in categories:
      categories.append(category)
  return StringSelectMenu(
    *categories,
    placeholder="Select Category",
    min_values=0,
    max_values=len(categories),
    custom_id="category_select"
  )

