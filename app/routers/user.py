from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.user import UserCreateSchema
from app.services.user import create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def register(
    user: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    return await create_user(session, user)
