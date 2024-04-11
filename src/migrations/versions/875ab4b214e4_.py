"""empty message

Revision ID: 875ab4b214e4
Revises: e84ee22923c0
Create Date: 2024-04-09 07:26:46.627310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '875ab4b214e4'
down_revision: Union[str, None] = 'e84ee22923c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'id_hash',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.VARCHAR(length=256),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'id_hash',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.VARCHAR(length=8),
               existing_nullable=True)
    # ### end Alembic commands ###