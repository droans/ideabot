from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.sqlite import INTEGER, TEXT
from sqlalchemy.orm import Mapped, mapped_column

class IdeaModel(BaseModel):
  """Base model for an idea saved to ideas.json"""
  server: str | None = None
  channel: str | None = None
  idea: str
  user: str
  category: str | None = None
  idea_name: str | None = None


class Base(DeclarativeBase):
  """Base SQLAlchemy model."""

class IdeasTable(Base):
  """Ideas table model."""

  __tablename__ = "IDEAS"

  id: Mapped[int] = mapped_column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
  server: Mapped[str] = mapped_column(TEXT, nullable=True)
  channel: Mapped[str] = mapped_column(TEXT, nullable=True)
  idea: Mapped[str] = mapped_column(TEXT, nullable=False)
  user: Mapped[str] = mapped_column(TEXT, nullable=False)
  category: Mapped[str] = mapped_column(TEXT, nullable=True)
  idea_name: Mapped[str] = mapped_column(TEXT, nullable=True)
