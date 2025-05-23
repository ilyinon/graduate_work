from contextlib import asynccontextmanager

from core.config import promocodes_settings
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_async_engine(
    promocodes_settings.database_dsn,
    echo=promocodes_settings.pg_echo,
    future=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=600,
)
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_session_local() -> AsyncSession:
    async with async_session() as session:
        yield session
