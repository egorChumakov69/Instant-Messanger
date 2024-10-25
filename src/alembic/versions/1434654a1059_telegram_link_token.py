"""telegram link token

Revision ID: 1434654a1059
Revises: 73b21aa3e2aa
Create Date: 2024-10-23 10:05:22.434992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1434654a1059'
down_revision: Union[str, None] = '73b21aa3e2aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('telegram_link_token', sa.String(length=12), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'telegram_link_token')
    # ### end Alembic commands ###
