from sqlalchemy import Table, Column, MetaData, Integer, String, ForeignKeyConstraint, DateTime
from sqlalchemy.orm import relationship, mapper, backref

metadata = MetaData()
metadata.clear()

PostCategories = Table(
    'post_categories',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(length=100), nullable=False, unique=True),
)

Post = Table(
    'post',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('category_id', Integer, nullable=False),
    Column('title', String(length=100), nullable=False),
    Column('text', String, nullable=False),
    Column('main_img', String, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('last_updated', DateTime, nullable=False),

    ForeignKeyConstraint(['category_id'], [PostCategories.c.id],
                         name='post_category_id_fkey',
                         ondelete='CASCADE')
)
