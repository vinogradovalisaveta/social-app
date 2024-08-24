from datetime import datetime
from pydantic import BaseModel


class CreatePostSchema(BaseModel):
    title: str
    body: str


class ReadPostSchema(BaseModel):
    author: int
    title: str
    body: str
    created_at: datetime
