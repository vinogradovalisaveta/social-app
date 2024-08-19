from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.schemas.user import UserCreateSchema
from app.services.auth import encrypt_password


async def create_user(session: AsyncSession, user: UserCreateSchema):
    new_user = User(**user.model_dump())
    new_user.password = await encrypt_password(new_user.password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
