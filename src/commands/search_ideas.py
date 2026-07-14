from src.const import SearchComponentIDs
from src.commands.util import (
    create_category_search_form,
    create_name_search_form,
    get_context,
)
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
        context = get_context(ctx)
        if not context.user:
            raise ValueError("Can't determine user!")
        filter = IdeaFilterModelWithUser(
            server=context.server,
            channel=context.channel,
            user=context.user,
        )
        ideas = retrieve_ideas(self._db.engine, filter)
        component = create_name_search_form(ideas, SearchComponentIDs.NAME)
        await ctx.send("Search your ideas", components=component)

    async def search_ideas_by_category(self, ctx: SlashContext) -> None:
        """Search ideas."""
        context = get_context(ctx)
        if not context.user:
            raise ValueError("Can't determine user!")
        filter = IdeaFilterModelWithUser(
            server=context.server,
            channel=context.channel,
            user=context.user,
        )
        ideas = retrieve_ideas(
            self._db.engine,
            filter,
        )
        component = create_category_search_form(ideas, SearchComponentIDs.CATEGORY)
        await ctx.send("Search your ideas", components=component)
