"""Add image_filename to listing

Revision ID: 4f9d20f15f9e
Revises: 
Create Date: 2024-07-05 14:58:47.135415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f9d20f15f9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_filename', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('date', sa.DateTime(timezone=True), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listing', schema=None) as batch_op:
        batch_op.drop_column('date')
        batch_op.drop_column('image_filename')

    # ### end Alembic commands ###
