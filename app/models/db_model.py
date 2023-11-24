import datetime
import uuid
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, UUID, DateTime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class BaseOrm(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                          default=uuid.uuid4(),
                                          unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(),
                                                          onupdate=datetime.datetime.now())
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class TenderOrm(BaseOrm):
    __tablename__ = 'tender'
    name: Mapped[str]
    url: Mapped[str] = mapped_column(unique=True)
    registration_number: Mapped[str] = mapped_column(unique=True)
    end_date: Mapped[datetime.datetime]
    status: Mapped[str]


class SubmittedTender(BaseOrm):
    __tablename__ = 'submitted_tender'
    tender_id = mapped_column(UUID, ForeignKey('tender.id',
                                               ondelete="CASCADE"))
    tender: Mapped['TenderOrm'] = relationship(lazy='joined')


class DeletedTender(BaseOrm):
    __tablename__ = 'deleted_tender'
    tender_id = mapped_column(UUID, ForeignKey('tender.id',
                                               ondelete="CASCADE"))
    tender: Mapped['TenderOrm'] = relationship(lazy='joined')


class WorkedTender(BaseOrm):
    __tablename__ = 'worked_tender'
    tender_id = mapped_column(UUID, ForeignKey('tender.id',
                                               ondelete="CASCADE"))
    tender_in_work: Mapped['TenderOrm'] = relationship(lazy='joined')
