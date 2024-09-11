from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class News(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(...)
    image: str = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)
    comment: Optional[str] = Field(default="[]")
