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


def create_idea_search_form(ideas: list[IdeaModel], form_id: str) -> StringSelectMenu:
    """Creates a form for the user to filter which items to select."""
    idea_descs = ["All"]
    for idea in ideas:
        idea = idea.idea
        if idea and idea not in idea_descs:
            idea_descs.append(idea)
    return StringSelectMenu(
        *idea_descs,
        placeholder="Select Idea",
        min_values=0,
        max_values=len(idea_descs),
        custom_id=form_id,
    )


def create_server_search_form(ideas: list[IdeaModel], form_id: str) -> StringSelectMenu:
    """Creates a form for the user to filter which items to select."""
    servers = ["All"]
    for idea in ideas:
        server = idea.server
        if not server:
            server = "Unknown"
        if server and server not in servers:
            servers.append(server)
    return StringSelectMenu(
        *servers,
        placeholder="Select Server",
        min_values=0,
        max_values=len(servers),
        custom_id=form_id,
    )


def create_channel_search_form(
    ideas: list[IdeaModel], form_id: str
) -> StringSelectMenu:
    """Creates a form for the user to filter which items to select."""
    channels = ["All"]
    for idea in ideas:
        channel = idea.channel
        if not channel:
            channel = "Unknown"
        if channel and channel not in channels:
            channels.append(channel)
    return StringSelectMenu(
        *channels,
        placeholder="Select Channel",
        min_values=0,
        max_values=len(channels),
        custom_id=form_id,
    )
