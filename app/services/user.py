from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.schemas.user import UserCreateSchema
from app.services.auth import encrypt_password


async def get_user_by_username(session: AsyncSession, username: str):
    user = await session.execute(select(User).where(User.username == username))
    user = user.scalar()
    return user


async def get_user_by_email(session: AsyncSession, email: str):
    user = await session.execute(select(User).where(User.email == email))
    user = user.scalar()
    return user


async def get_user_by_id(session: AsyncSession, user_id: int):
    user = await session.execute(select(User).where(User.id == user_id))
    user = user.scalar()
    return user


async def create_user(session: AsyncSession, user: UserCreateSchema):
    new_user = User(**user.model_dump())
    new_user.password = await encrypt_password(new_user.password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
