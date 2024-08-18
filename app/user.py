from cryptography.utils import deprecated
from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only
from starlette.exceptions import HTTPException

from app.database import get_session
from app.models import User


class UserBaseSchema(BaseModel):
    """
    Эта схема определяет базовые свойства пользователя, которые
    являются общими для всех представлений пользователя.
    Использование: Эта схема используется как основа для других
    схем пользователя, таких как UserSchema и UserCreateSchema.
    """

    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=256)


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


class UserCreateSchema(UserBaseSchema):
    """
    Эта схема представляет данные, необходимые для создания нового
    пользователя. Она также наследует свойства от UserBaseSchema,
    но дополнительно включает поле password.
    Использование: Эта схема используется для валидации данных,
    которые пользователь предоставляет для регистрации.
    """

    password: str = Field(..., max_length=256)


async def encrypt_password(password: str) -> str:
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return __pwd_context.hash(password)


async def create_user(session: AsyncSession, user: UserCreateSchema):
    new_user = User(**user.model_dump())
    new_user.password = await encrypt_password(new_user.password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def register(
    user: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    try:
        return await create_user(session, user)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="this user already exists")
