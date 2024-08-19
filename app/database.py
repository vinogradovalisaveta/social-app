from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///social_db.db"
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autoflush=False, autocommit=False, bind=engine)


async def get_session():
    async with SessionLocal() as session:
        yield session
