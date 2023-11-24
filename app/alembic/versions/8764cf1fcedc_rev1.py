"""rev1

Revision ID: 8764cf1fcedc
Revises: 62a06209566d
Create Date: 2023-11-23 22:59:13.457587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8764cf1fcedc'
down_revision: Union[str, None] = '62a06209566d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submitted_tender',
    sa.Column('tender_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['tender_id'], ['tender.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('worked_tender',
    sa.Column('tender_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['tender_id'], ['tender.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.drop_table('in_work_tender')
    op.add_column('deleted_tender', sa.Column('tender_id', sa.UUID(), nullable=True))
    op.create_unique_constraint(None, 'deleted_tender', ['id'])
    op.drop_constraint('deleted_tender_tender_deleted_id_fkey', 'deleted_tender', type_='foreignkey')
    op.create_foreign_key(None, 'deleted_tender', 'tender', ['tender_id'], ['id'], ondelete='CASCADE')
    op.drop_column('deleted_tender', 'tender_deleted_id')
    op.create_unique_constraint(None, 'tender', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tender', type_='unique')
    op.add_column('deleted_tender', sa.Column('tender_deleted_id', sa.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'deleted_tender', type_='foreignkey')
    op.create_foreign_key('deleted_tender_tender_deleted_id_fkey', 'deleted_tender', 'tender', ['tender_deleted_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'deleted_tender', type_='unique')
    op.drop_column('deleted_tender', 'tender_id')
    op.create_table('in_work_tender',
    sa.Column('tender_in_work_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['tender_in_work_id'], ['tender.id'], name='in_work_tender_tender_in_work_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='in_work_tender_pkey')
    )
    op.drop_table('worked_tender')
    op.drop_table('submitted_tender')
    # ### end Alembic commands ###