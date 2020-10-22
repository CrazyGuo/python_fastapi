"""first commit

Revision ID: 9f898f4dc842
Revises: 
Create Date: 2020-10-13 15:58:00.343592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f898f4dc842'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appusers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appusers_email'), 'appusers', ['email'], unique=True)
    op.create_index(op.f('ix_appusers_full_name'), 'appusers', ['full_name'], unique=False)
    op.create_index(op.f('ix_appusers_id'), 'appusers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_appusers_id'), table_name='appusers')
    op.drop_index(op.f('ix_appusers_full_name'), table_name='appusers')
    op.drop_index(op.f('ix_appusers_email'), table_name='appusers')
    op.drop_table('appusers')
    # ### end Alembic commands ###
