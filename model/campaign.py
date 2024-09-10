from fastapi import UploadFile
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import datetime

class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(...)
    image: Optional[List[str]] = Field(sa_column=Column(JSON))
    # upload_image: Optional[List[UploadFile]]
    owner: int = Field(...)
    title: str = Field(...)
    goal: int = Field(...)
    content: str = Field(...)
    region: str = Field(...)
    signature: Optional[str] = Field(default="[]")
    comment: Optional[str] = Field(default="[]")
