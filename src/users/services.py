from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.schemas import UserCreateSchema, UserUpdateSchema
from security.password import encrypt_password
from users.models import User


async def create_user(session: AsyncSession, user: UserCreateSchema) -> User:
    """
    создает нового пользователя в базе данных.

    session: сессия базы данных (асинхронная).
    user: данные для создания пользователя, полученные из схемы валидации.

    Returns: созданный объект пользователя из базы данных.
    """

    # извлекаем из формы данные
    new_user = User(**user.model_dump())
    # хэшируем пароль
    new_user.password = await encrypt_password(new_user.password)

    # добавляем данные в базу данных и сохраняем
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def update_user(
    session: AsyncSession, user_data: UserUpdateSchema, db_user: User
):
    """
    обновляет данные пользователя в базе данных.

    session: сессия базы данных (асинхронная).
    user_data: данные для обновления пользователя, полученные из схемы валидации.
    db_user: объект пользователя, который нужно обновить, полученный из базы данных.

    Returns: обновленный объект пользователя из базы данных.
    """

    # если в user_data есть пароль, хэшируем и обновляем в базе данных
    if user_data.password:
        password = await encrypt_password(user_data.password)
        db_user.password = password

    db_user.name = user_data.name
    db_user.location = user_data.location
    db_user.bio = user_data.bio

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    """
    делает запрос в базу данных обо всех пользователях
    session: сессия базы данных (асинхронная).


    Returns: список всех зарегистрированных пользователей
    """

    users = await session.execute(select(User))
    users = users.scalars().all()

    return users


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    """
    делает запрос в базу данных о конкретном пользователе
    session: сессия базы данных (асинхронная).
    username: строковое значение юзернейма искомого пользователя

    returns объект класса User или None, если пользователь не найден
    """

    query = await session.execute(select(User).where(User.username == username))
    user = query.scalar_one_or_none()

    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """
    делает запрос в базу данных о конкретном пользователе
    session: сессия базы данных (асинхронная).
    email: строковое значение email искомого пользователя

    returns: объект класса User или None, если пользователь не найден
    """

    query = await session.execute(select(User).where(User.email == email))
    user = query.scalar_one_or_none()

    return user
