from passlib.context import CryptContext


async def encrypt_password(password: str) -> str:
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return __pwd_context.hash(password)
