from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(url=settings.DATABASE_URL, echo=False)

get_async_session = async_sessionmaker(engine, expire_on_commit=False)
