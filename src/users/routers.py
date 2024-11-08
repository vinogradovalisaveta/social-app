from typing import List
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from security.services import get_current_user, authenticate_user
from security.token import create_jwt_token_pair
from security.token_schema import TokenPairSchema
from users.schemas import (
    UserSchema,
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from users.models import User
from users.services import (
    create_user,
    get_all_users,
    update_user,
    get_user_by_username,
    get_user_by_email,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def register(
    user: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    """
    регистрирует нового пользователя.
    если пользователь с введенным именем пользователя или имейлом существует -
    ошибка 400

    user: данные нового пользователя, полученные из схемы валидации.
    session: асинхронная сессия базы данных.

    returns: созданный объект пользователя.

    """

    # запрос в бд по имени пользователя
    db_username = await get_user_by_username(session=session, username=user.username)
    # запрос в бд по имейлу
    db_email = await get_user_by_email(session=session, email=user.email)

    if db_username:
        raise HTTPException(status_code=400, detail="this username is already taken")
    elif db_email:
        raise HTTPException(status_code=400, detail="this email is already taken")

    # если имя пользователя и имейл не заняты
    user = await create_user(session=session, user=user)
    return user


@router.get("/me", response_model=UserSchema)
async def get_current_user_view(current_user: User = Depends(get_current_user)):
    """
    возвращает текущего пользователя
    """
    return current_user


@router.get("/{username}", response_model=UserSchema)
async def get_user_profile(
    username: str,
    session: AsyncSession = Depends(get_session),
):
    """
    возвращает пользователя по имени пользователя
    username: строковое значение имени пользователя
    session: асинхронная сессия базы данных

    returns: искомый объект пользователя
    """

    user = await get_user_by_username(session=session, username=username)

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    return user


@router.get("/", response_model=List[UserReadSchema])
@cache(expire=0)
async def get_users(session: AsyncSession = Depends(get_session)):
    """
    session: асинхронная сессия базы данных
    returns: список пользователей либо 404
    """
    users = await get_all_users(session=session)

    return users


@router.post("/token", response_model=TokenPairSchema)
async def authenticate(
    session: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    получение пары jwt токенов
    """
    user = await authenticate_user(
        session=session, username=form_data.username, password=form_data.password
    )

    return create_jwt_token_pair(user_username=user.username)


@router.put("/{username}/update", response_model=UserUpdateSchema)
async def update_user_data(
    user: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    обновляет данные текущего пользователя
    user: данные пользователя, полученные из формы валидации
    current_user: текущий пользователь
    """

    result = await update_user(session=session, user_data=user, db_user=current_user)
    return result
