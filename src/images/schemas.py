from pydantic import BaseModel


class Image(BaseModel):
    id: int
    image_id: int
    post_id: int
    filename: str
