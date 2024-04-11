"""empty message

Revision ID: e84ee22923c0
Revises: 3b97dd22a7f6
Create Date: 2024-04-09 07:23:50.925254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e84ee22923c0'
down_revision: Union[str, None] = '3b97dd22a7f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'id_hash',
               existing_type=sa.VARCHAR(length=8),
               nullable=True)
    op.alter_column('messages', 'message_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'message_url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('messages', 'id_hash',
               existing_type=sa.VARCHAR(length=8),
               nullable=False)
    # ### end Alembic commands ###