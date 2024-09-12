import json

from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
from datetime import datetime
from model.dto import Comment, Signature

class Campaign(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(...)
    images: Optional[list[str]] = Field(sa_column=Column(JSON))
    owner: int = Field(...)
    title: str = Field(...)
    goal: int = Field(...)
    content: str = Field(...)
    region: str = Field(...)
    signature: Optional[str] = Field(default="[]")
    signature_id_increment: Optional[int] = Field(default=0)
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
    
    def signature_add(self, signature: Signature):
        signatures = json.loads(self.signature)
        self.signature_id_increment += 1
        new_signature = {
            "id": self.signature_id_increment,
            "user": signature.user,
            "sign": signature.sign
        }
        signatures.append(new_signature)
        self.signature = json.dumps(signatures, ensure_ascii=False)

    def signature_del(self, id: int):
        signatures = json.loads(self.signature)
        signatures = [signature for signature in signatures if signature["id"] != id]
        self.signature = json.dumps(signatures, ensure_ascii=False)
