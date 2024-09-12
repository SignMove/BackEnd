import json

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from model.dto import Comment

class News(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(...)
    image: str = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)
    comment: Optional[str] = Field(default="[]")
    comment_id_increment: Optional[int] = Field(default=0)

    def comment_add(self, comment: Comment):
        comments = json.loads(self.comment)
        self.comment_id_increment += 1
        new_comment = {
            "id": self.comment_id_increment,
            "user": comment.user,
            "content": comment.content
        }
        comments.append(new_comment)
        self.comment = json.dumps(comments, ensure_ascii=False)

    def comment_del(self, id: int):
        comments = json.loads(self.comment)
        comments = [comment for comment in comments if comment["id"] != id]
        self.comment = json.dumps(comments, ensure_ascii=False)
