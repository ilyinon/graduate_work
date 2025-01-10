import os
import pytest
import asyncio
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.promocodes import ModelBase
from tests.db.pg import get_session
from app.main import app

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

@pytest.fixture(scope='session')
def postgres_container():
    with PostgresContainer("postgres:16.3-alpine") as postgres:
        postgres.start()
        yield postgres

@pytest.fixture(scope='session', autouse=True)
async def initialized_test_db(postgres_container):
    DATABASE_TEST_URL = postgres_container.get_connection_url().replace('postgresql://', 'postgresql+asyncpg://')
    os.environ['DATABASE_TEST_URL'] = DATABASE_TEST_URL

    engine_test = create_async_engine(DATABASE_TEST_URL, echo=False)
    AsyncSessionTestLocal = sessionmaker(
        bind=engine_test, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_session():
        async with AsyncSessionTestLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    # Создаем таблицы
    async with engine_test.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)

    yield

    # Удаляем таблицы после тестов и закрываем соединение
    async with engine_test.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
    await engine_test.dispose()