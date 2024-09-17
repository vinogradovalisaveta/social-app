from pydantic import BaseModel


class Image(BaseModel):
    id: int
    post_id: int
    filename: str
