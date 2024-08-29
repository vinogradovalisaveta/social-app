from typing import Optional, List

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.users.schemas import (
    UserSchema,
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from app.security.services import get_current_user, authenticate_user
from app.security.token import create_jwt_token_pair
from app.security.token_schema import TokenPairSchema
from app.models import User
from app.users.services import (
    create_user,
    get_all_users,
    update_user,
    get_user_by_username,
    get_user_by_email,
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/")
async def register(
    user: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    db_username = await get_user_by_username(session, username=user.username)
    db_email = await get_user_by_email(session, email=user.email)
    if db_username:
        raise HTTPException(status_code=400, detail="this username is already taken")
    elif db_email:
        raise HTTPException(status_code=400, detail="this email is already taken")
    return await create_user(session=session, user=user)


@user_router.get("/me", response_model=UserSchema)
async def get_current_user_view(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.get("/user/user", response_model=UserSchema)
async def get_user_profile(
    username: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    if username:
        db_user = await get_user_by_username(session=session, username=username)
    else:
        raise HTTPException(status_code=404, detail="user not found")

    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


@user_router.get("/users", response_model=List[UserReadSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session=session)
    return users


@user_router.post("/token", response_model=TokenPairSchema)
async def authenticate(
    session: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    return await create_jwt_token_pair(user_username=user.username)


@user_router.put("/{username}", response_model=UserUpdateSchema)
async def update_user_data(
    username: str,
    user: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if username != current_user.username:
        raise HTTPException(status_code=403, detail="no permission")

    result = await update_user(session, user, current_user)
    return result
