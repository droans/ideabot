import dataclasses
from src.database.tasks.ideas import delete_ideas
from src.const import DeleteComponentIDs, SearchComponentIDs
from src.models import IdeaFilterModelWithUser
from src.database.tasks import retrieve_ideas
from src.database import IdeabotDatabase
import logging
from src.util import format_ideas
from interactions import Guild, Client, Listener, ComponentContext
from interactions.api.events import Component

logger = logging.getLogger(__name__)


class ComponentsListener:
    """Class for component listener."""

    def __init__(self, bot: Client, db: IdeabotDatabase):
        """Initialize class."""
        self._bot = bot
        self._db = db
        self.add_component_listener()
        logger.info("Initialized components listener.")

    async def on_component(self, event: Component) -> None:
        """Respond to search request."""
        logger.info("Got component request.")
        ctx = event.ctx
        component_id = ctx.custom_id
        guild = ctx.guild
        server_name = guild.name if isinstance(guild, Guild) else ""
        channel = ctx.channel
        if channel and isinstance(channel.name, str):
            channel_name = channel.name
        else:
            channel_name = ""
        user = ctx.author
        user_name = user.global_name
        if not user_name:
            raise ValueError("Can't discern user name")
        search_components = dataclasses.asdict(SearchComponentIDs()).values()
        delete_components = dataclasses.asdict(DeleteComponentIDs()).values()
        if component_id in search_components:
            await self.handle_search_ideas(
                ctx,
                user_name,
                server_name,
                channel_name,
                component_id,
                ctx.values,
            )
        elif component_id in delete_components:
            await self.handle_delete_idea(
                ctx,
                user_name,
                component_id,
                ctx.values,
            )

    async def handle_search_ideas(
        self,
        ctx: ComponentContext,
        user: str,
        server_name: str,
        channel_name: str,
        component: str,
        filters: list[str],
    ) -> None:
        logger.info(
            f"Got search request for user {user} with filters {', '.join(filters)}"
        )
        filter = IdeaFilterModelWithUser(
            server=server_name,
            channel=channel_name,
            user=user,
        )
        if component == SearchComponentIDs.NAME:
            filter.idea_name = filters
        if component == SearchComponentIDs.CATEGORY:
            filter.category = filters
        ideas = retrieve_ideas(
            engine=self._db.engine,
            filters=filter,
        )
        logger.info(
            f"Sending back ideas {','.join([idea.idea_name or '' for idea in ideas])}"
        )
        await ctx.send(format_ideas(ideas))

    async def handle_delete_idea(
        self, ctx: ComponentContext, user: str, component: str, idea_filters: list[str]
    ) -> None:
        """Delete ideas."""
        logger.info(
            f"Got delete request for user {user} with filters {','.join(idea_filters)}"
        )
        result = True
        filter = IdeaFilterModelWithUser(
            user=user,
        )
        _idea_filters = [
            _filter[:-3] for _filter in idea_filters if _filter.endswith("...")
        ]
        if component == DeleteComponentIDs.IDEA:
            filter.idea = _idea_filters
        elif component == DeleteComponentIDs.NAME:
            filter.idea_name = _idea_filters
        elif component == DeleteComponentIDs.SERVER:
            filter.server = _idea_filters
        elif component == DeleteComponentIDs.CHANNEL:
            filter.channel = _idea_filters
        elif component == DeleteComponentIDs.CATEGORY:
            filter.category = _idea_filters
        try:
            delete_ideas(self._db.engine, filter)
        except Exception as e:
            result = False
            error_message = str(e)
            logger.exception(e)
        if result:
            await ctx.send("👍")
            return
        await ctx.send(f"👎 \n\n{error_message}")

    def add_component_listener(self) -> Listener:
        """Subscribes the mention listener to the bot."""
        listen_func = Listener.create("Component")
        result = listen_func(self.on_component)
        self._bot.add_listener(result)
        logger.info("Added components listener.")
        return result
