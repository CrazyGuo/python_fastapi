"""check field type

Revision ID: 635b9650ffdf
Revises: 6cc5acd6c04f
Create Date: 2020-11-06 13:21:35.216759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '635b9650ffdf'
down_revision = '6cc5acd6c04f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('iislog', 'cs_uri_query',
               existing_type=sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.String(length=200),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('iislog', 'cs_uri_query',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=True)
    # ### end Alembic commands ###