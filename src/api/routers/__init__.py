"""API routers."""

from .admin import AdminRouter
from .ideas import IdeasRouter

__all__ = (
    "AdminRouter",
    "IdeasRouter",
)
