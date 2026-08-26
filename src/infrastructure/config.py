import os
from ipaddress import IPv4Network
from typing import Literal

from pydantic import AmqpDsn, BaseModel, Field, IPvAnyNetwork, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    """
    PostgreSQL settings to use it as Database engine.
    """

    url: PostgresDsn = PostgresDsn(
        url='postgresql+asyncpg://user:pass@localhost:5432/sustratio',
    )
    pool_size: int = 10


class RabbitMQSettings(BaseModel):
    """
    RabbitMQ settings to use it as AMQP engine.
    """

    url: AmqpDsn = AmqpDsn(url='amqp://guest:guest@localhost:5672//')
    queue_name: str = 'telemetry'


class OAuth0Settings(BaseModel):
    """
    OAuth0 settings to use it as Authorization engine.
    """

    domain: str = 'autho0.com'
    audience: str = 'sustratio'


class UvicornSettings(BaseModel):
    """
    Uvicorn configuration.
    """

    host: IPvAnyNetwork = IPv4Network(address='127.0.0.1')
    port: int = 8000
    reload: bool = True
    workers: int | None = Field(
        default_factory=lambda: (os.cpu_count() or 1) * 2 + 1,
    )
    use_colors: bool | None = True


class Settings(BaseSettings):
    """
    Controls all the settings for the infrastructure.
    """

    log_level: str = 'INFO'
    environment: str = 'development'

    # Uvicorn configs
    uvicorn: UvicornSettings = Field(default_factory=UvicornSettings)

    # Driver selection flags
    AUTH_ENGINE: Literal['oauth0', 'null_auth'] = 'null_auth'
    DATABASE_ENGINE: Literal['postgres', 'in_memory'] = 'in_memory'
    AMQP_ENGINE: Literal['rabbitmq', 'memory'] | None = None

    # Engine configs
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    rabbitmq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)
    oauth0: OAuth0Settings = Field(default_factory=OAuth0Settings)

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
    )


settings = Settings()
