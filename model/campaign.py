from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
from datetime import datetime

class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(...)
    images: Optional[list[str]] = Field(sa_column=Column(JSON))
    upload_images: Optional[list[str]]
    owner: int = Field(...)
    title: str = Field(...)
    goal: int = Field(...)
    content: str = Field(...)
    region: str = Field(...)
    signature: Optional[str] = Field(default="[]")
    comment: Optional[str] = Field(default="[]")
