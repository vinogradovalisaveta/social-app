from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autoflush=False, autocommit=False, bind=engine)
metadata = MetaData()


async def get_session():
    async with SessionLocal() as session:
        yield session


Base = declarative_base(metadata=metadata)
