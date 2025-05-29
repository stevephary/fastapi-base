import secrets
import warnings
from typing import Annotated, Any, Generator, Literal

from fastapi import Depends
from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Session

from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60 * 24 * 7  # 7 days
    PASSWORD_RESET_EXPIRES_MINUTES: int = 15
    EMAIL_VERIFICATION_EXPIRES_MINUTES: int = 1
    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
        ] = []
    
    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]
        
    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        
    #redis
    # REDIS_HOST: str 
    # REDIS_PORT: int = 6379
    # REDIS_USER: str 
    # REDIS_PASSWORD: str 
    # REDIS_DB: int = 0   
    
    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def REDIS_URL(self) -> str:
    #     return MultiHostUrl.build(
    #         scheme="redis",
    #         username=self.REDIS_USER,
    #         password=self.REDIS_PASSWORD,
    #         host=self.REDIS_HOST,
    #         port=self.REDIS_PORT,
    #         path=str(self.REDIS_DB),
    #     )
         
    # CELERY_BROKER_URL: str
    # CELERY_RESULT_BACKEND: str 
    # CELERY_ACCEPT_CONTENT: list[str] = ["json"]
    # CELERY_TASK_SERIALIZER: str = "json"
    # CELERY_RESULT_SERIALIZER: str = "json"
    # CELERY_TIMEZONE: str = "UTC"
    # CELERY_ENABLE_UTC: bool = True
    # CELERY_TASK_TRACK_STARTED: bool = True
    
    # @model_validator(mode="after")
    # def _set_celery_broker_url(self) -> Self:
    #     if not self.CELERY_BROKER_URL:
    #         self.CELERY_BROKER_URL = self.REDIS_URL
    #     return self
    # @model_validator(mode="after")
    # def _set_celery_result_backend(self) -> Self:
    #     if not self.CELERY_RESULT_BACKEND:
    #         self.CELERY_RESULT_BACKEND = self.REDIS_URL
    #     return self


    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)
    
    
settings = Settings()    