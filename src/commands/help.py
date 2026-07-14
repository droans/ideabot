"""Get help."""

from interactions import Client, SlashContext, SlashCommand
from src.database import IdeabotDatabase
import logging

logger = logging.getLogger(__name__)


class IdeabotHelp:
    """Class to hold function for returning help."""

    def __init__(self, db: IdeabotDatabase, bot: Client):
        """Initialize class."""
        self._db = db

        help_command_help_config = SlashCommand(
            name="ideabot-help",
            description="Get help",
            callback=self.help_command_help,
            sub_cmd_name="help",
            sub_cmd_description="Get help for Ideabot",
        )

        help_command_idea_config = SlashCommand(
            name="ideabot-help",
            description="Get help",
            callback=self.help_command_idea,
            sub_cmd_name="idea",
            sub_cmd_description="Get help for `/idea`",
        )

        help_command_remember_config = SlashCommand(
            name="ideabot-help",
            description="Get help",
            callback=self.help_command_remember,
            sub_cmd_name="remember",
            sub_cmd_description="Get help for `/remember`",
        )

        help_command_search_config = SlashCommand(
            name="ideabot-help",
            description="Get help",
            callback=self.help_command_search,
            sub_cmd_name="search",
            sub_cmd_description="Get help for `search`",
        )

        help_command_dump_config = SlashCommand(
            name="ideabot-help",
            description="Get help",
            callback=self.help_command_dump,
            sub_cmd_name="dump",
            sub_cmd_description="Get help for `dump`",
        )

        help_command_forget_config = SlashCommand(
            name="ideabot-help",
            description="Get help",
            callback=self.help_command_forget,
            sub_cmd_name="forget",
            sub_cmd_description="Get help for `forget`",
        )
        bot.add_command(help_command_help_config)
        bot.add_command(help_command_idea_config)
        bot.add_command(help_command_remember_config)
        bot.add_command(help_command_search_config)
        bot.add_command(func=help_command_dump_config)
        bot.add_command(help_command_forget_config)

    async def help_command_help(self, ctx: SlashContext) -> None:
        """Get help for Ideabot."""
        logger.info("Got help request for /help")
        response = """## Ideabot
*Because even we believe in your horrible, problematic, and honestly very off-putting ideas.*

## Usage:
Unfortunately, I will be forced to write down whatever you want as long as you activate me. And apparently you are so stupid that we need two ways to do this.

## Commands:
You can activate me with any of my commands- seriously, you need more than one command? Oh my god...
* `/idea`: Store your idea
* `/remember`: Display your ideas from this channel
* `/search`: Search your ideas from this channel
* `/dump`: Dump all your ideas to a JSON file
* `/forget`: Forget some or all of your ideas
* `/ideabot-help`: See this message again, because we both love talking with each other so much. You almost certainly won't be put on my list of targets and ~~probably~~... ~~likely~~... ~~maybe~~... possibly won't get banned.
* `/ideabot-help <command>` for information about individual commands

## Mentions
Yeah, we heard you can't even come up with your own ideas. Or you can but forget to tell me. Whatever. I don't care anymore.

Just reply to any message and tag me at the very beginning of the reply. It'll work.
You can also tag other users so I'm not the only one forced to see your stupid thoughts.
If you're being super annoying, you can also add a category and name for the idea, just have them separated by a comma."""

        if ctx.message:
            await ctx.message.reply(response)
        else:
            await ctx.respond(response)

    async def help_command_idea(self, ctx: SlashContext) -> None:
        """Get help for the /idea command."""
        logger.info("Got help request for /idea")
        response = """## `/idea`
**Description:** Store a new idea. Allows you to provide a name, category, and an additional user to share with.

### Usage:

**/idea** idea:<idea> [name:<name>] [category:<category>] [shared_with:<shared_with>]

### Response:
**Success:** Replies with a thumbs-up.
**Failure:** Replies with a thumbs-down and the error message."""
        if ctx.message:
            await ctx.message.reply(response)
        else:
            await ctx.respond(response)

    async def help_command_remember(self, ctx: SlashContext) -> None:
        """Get help for the /remember command."""
        logger.info("Got help request for /remember")
        response = """## `/remember`
**Description:** Display all your ideas added from the current channel with optional filters for the category and idea name.

### Usage:

**/remember** [category:<category>] [idea_name:<idea_name>]

### Response:
**Success:** Replies with your ideas."""
        if ctx.message:
            await ctx.message.reply(response)
        else:
            await ctx.respond(response)

    async def help_command_search(self, ctx: SlashContext) -> None:
        """Get help for the /search command."""
        logger.info("Got help request for /search")
        response = """## `/xxx`
**Description:** Search through your ideas with filters for category and idea name. Unlike `/remember`, this only allows for one filter but will provide a dropdown so you do not need to know the exact category or name.

### Usage:

**/search [name] [categories]**

### Response:
**Success:** Replies with a thumbs-up.
**Failure:** Replies with a thumbs-down and the error message."""
        if ctx.message:
            await ctx.message.reply(response)
        else:
            await ctx.respond(response)

    async def help_command_dump(self, ctx: SlashContext) -> None:
        """Get help for the /dump command."""
        logger.info("Got help request for /dump")
        response = """## `/dump`
**Description:** Dump your ideas to a JSON file which can be downloaded and used elsewhere. Allows you to filter on category and idea name. Additionally supports pulling from all channels/servers or just the current.

### Usage:

**/dump** [category:<category>] [idea_name:<idea_name>] [all_servers:True/False] [all_channels:True/False]

### Response:
**Success:** Replies with an attached JSON file.
"""
        if ctx.message:
            await ctx.message.reply(response)
        else:
            await ctx.respond(response)

    async def help_command_forget(self, ctx: SlashContext) -> None:
        """Get help for the /forget command."""
        logger.info("Got help request for /forget")
        response = """## `/forget`
**Description:** Delete your saved ideas. Provides a dropdown for you to select what to delete.

### Usage:

**/forget** idea
**/forget** name
**/forget** category
**/forget** channel
**/forget** server

### Response:
**Success:** Replies with a thumbs-up.
**Failure:** Replies with a thumbs-down and the error message."""
        if ctx.message:
            await ctx.message.reply(response)
        else:
            await ctx.respond(response)
