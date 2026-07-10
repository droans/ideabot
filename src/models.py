from pydantic import BaseModel

class IdeaModel(BaseModel):
  """Base model for an idea saved to ideas.json"""
  server: str | None = None
  channel: str | None = None
  idea: str
  user: str
  category: str | None = None
  idea_name: str | None = None