from pydantic import BaseModel


class LikeBaseSchema(BaseModel):
    user_id: int
    post_id: int


class LikeResponseSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True
