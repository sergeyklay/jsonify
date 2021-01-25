"""Drop timstapms fields from Organization

Revision ID: 00a3b8f85223
Revises: 2ad1c0222abd
Create Date: 2021-01-25 20:08:31.266759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00a3b8f85223'
down_revision = '2ad1c0222abd'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite does not support dropping or altering columns.
    # Alembic's batch_alter_table context manager lets you specify
    # the changes in a natural way, and does a little
    #   "make new table - copy data - drop old table - rename new table"
    # dance behind the scenes when using SQLite.
    # For more see: https://alembic.sqlalchemy.org/en/latest/batch.html
    with op.batch_alter_table('organizations') as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('updated_at')


def downgrade():
    # See comments for 'upgrade' function.
    with op.batch_alter_table('organizations') as batch_op:
        batch_op.add_column(
            sa.Column('created_at', sa.TIMESTAMP(),
                      server_default=sa.text('(CURRENT_TIMESTAMP)'),
                      nullable=True))

        batch_op.add_column(
            sa.Column('updated_at', sa.TIMESTAMP(), nullable=True))
