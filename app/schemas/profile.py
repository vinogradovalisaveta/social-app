from pydantic import BaseModel


class BaseProfileSchema(BaseModel):
    name: str
    location: str
    bio: str


class UpdateProfileSchema(BaseProfileSchema):
    pass


class ProfileSchema(BaseProfileSchema):
    id: int
    user_id: int
