from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from decouple import config
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

DB_URL = config("DB_URL")
engine = create_async_engine(DB_URL)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    await engine.dispose()


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
