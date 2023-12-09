"""Cria tabela contas a pagar e receber

Revision ID: 7e0dfb9738a9
Revises: 
Create Date: 2023-12-09 20:51:32.692641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e0dfb9738a9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contas_a_pagar_e_receber',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('descricao', sa.String(length=40), nullable=True),
    sa.Column('valor', sa.Numeric(), nullable=True),
    sa.Column('tipo', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contas_a_pagar_e_receber')
    # ### end Alembic commands ###
