from pydantic import BaseModel


class AccessTokenSchema(BaseModel):
    access_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPairSchema(AccessTokenSchema, RefreshTokenSchema):
    pass
