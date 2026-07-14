"""Fetch ideas."""

from src.models import IdeaFilterModelWithUser
from src.database.tasks import retrieve_ideas
from src.database import IdeabotDatabase
from src.util import format_ideas

from interactions import (
    SlashContext,
    SlashCommandOption,
    OptionType,
    SlashCommand,
    Client,
)


class FetchIdeas:
    """Class to hold function to fetch ideas."""

    def __init__(self, db: IdeabotDatabase, bot: Client):
        """Initialize class."""
        self._db = db
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
            ),
        ]
        fetch_ideas_config = SlashCommand(
            name="remember",
            description="Fetch my ideas",
            options=_fetch_ideas_options,  # ty:ignore[invalid-argument-type]
            callback=self.fetch_ideas,
        )
        bot.add_command(fetch_ideas_config)

    async def fetch_ideas(
        self,
        ctx: SlashContext,
        idea_name: str | None = None,
        category: str | None = None,
    ) -> None:
        """Fetch ideas."""
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
            category=category,
            idea_name=idea_name,
        )
        ideas = retrieve_ideas(
            self._db.engine,
            filter,
        )
        await ctx.send(format_ideas(ideas))
