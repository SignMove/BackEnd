from pydantic import BaseModel

class Comment(BaseModel):
    user: int
    content: str

class Signature(BaseModel):
    user: int
    sign: str
