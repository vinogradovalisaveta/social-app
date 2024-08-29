from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.security.password import validate_password
from app.security.token import oauth2_scheme, get_token_payload, USER_IDENTIFIER
from app.models import User


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User:
    try:
        query = select(User).where(User.username == username)
        print(query)
        result = await session.execute(query)
        user = result.scalar_one()

    except NoResultFound:
        raise HTTPException(status_code=401, detail="could not validate credentials")

    if not await validate_password(password, user.password):
        raise HTTPException(status_code=401, detail="could not validate credentials")

    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    payload = await get_token_payload(token, "access")
    try:
        query = select(User).where(User.username == payload[USER_IDENTIFIER])
        print(query)
        result = await session.execute(query)
        result.unique()

        return result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=401, detail="could not validate credentials")
