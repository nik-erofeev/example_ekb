"""add code

Revision ID: a0d71f9983ec
Revises: dea40de81a34
Create Date: 2024-02-10 02:33:08.324999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0d71f9983ec'
down_revision = 'dea40de81a34'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('codes',
    sa.Column('unique_product_code', sa.String(length=30), nullable=False),
    sa.Column('is_aggregated', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('aggregated_at', sa.DateTime(), nullable=True),
    sa.Column('shift_task_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['shift_task_id'], ['shift_tasks.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('unique_product_code')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('codes')
    # ### end Alembic commands ###
