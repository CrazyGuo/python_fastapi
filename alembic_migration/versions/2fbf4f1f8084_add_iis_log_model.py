"""add iis_log model

Revision ID: 2fbf4f1f8084
Revises: 9f898f4dc842
Create Date: 2020-11-06 11:31:24.988497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fbf4f1f8084'
down_revision = '9f898f4dc842'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('iislog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('time', sa.String(length=20), nullable=True),
    sa.Column('s_ip', sa.String(length=20), nullable=True),
    sa.Column('cs_method', sa.String(length=10), nullable=True),
    sa.Column('cs_uri_stem', sa.String(length=200), nullable=True),
    sa.Column('cs_uri_query', sa.String(length=100), nullable=True),
    sa.Column('s_port', sa.Integer(), nullable=True),
    sa.Column('cs_username', sa.String(length=20), nullable=True),
    sa.Column('c_ip', sa.String(length=20), nullable=True),
    sa.Column('cs_user_agent', sa.String(length=500), nullable=True),
    sa.Column('sc_status', sa.String(length=200), nullable=True),
    sa.Column('sc_substatus', sa.Integer(), nullable=True),
    sa.Column('sc_win32_status', sa.Integer(), nullable=True),
    sa.Column('sc_bytes', sa.Integer(), nullable=True),
    sa.Column('cs_bytes', sa.Integer(), nullable=True),
    sa.Column('time_taken', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_iislog_c_ip'), 'iislog', ['c_ip'], unique=False)
    op.create_index(op.f('ix_iislog_cs_method'), 'iislog', ['cs_method'], unique=False)
    op.create_index(op.f('ix_iislog_id'), 'iislog', ['id'], unique=False)
    op.create_index(op.f('ix_iislog_s_ip'), 'iislog', ['s_ip'], unique=False)
    op.create_index(op.f('ix_iislog_time'), 'iislog', ['time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_iislog_time'), table_name='iislog')
    op.drop_index(op.f('ix_iislog_s_ip'), table_name='iislog')
    op.drop_index(op.f('ix_iislog_id'), table_name='iislog')
    op.drop_index(op.f('ix_iislog_cs_method'), table_name='iislog')
    op.drop_index(op.f('ix_iislog_c_ip'), table_name='iislog')
    op.drop_table('iislog')
    # ### end Alembic commands ###
