from datetime import datetime
from pydantic import BaseModel


class BasePostModel(BaseModel):
    title: str
    body: str


class CreatePostSchema(BasePostModel):
    pass


class ReadPostSchema(BasePostModel):
    author: int
    created_at: datetime
