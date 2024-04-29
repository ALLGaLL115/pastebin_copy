"""empty message

Revision ID: ab2cf7f67f8d
Revises: ed94dda8a20e
Create Date: 2024-04-28 09:15:45.553529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab2cf7f67f8d'
down_revision: Union[str, None] = 'ed94dda8a20e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subscriber_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['target_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('subscriber_id', 'target_id')
    )
    op.add_column('messages', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'messages', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_column('messages', 'user_id')
    op.drop_table('subscriptions')
    # ### end Alembic commands ###
