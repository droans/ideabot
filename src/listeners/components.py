from src.models import IdeaFilterModelWithUser
from src.database.tasks import retrieve_ideas
from src.database import IdeabotDatabase
import logging
from src.util import format_ideas
from interactions import Guild, Client, Listener
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
        filter = IdeaFilterModelWithUser(
            server=server_name,
            channel=channel_name,
            user=user_name,
        )
        if component_id == "name_select":
            filter.idea_name = ctx.values
            # kwargs["name"] = ctx.values
        if component_id == "category_select":
            filter.category = event.ctx.values
        ideas = retrieve_ideas(
            engine=self._db.engine,
            filters=filter,
        )
        await ctx.send(format_ideas(ideas))

    def add_component_listener(self) -> Listener:
        """Subscribes the mention listener to the bot."""
        listen_func = Listener.create("Component")
        result = listen_func(self.on_component)
        self._bot.add_listener(result)
        logger.info("Added components listener.")
        return result
