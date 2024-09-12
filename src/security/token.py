import os
from datetime import timedelta, datetime
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from security.token_schema import TokenPairSchema


def get_token_payload(token: str, token_type: str) -> dict:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")

    if payload.get("type") != token_type:
        raise HTTPException(status_code=401, detail="invalid token")
    if payload.get(USER_IDENTIFIER) is None:
        raise HTTPException(status_code=401, detail="couldn't validadate credentials")

    return payload


def create_jwt_token_pair(user_username: str) -> TokenPairSchema:
    access_token = create_jwt_token(
        {USER_IDENTIFIER: user_username, "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_jwt_token(
        {USER_IDENTIFIER: user_username, "type": "refresh"},
        timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS),
    )

    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


def refresh_access_token(refresh_token: str) -> str:
    payload = get_token_payload(refresh_token, "refresh")
    return create_jwt_token(
        {USER_IDENTIFIER: payload[USER_IDENTIFIER], "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_jwt_token(data: dict, delta: timedelta) -> str:
    expires_delta = datetime.utcnow() + delta
    data.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default-i9i3902849209323m009sfhs90dh")
ALGORITHM = "HS512"
USER_IDENTIFIER = "user_username"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24 * 7
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
