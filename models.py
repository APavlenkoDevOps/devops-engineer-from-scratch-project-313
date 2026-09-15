from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class LinkBase(SQLModel):
    original_url: str
    short_name: str = Field(index=True, unique=True)


class Link(LinkBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LinkCreate(LinkBase):
    pass


class LinkUpdate(SQLModel):
    original_url: Optional[str] = None
    short_name: Optional[str] = None


class LinkResponse(LinkBase):
    id: int
    short_url: str