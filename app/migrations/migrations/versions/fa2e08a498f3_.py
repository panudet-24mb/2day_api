"""empty message

Revision ID: fa2e08a498f3
Revises: 
Create Date: 2020-10-25 19:15:47.912935

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fa2e08a498f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('users_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('users_citizen_id', sa.String(length=14), nullable=True),
    sa.PrimaryKeyConstraint('users_id')
    )
    op.create_table('token',
    sa.Column('token_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=230), nullable=True),
    sa.Column('token_created', sa.DateTime(), nullable=True),
    sa.Column('token_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['users_id'], ['users.users_id'], ),
    sa.PrimaryKeyConstraint('token_id')
    )
    op.create_index(op.f('ix_token_token_created'), 'token', ['token_created'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_token_created'), table_name='token')
    op.drop_table('token')
    op.drop_table('users')
    # ### end Alembic commands ###
