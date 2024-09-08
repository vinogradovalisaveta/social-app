from datetime import datetime

from pydantic import BaseModel


class CommentAddSchema(BaseModel):
    text: str


class CommentReadSchema(CommentAddSchema):
    author_username: str
    created_at: datetime
