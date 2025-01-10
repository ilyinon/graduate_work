import pytest
from alembic import command
from alembic.config import Config
from core.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
from tests.models.base import ModelBase
from tests.models.user import User

Base = declarative_base()

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
@pytest.mark.alembic_auto_upgrade  # Добавляем маркер Alembic
def engine():
    engine = create_engine(test_settings.database_dsn_not_async)
    ModelBase.metadata.create_all(bind=engine)
    yield engine

    # ModelBase.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def tables(engine):
    alembic_cfg = Config("/opt/alembic")
    alembic_cfg.set_main_option("script_location", "/opt/alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))

    command.upgrade(alembic_cfg, "head")

    yield
    # command.downgrade(alembic_cfg, "base")


@pytest.fixture(scope="session")
def get_db(engine, tables):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
