"""Save Ideas."""

from src.database.tasks import add_idea
from src.database import IdeabotDatabase
import logging
from src.models import IdeaModel

from interactions import (
    SlashContext,
    Guild,
    SlashCommandOption,
    OptionType,
    SlashCommand,
    Client,
    User,
)

logger = logging.getLogger(__name__)


class RememberIdea:
    """Class to hold function to save ideas."""

    def __init__(self, db: IdeabotDatabase, bot: Client):
        """Initialize class."""
        self._db = db
        _remember_idea_options = [
            SlashCommandOption(
                name="idea",
                description="My Idea",
                type=OptionType.STRING,
                required=True,
            ),
            SlashCommandOption(
                name="name",
                description="Idea Name",
                type=OptionType.STRING,
                required=False,
            ),
            SlashCommandOption(
                name="category",
                description="Category",
                type=OptionType.STRING,
                required=False,
            ),
            SlashCommandOption(
                name="shared_with",
                description="Share with user",
                type=OptionType.USER,
                required=False,
            ),
        ]
        remember_idea_config = SlashCommand(
            name="idea",
            description="Save my idea",
            options=_remember_idea_options,  # ty:ignore[invalid-argument-type]
            callback=self.remember_idea,
        )
        bot.add_command(remember_idea_config)

    async def remember_idea(
        self,
        ctx: SlashContext,
        category: str | None = None,
        idea: str = "",
        name: str | None = None,
        shared_with: User | None = None,
    ) -> None:
        """Save your idea."""
        result = False
        error_message = ""
        try:
            logger.info("Got idea command!")
            guild = ctx.guild
            if isinstance(guild, Guild):
                server_name = guild.name
            else:
                server_name = ""
            channel = ctx.channel
            if isinstance(channel.name, str):
                channel_name = channel.name
            user = ctx.user
            user_name = user.global_name
            if not user_name:
                raise ValueError("Can't discern username.")
            logger.debug(f"Guild: {guild}")
            logger.debug(f"Server Name: {server_name}")
            logger.debug(f"Channel: {channel}")
            logger.debug(f"Channel Name: {channel_name}")
            logger.info(f"User Name: {user_name}")
            logger.debug(f"Idea: {idea}")
            idea_model = IdeaModel(
                server=server_name,
                channel=channel_name,
                idea=idea,
                user=user_name,
                category=category,
                idea_name=name,
            )
            logger.debug(f"Saving idea {idea_model}")
            add_idea(self._db.engine, idea_model)
            if shared_with and shared_with.global_name:
                logger.info(f"Got share with: {shared_with}")
                idea_model.user = shared_with.global_name
                add_idea(self._db.engine, idea_model)
            result = True
        except Exception as e:  # noqa: E722
            result = False
            error_message = str(e)
            logger.exception(e)
        if result:
            await ctx.send("👍")
            return
        await ctx.send(f"👎 \n\n{error_message}")
