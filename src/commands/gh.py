"""Manage GH commands."""

import logging
from src.database.tasks.users import add_github_account, get_github_account
from src.github.auth import get_github_user_from_token, is_github_enabled
from src.models import GithubDeviceFlowOAuthExceptionResponseModel
from src.commands.util import get_context
from src.github import init_gh_auth, check_token
from interactions import Client, SlashContext, DM, SlashCommand
from src.database import IdeabotDatabase

logger = logging.getLogger(__name__)


class GithubCommand:
    """Class to manage GH commands."""

    def __init__(self, db: IdeabotDatabase, bot: Client) -> None:
        """Initialize class."""
        if not is_github_enabled():
            logger.info(
                "Not setting up Github commands - either GH_CLIENT_ID or GH_TOKEN is missing."
            )
            return

        self._db = db
        self.auth_device_codes: dict[str, str] = {}

        github_initialize_auth_config = SlashCommand(
            name="ideabot",
            description="Ideabot config",
            callback=self.initialize_auth,
            sub_cmd_name="init-gh-auth",
            sub_cmd_description="Initialize Github Authentication",
        )
        github_finish_auth_config = SlashCommand(
            name="ideabot",
            description="Ideabot config",
            callback=self.finalize_auth,
            sub_cmd_name="finish-gh-auth",
            sub_cmd_description="Finish Github Authentication",
        )
        bot.add_command(github_initialize_auth_config)
        bot.add_command(github_finish_auth_config)

    async def initialize_auth(self, ctx: SlashContext) -> None:
        """Initialize auth flow."""
        if not isinstance(ctx.channel, DM):
            await ctx.respond(
                "I'm sorry, Dave. I'm afraid I can't do that.\n\nYou must message me directly to add your GitHub account."
            )
            return

        context = get_context(ctx)
        user = context.user
        auth = init_gh_auth()
        self.auth_device_codes[user] = auth.device_code
        url = auth.verification_uri
        code = auth.user_code
        msg = f"""## Code: {code}

Navigate to the URL below and type in the code above. When finished, run the command "/ideabot finish-gh-auth".
{url}

**NOTE:** No access tokens are stored. You may revoke Github access at any point. The token is only used to validate the Github account belonging to you.
"""
        await ctx.respond(msg)

    async def finalize_auth(self, ctx: SlashContext) -> None:
        """Finalize auth."""
        if not isinstance(ctx.channel, DM):
            await ctx.respond(
                "I'm sorry, Dave. I'm afraid I can't do that.\n\nYou must message me directly to add your GitHub account."
            )
            return
        context = get_context(ctx)
        user = context.user
        device_code = self.auth_device_codes.get(user)
        if device_code is None:
            await ctx.respond(
                "You must initiate auth before you can finalize. Please run /ideabot init-gh-auth first"
            )
            return
        response = check_token(device_code)
        if isinstance(response, GithubDeviceFlowOAuthExceptionResponseModel):
            if response.error == "authorization_pending":
                await ctx.respond(
                    "Please finish completing authentication and try again."
                )
                return
            msg = f"""Received error completing flow:

Error: {response.error}
Description: {response.error_description}
Error URL: {response.error_uri}

Please restart the auth flow.
"""
            await ctx.respond(msg)
            self.auth_device_codes.pop(user)
            return
        self.auth_device_codes.pop(user)
        github_user = get_github_user_from_token(response.access_token)
        del response
        if not isinstance(github_user, str):
            msg = f"""Received error completing flow:

Error: {github_user.status}
Description: {github_user.message}
Error URL: {github_user.documentation_url}

Please restart the auth flow.
"""
            await ctx.respond(msg)
            return
        add_github_account(self._db.engine, user, github_user)
        await ctx.respond(f"Github account {github_user} has been added for you.")

    async def post_issue_to_github(
        self,
        ctx: SlashContext,
        discord_user: str,
        git_repo: str,
        idea_name: str,
        idea: str,
    ) -> None:
        """Post an idea as an issue to Github."""
        gh_account = get_github_account(self._db.engine, discord_user)
        if gh_account is None:
            await ctx.respond("")
