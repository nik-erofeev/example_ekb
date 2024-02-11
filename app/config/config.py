from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    DEBUG: bool = True

    DATABASE_USER: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_HOST: str | None = None
    DATABASE_PORT: str | None = None
    DATABASE_NAME: str | None = None

    @property
    def database_url(self) -> str:
        if not all(
            (
                self.DATABASE_USER,
                self.DATABASE_PASSWORD,
                self.DATABASE_HOST,
                self.DATABASE_PORT,
                self.DATABASE_NAME,
            ),
        ):
            raise ValueError(
                "Отсутствуют необходимые данные для подключения к БД",
            )

        return (
            f"postgresql+asyncpg://"  # noqa
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"  # noqa
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"  # noqa
        )


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
