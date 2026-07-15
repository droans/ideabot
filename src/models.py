from typing import Literal
from sqlalchemy import CheckConstraint
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.sqlite import INTEGER, TEXT, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column


class IdeaModel(BaseModel):
    """Base model for an idea saved to ideas.json"""

    server: str | None = None
    channel: str | None = None
    idea: str
    user: str
    category: str | None = None
    idea_name: str | None = None


class BaseIdeaFilterModel(BaseModel):
    """Model for filtering ideas."""

    server: str | list[str] | None = None
    channel: str | list[str] | None = None
    category: str | list[str] | None = None
    idea_name: str | list[str] | None = None
    idea: str | list[str] | None = None


class IdeaFilterModelWithUser(BaseIdeaFilterModel):
    """Model for filtering ideas by user."""

    user: str | list[str]


class IdeaFilterModelWithAPIKey(BaseIdeaFilterModel):
    """Model for filtering ideas by API key"""

    api_key: str


class Base(DeclarativeBase):
    """Base SQLAlchemy model."""


class IdeasTable(Base):
    """Ideas table model."""

    __tablename__ = "IDEAS"

    id: Mapped[int] = mapped_column(
        INTEGER, nullable=False, primary_key=True, autoincrement=True
    )
    server: Mapped[str] = mapped_column(TEXT, nullable=True)
    channel: Mapped[str] = mapped_column(TEXT, nullable=True)
    idea: Mapped[str] = mapped_column(TEXT, nullable=False)
    user: Mapped[str] = mapped_column(TEXT, nullable=False)
    category: Mapped[str] = mapped_column(TEXT, nullable=True)
    idea_name: Mapped[str] = mapped_column(TEXT, nullable=True)


class UserTable(Base):
    __tablename__ = "USERS"

    name: Mapped[str] = mapped_column(
        TEXT, nullable=False, unique=True, primary_key=True
    )
    apikey: Mapped[int] = mapped_column(INTEGER, nullable=True)
    admin: Mapped[bool] = mapped_column(
        BOOLEAN,
        CheckConstraint("admin in (0,1)"),
        nullable=False,
    )


class ContextModel(BaseModel):
    """Model for context information."""

    server: str | list[str] | None = None
    channel: str | list[str] | None = None
    user: str


class GithubDeviceFlowInitRequestModel(BaseModel):
    """Model for a response when initiating device flow."""

    device_code: str
    expires_in: int
    interval: int
    user_code: str
    verification_uri: str


class GithubDeviceFlowOAuthResponseModel(BaseModel):
    """Model for a response validating access has been granted."""

    access_token: str
    token_type: Literal["bearer"] = "bearer"
    scope: Literal["read:user"] = "read:user"
