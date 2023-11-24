from dotenv import load_dotenv
from pydantic import ValidationError, Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    telegram_token: str = ''

    postgres_db: str = Field(default='tender_bot')

    postgres_user: str = Field('app')
    postgres_password: str = Field('123qwe')
    postgres_host: str = Field('localhost')
    postgres_port: str = Field('5432')
    postgres_engine_echo: bool = Field(True)

    def pg_url(self):
        return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'


try:
    settings = Settings()
except ValidationError as e:
    print(e)
