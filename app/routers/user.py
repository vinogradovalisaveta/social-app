from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.database import get_session
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.user import (
    create_user,
    get_user_by_username,
    get_user_by_email,
    get_user_by_id,
)

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


@router.get("/user/user", response_model=UserSchema)
async def get_user_profile(
    username: Optional[str] = None,
    user_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
):
    if username:
        db_user = await get_user_by_username(session=session, username=username)
    elif user_id:
        db_user = await get_user_by_id(session=session, user_id=user_id)
    else:
        raise HTTPException(status_code=404, detail="user not found")

    if db_user is None:
        raise HTTPException(status_code=404, detail="usernot found")
    return db_user
