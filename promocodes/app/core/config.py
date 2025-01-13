import os
from logging import config as logging_config

from async_fastapi_jwt_auth import AuthJWT
from core.logger import LOGGING
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".env"))

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PromocodesSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    project_name: str = "promocodes"

    redis_host: str
    redis_port: int

    pg_user: str
    pg_password: str
    pg_host: str
    pg_port: int
    pg_db: str

    sentry_enable: bool = True
    sentry_dsn: str = "https://c6e15651de424b3321b89771c9ec00bb@o4508310740598784.ingest.de.sentry.io/4508310743941200"
    sentry_traces_sample_rate: float = 1.0

    authjwt_secret_key: str
    authjwt_algorithm: str = "HS256"

    auth_service_url: str = "http://auth:8000/api/v1/auth/check_access"
    auth_sender_role: str = "service,admin"
    auth_timeout: float = 5.0

    jwt_access_token_expires_in_seconds: int = 1800
    jwt_refresh_token_expires_in_days: int = 30

    pg_echo: bool = False

    log_level: bool = False

    enable_tracer: bool = True
    jaeger_agent_host: str = "jaeger"
    jaeger_agent_port: int = 6831

    promocode_service_url: str = "http://promocodes:8000/api/v1/promocodes"

    @property
    def database_dsn(self):
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"

    @property
    def database_dsn_not_async(self):
        return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"


promocodes_settings = PromocodesSettings()


@AuthJWT.load_config
def get_config():
    return PromocodesSettings()
