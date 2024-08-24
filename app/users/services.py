from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas import UserCreateSchema, UserUpdateSchema
from app.security.password import encrypt_password
from app.users.models import User


async def create_user(session: AsyncSession, user: UserCreateSchema):
    new_user = User(**user.model_dump())
    new_user.password = await encrypt_password(new_user.password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def update_user(session: AsyncSession, user_data: UserUpdateSchema, db_user):
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


async def get_all_users(session: AsyncSession):
    users = await session.execute(select(User))
    return users.scalars().all()


async def get_user_by_username(session: AsyncSession, username: str):
    user = await session.execute(select(User).where(User.username == username))
    user = user.scalar_one_or_none()
    return user


async def get_user_by_email(session: AsyncSession, email: str):
    user = await session.execute(select(User).where(User.email == email))
    return user.scalar_one_or_none()
