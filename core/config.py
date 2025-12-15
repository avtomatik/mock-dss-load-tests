from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "default_pass"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "mock_dss_db"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "default_pass"
    POSTGRES_DB: str = "mock_dss_db"

    MQ_USER: str = "guest"
    MQ_PASSWORD: str = "guest"
    MQ_HOST: str = "rabbitmq"
    MQ_PORT: int = 5672

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def db_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def mq_url(self) -> str:
        return (
            f"amqp://{self.MQ_USER}:{self.MQ_PASSWORD}@"
            f"{self.MQ_HOST}:{self.MQ_PORT}/"
        )

    @property
    def cache_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = ConfigDict(env_file=".env.local")


settings = Settings()
