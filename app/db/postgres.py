from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from models.db_model import BaseOrm
from settings import settings


class PostgresConnectAsync:
    def __init__(self):
        self.engine = create_async_engine(
                settings.pg_url(), echo=settings.postgres_engine_echo,
                future=True
        )
        pass

    async def create_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseOrm.metadata.create_all)

    async def purge_database(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseOrm.metadata.drop_all)

    def get_session(self):
        async_session = async_sessionmaker(self.engine,
                                           expire_on_commit=False)
        return async_session
