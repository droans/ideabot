"""Save Ideas."""

from src.commands.gh import post_issue_to_github
from typing import cast
from src.github.auth import get_gh_token, is_github_enabled
from github import Github, Auth
from src.commands.util import get_context

from src.database.tasks import add_idea
from src.database import IdeabotDatabase
import logging
from src.models import IdeaModel

from interactions import (
    SlashContext,
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
        self._github = None
        if is_github_enabled():
            logger.info("Github is enabled. Allowing it to be used to save ideas.")
            _remember_idea_options.append(
                SlashCommandOption(
                    name="repo",
                    description="Post as issue to GH repo",
                    type=OptionType.STRING,
                    required=False,
                )
            )
            gh_auth = Auth.Token(token=cast(str, get_gh_token()))
            self._github = Github(auth=gh_auth)

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
        repo: str | None = None,
    ) -> None:
        """Save your idea."""
        result = False
        error_message = ""
        try:
            context = get_context(ctx)
            if not context.user:
                raise ValueError("Can't determine user!")
            assert isinstance(context.server, str)
            assert isinstance(context.channel, str)
            logger.info("Got idea command!")
            logger.debug(f"Server Name: {context.server}")
            logger.debug(f"Channel Name: {context.channel}")
            logger.info(f"User Name: {context.user}")
            idea_model = IdeaModel(
                server=context.server,
                channel=context.channel,
                idea=idea,
                user=context.user,
                category=category,
                idea_name=name,
            )
            logger.debug(f"Saving idea {idea_model}")
            add_idea(self._db.engine, idea_model)
            if shared_with and shared_with.global_name:
                logger.info(f"Got share with: {shared_with}")
                idea_model.user = shared_with.global_name
                add_idea(self._db.engine, idea_model)
            if repo and self._github:
                response = post_issue_to_github(
                    engine=self._db.engine,
                    discord_user=context.user,
                    git_repo=repo,
                    idea_name=name,
                    idea=idea,
                    gh=self._github,
                )
                if response:
                    raise ValueError(response)
            result = True
        except Exception as e:  # noqa: E722
            result = False
            error_message = str(e)
            logger.exception(e)
        if not result:
            await ctx.send(f"👎 \n\n{error_message}")
            return
        await ctx.send("👍")
