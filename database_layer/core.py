import abc
from enum import Enum

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class DB(Enum):
    Postgres = 'postgresql'
    SQLite = 'sqlite'

if settings.DB == DB.Postgres.value:
    engine = create_async_engine(
        url=settings.url,
        echo=settings.ECHO,
        pool_size=settings.DB_POOL_SIZE
    )

elif settings.DB == DB.SQLite.value:
    engine = create_async_engine(url=settings.sqlite_url, echo=settings.ECHO)
else:
    engine = create_async_engine(url=settings.sqlite_url, echo=settings.ECHO)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    @abc.abstractmethod
    def to_schema(self):
        raise NotImplementedError

    def __repr__(self):
        return self.to_schema().__repr__()


async def get_session():
    async with async_session() as session:
        yield session


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
