import os
from logging import config as logging_config

from async_fastapi_jwt_auth import AuthJWT
from core.logger import LOGGING
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PurchaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    project_name: str = "purchase"

    redis_host: str
    redis_port: int

    pg_user: str
    pg_password: str
    pg_host: str
    pg_port: int
    pg_db: str

    authjwt_secret_key: str
    authjwt_algorithm: str = "HS256"

    jwt_access_token_expires_in_seconds: int = 1800
    jwt_refresh_token_expires_in_days: int = 30

    pg_echo: bool = False

    log_level: bool = False

    enable_tracer: bool = True
    jaeger_agent_host: str = "jaeger"
    jaeger_agent_port: int = 6831

    promocode_service_url: str = "http://promocodes:8000/api/v1/promocodes"
    promocode_service_token: str

    auth_server_url: str = "http://auth:8000/api/v1/auth/check_access"

    @property
    def database_dsn(self):
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"

    @property
    def database_dsn_not_async(self):
        return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"


purchase_settings = PurchaseSettings()


@AuthJWT.load_config
def get_config():
    return PurchaseSettings()
