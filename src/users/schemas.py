from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):

    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=256)
    name: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None


class UserSchema(UserBaseSchema):
    """
    Эта схема представляет полную информацию о пользователе,
    включая его идентификатор (id). Она наследует свойства от
    UserBaseSchema.
    Использование: Эта схема используется для представления
    существующего пользователя, например, при получении данных
    пользователя из базы данных.
    """

    id: int


class UserCreateSchema(BaseModel):
    """
    Эта схема представляет данные, необходимые для создания нового
    пользователя. Она также наследует свойства от UserBaseSchema,
    но дополнительно включает поле password.
    Использование: Эта схема используется для валидации данных,
    которые пользователь предоставляет для регистрации.
    """

    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., max_length=256)


class UserReadSchema(BaseModel):
    username: str
    email: str
    name: str
    location: str
    bio: str

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    password: Optional[str] = None
    name: str
    location: str
    bio: str


class UserSubscribeSchema(BaseModel):
    """
    for subscription/subscriber list
    """

    username: str


class LoginSchema(BaseModel):
    username: str
    password: str
