"""update statistics

Revision ID: a4f024d8b298
Revises: 137fa99ed4b8
Create Date: 2019-11-06 07:12:50.675788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4f024d8b298'
down_revision = '137fa99ed4b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('statistic', sa.Column('grades', sa.TEXT(), nullable=True))
    op.add_column('statistic', sa.Column('ungraded_vacancies', sa.TEXT(), nullable=True))
    op.add_column('statistic', sa.Column('words', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('statistic', 'words')
    op.drop_column('statistic', 'ungraded_vacancies')
    op.drop_column('statistic', 'grades')
    # ### end Alembic commands ###
