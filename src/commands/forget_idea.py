"""Create form for deleting ideas, fulfilled by forget listener."""

import logging
from src.const import ForgetComponentIDs
from src.database.tasks import retrieve_ideas
from src.models import IdeaFilterModelWithUser
from src.commands.util import (
    get_context,
    create_idea_search_form,
    create_server_search_form,
    create_channel_search_form,
    create_category_search_form,
)

from interactions import Client, SlashContext, SlashCommand
from src.database import IdeabotDatabase

logger = logging.getLogger(__name__)


class ForgetIdeas:
    """Class to hold the function to forget ideas."""

    def __init__(self, db: IdeabotDatabase, bot: Client):
        """Initialize class."""
        self._db = db

        forget_ideas_by_idea_config = SlashCommand(
            name="forget",
            description="Forget my ideas",
            callback=self.forget_ideas_by_idea,
            sub_cmd_name="idea",
            sub_cmd_description="Forget by idea",
        )
        forget_ideas_by_name_config = SlashCommand(
            name="forget",
            description="Forget my ideas",
            callback=self.forget_ideas_by_name,
            sub_cmd_name="name",
            sub_cmd_description="Forget by name",
        )
        forget_ideas_by_server_config = SlashCommand(
            name="forget",
            description="Forget my ideas",
            callback=self.forget_ideas_by_server,
            sub_cmd_name="server",
            sub_cmd_description="Forget by server",
        )
        forget_ideas_by_channel_config = SlashCommand(
            name="forget",
            description="Forget my ideas",
            callback=self.forget_ideas_by_channel,
            sub_cmd_name="channel",
            sub_cmd_description="Forget by channel",
        )
        forget_ideas_by_category_config = SlashCommand(
            name="forget",
            description="Forget my ideas",
            callback=self.forget_ideas_by_category,
            sub_cmd_name="category",
            sub_cmd_description="Forget by category",
        )
        bot.add_command(forget_ideas_by_idea_config)
        bot.add_command(forget_ideas_by_name_config)
        bot.add_command(forget_ideas_by_server_config)
        bot.add_command(forget_ideas_by_channel_config)
        bot.add_command(forget_ideas_by_category_config)

    async def forget_ideas_by_idea(
        self,
        ctx: SlashContext,
    ) -> None:
        """Create form for deleting ideas based on the idea itself."""
        logger.info("Got request to forget idea by idea")
        context = get_context(ctx)
        if not context.user:
            raise ValueError("Can't determine user!")
        filter = IdeaFilterModelWithUser(
            user=context.user,
        )
        user_ideas = retrieve_ideas(self._db.engine, filter)
        logger.debug(
            f"Got all ideas: `{'`, `'.join([idea.idea[:100].replace('\n', '') for idea in user_ideas])}`"
        )
        trimmed_ideas = []
        for idea in user_ideas:
            if len(idea.idea) > 100:
                idea.idea = f"{idea.idea[:97]}..."
            trimmed_ideas.append(idea)
        logger.debug(
            f"Got trimmed ideas: `{'`, `'.join([idea.idea[:100].replace('\n', '') for idea in trimmed_ideas])}`"
        )
        component = create_idea_search_form(trimmed_ideas, ForgetComponentIDs.IDEA)
        await ctx.send("Select ideas to forget", components=component)

    async def forget_ideas_by_name(
        self,
        ctx: SlashContext,
    ) -> None:
        """Create form for deleting ideas based on the names."""
        logger.info("Got request to forget idea by names")
        context = get_context(ctx)
        if not context.user:
            raise ValueError("Can't determine user!")
        filter = IdeaFilterModelWithUser(
            user=context.user,
        )
        user_ideas = retrieve_ideas(self._db.engine, filter)
        logger.info(
            f"Got all ideas: `{'`, `'.join([idea.idea[:100] for idea in user_ideas])}`"
        )
        component = create_idea_search_form(user_ideas, ForgetComponentIDs.NAME)
        await ctx.send("Select idea names to forget", components=component)

    async def forget_ideas_by_server(
        self,
        ctx: SlashContext,
    ) -> None:
        """Create form for deleting ideas based on the server."""
        logger.info("Got request to forget idea by server")
        context = get_context(ctx)
        if not context.user:
            raise ValueError("Can't determine user!")
        filter = IdeaFilterModelWithUser(
            user=context.user,
        )
        user_ideas = retrieve_ideas(self._db.engine, filter)
        logger.info(
            f"Got all ideas: `{'`, `'.join([idea.idea[:100] for idea in user_ideas])}`"
        )
        component = create_server_search_form(user_ideas, ForgetComponentIDs.SERVER)
        await ctx.send("Select servers to forget", components=component)

    async def forget_ideas_by_channel(
        self,
        ctx: SlashContext,
    ) -> None:
        """Create form for deleting ideas based on the channel."""
        logger.info("Got request to forget idea by channel")
        context = get_context(ctx)
        if not context.user:
            raise ValueError("Can't determine user!")
        filter = IdeaFilterModelWithUser(
            user=context.user,
        )
        user_ideas = retrieve_ideas(self._db.engine, filter)
        logger.info(
            f"Got all ideas: `{'`, `'.join([idea.idea[:100] for idea in user_ideas])}`"
        )
        component = create_channel_search_form(user_ideas, ForgetComponentIDs.CHANNEL)
        await ctx.send("Select channels to forget", components=component)

    async def forget_ideas_by_category(
        self,
        ctx: SlashContext,
    ) -> None:
        """Create form for deleting ideas based on the category."""
        logger.info("Got request to forget idea by category")
        context = get_context(ctx)
        if not context.user:
            raise ValueError("Can't determine user!")
        filter = IdeaFilterModelWithUser(
            user=context.user,
        )
        user_ideas = retrieve_ideas(self._db.engine, filter)
        logger.info(
            f"Got all ideas: `{'`, `'.join([idea.idea[:100] for idea in user_ideas])}`"
        )
        component = create_category_search_form(user_ideas, ForgetComponentIDs.CATEGORY)
        await ctx.send("Select categories to forget", components=component)
