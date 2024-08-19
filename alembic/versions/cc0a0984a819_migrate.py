"""migrate

Revision ID: cc0a0984a819
Revises: 
Create Date: 2024-08-19 18:51:29.972899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc0a0984a819'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('location', sa.String(length=150), nullable=True),
    sa.Column('bio', sa.String(length=150), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    op.drop_table('users')
    # ### end Alembic commands ###
