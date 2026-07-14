from src.database.tasks import retrieve_ideas
from src.database import IdeabotDatabase
import logging
from interactions import SlashContext, SlashCommand, Client
from src.models import IdeaFilterModelWithUser

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
            sub_cmd_description="Search by category",
        )
        search_ideas_names_config = SlashCommand(
            name="search",
            description="Search my ideas",
            callback=self.search_ideas_by_name,
            sub_cmd_name="name",
            sub_cmd_description="Search by name",
        )
        bot.add_command(search_ideas_categories_config)
        bot.add_command(search_ideas_names_config)

    async def search_ideas_by_name(self, ctx: SlashContext) -> None:
        """Search ideas."""
        user = ctx.user.global_name
        if not user:
            raise ValueError("Can't determine user!")
        server = ctx.guild
        channel = ctx.channel
        server_name = server.name if server and isinstance(server.name, str) else None
        channel_name = (
            channel.name if channel and isinstance(channel.name, str) else None
        )
        filter = IdeaFilterModelWithUser(
            server=server_name,
            channel=channel_name,
            user=user,
        )
        ideas = retrieve_ideas(self._db.engine, filter)
        component = create_name_search_form(ideas, "name_select")
        await ctx.send("Search your ideas", components=component)

    async def search_ideas_by_category(self, ctx: SlashContext) -> None:
        """Search ideas."""
        user = ctx.user.global_name
        if not user:
            raise ValueError("Can't determine user!")
        server = ctx.guild
        channel = ctx.channel
        server_name = server.name if server and isinstance(server.name, str) else None
        channel_name = (
            channel.name if channel and isinstance(channel.name, str) else None
        )
        filter = IdeaFilterModelWithUser(
            server=server_name,
            channel=channel_name,
            user=user,
        )
        ideas = retrieve_ideas(
            self._db.engine,
            filter,
        )
        component = create_category_search_form(ideas, "category_select")
        await ctx.send("Search your ideas", components=component)


