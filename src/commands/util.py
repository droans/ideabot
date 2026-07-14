"""Utilities for commands."""

from interactions import StringSelectMenu
from src.models import IdeaModel


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


def create_category_search_form(ideas: list[IdeaModel], form_id: str) -> StringSelectMenu:
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
