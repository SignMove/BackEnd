from fastapi import UploadFile
from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    nickname: str = Field(...)
    description: str = Field(...)
    region: str = Field(...)
    image: Optional[str] = Field(default=None)
    # upload_image: Optional[UploadFile]
    created_campaign: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    joined_campaign: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
