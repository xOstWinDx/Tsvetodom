from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(url=settings.DATABASE_URL, echo=False)

get_async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker(engine)() as session:
        yield session
