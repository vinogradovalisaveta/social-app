from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from app.database import get_session
from app.schemas.user import UserCreateSchema
from app.services.user import create_user, get_user_by_username, get_user_by_email

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def register(
    user: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    new_username = await get_user_by_username(session, username=user.username)
    new_email = await get_user_by_email(session, email=user.email)
    if new_username:
        raise HTTPException(status_code=400, detail="this username is already taken")
    elif new_email:
        raise HTTPException(status_code=400, detail="this email is already taken")
    return await create_user(session=session, user=user)
