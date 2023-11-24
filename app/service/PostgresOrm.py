import uuid

from sqlalchemy import select, update, delete, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload

from db.postgres import PostgresConnectAsync
from models.db_model import TenderOrm


class PostgresOrm(PostgresConnectAsync):
    def __init__(self):
        super().__init__()
        self.session = self.get_session()

    async def create_tender(self, name, reg_num, datetime, url):
        async with self.session() as session:
            id_tender = uuid.uuid4()
            stmt = insert(TenderOrm).values(
                {
                    'id': id_tender,
                    "name": name,
                    "registration_number": reg_num,
                    'end_date': datetime,
                    'url': url,
                    'status': 'worked'
                }
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=['url'],
                set_=dict(name=name, end_date=datetime, status='worked')
            )
            await session.execute(stmt)
            await session.commit()

    async def get_tender(self, tender_id: uuid.UUID = None, reg_num: str = None, url: str = None) -> TenderOrm | None:
        async with self.session() as session:
            if tender_id:
                stmt = select(TenderOrm).where(TenderOrm.id == tender_id)
            elif reg_num:
                stmt = select(TenderOrm).where(TenderOrm.registration_number == reg_num)
            elif url:
                stmt = select(TenderOrm).where(TenderOrm.url == url)
            else:
                return None
            result = await session.execute(stmt)
            tender = result.unique().scalars().one()
            return tender

    async def get_tenders(self) -> list[TenderOrm]:
        async with self.session() as session:
            stmt = select(TenderOrm).where(or_(TenderOrm.status == 'worked',
                                               TenderOrm.status == 'submitted'))
            result = await session.execute(stmt)
            tender = result.unique().scalars().all()
            return tender

    async def update_tender(self, tender_id: uuid.UUID, *args, **kwargs):
        async with self.session() as session:
            update_stmt = update(TenderOrm).where(TenderOrm.id == tender_id).values(kwargs)
            await session.execute(update_stmt)
            await session.commit()
            pass

    async def get_tender_with_status(self, status: str):
        async with self.session() as session:
            stmt = select(TenderOrm).where(TenderOrm.status == status)
            result = await session.execute(stmt)
            tender = result.unique().scalars().all()
            return tender
            pass
