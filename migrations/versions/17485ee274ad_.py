"""empty message

Revision ID: 17485ee274ad
Revises: 4f9d20f15f9e
Create Date: 2024-07-07 19:50:14.592042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17485ee274ad'
down_revision = '4f9d20f15f9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_image')
    op.drop_table('room')
    with op.batch_alter_table('listing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amenities', sa.String(length=255), nullable=True))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.Text(),
               nullable=False)
        batch_op.alter_column('price',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('image_filename')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listing', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_filename', sa.VARCHAR(length=255), nullable=True))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('price',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=500),
               nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
        batch_op.drop_column('amenities')

    op.create_table('room',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=False),
    sa.Column('price', sa.FLOAT(), nullable=False),
    sa.Column('amenities', sa.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room_image',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('filename', sa.VARCHAR(length=100), nullable=False),
    sa.Column('room_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
