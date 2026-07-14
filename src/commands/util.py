"""Utilities for commands."""

from interactions import StringSelectMenu, SlashContext
from src.models import IdeaModel, ContextModel


def get_context(ctx: SlashContext) -> ContextModel:
    """Creates ContextModel from context."""
    server = ctx.guild
    channel = ctx.channel
    server_name = server.name if server and isinstance(server.name, str) else None
    channel_name = channel.name if channel and isinstance(channel.name, str) else None
    user = ctx.user.global_name or ""
    return ContextModel(
        server=server_name,
        channel=channel_name,
        user=user,
    )


def create_name_search_form(ideas: list[IdeaModel], form_id: str) -> StringSelectMenu:
    """Creates a form for the user to filter which items to select."""
    names = ["All"]
    for idea in ideas:
        name = idea.idea_name
        if name and name not in names:
            names.append(name)
    return StringSelectMenu(
        *names,
        placeholder="Select Name",
        min_values=0,
        max_values=len(names),
        custom_id=form_id,
    )


def create_category_search_form(
    ideas: list[IdeaModel], form_id: str
) -> StringSelectMenu:
    """Creates a form for the user to filter which items to select."""
    categories = ["All"]
    for idea in ideas:
        category = idea.category
        if category and category not in categories:
            categories.append(category)
    return StringSelectMenu(
        *categories,
        placeholder="Select Category",
        min_values=0,
        max_values=len(categories),
        custom_id=form_id,
    )
