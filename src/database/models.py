from sqlalchemy import Table, Column, MetaData, Integer, String

metadata = MetaData()

PostCategories = Table(
    'post_categories',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(length=100)),
)
