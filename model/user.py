from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    nickname: str = Field(...)
    description: str = Field(...)
    region: str = Field(...)
    image: Optional[str] = Field(default=None)
    # joined_campaign: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
