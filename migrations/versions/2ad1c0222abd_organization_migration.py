"""Organization migration

Revision ID: 2ad1c0222abd
Revises: 
Create Date: 2021-01-18 20:20:05.458893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ad1c0222abd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_uid', sa.String(length=32), nullable=False),
    sa.Column('domain', sa.String(length=512), nullable=True),
    sa.Column('token', sa.Text(), nullable=True),
    sa.Column('token_expires_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('organization_uid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organizations')
    # ### end Alembic commands ###
