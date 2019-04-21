import logging

import sqlalchemy
from sqlalchemy import MetaData, create_engine

from database.models import PostCategories, Post

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
logger = logging.getLogger('init_db')


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[PostCategories, Post])


def sample_data(engine):
    conn = engine.connect()
    categories = [
            {'title': 'testcat'},
            {'title': 'interesting'},
            {'title': 'moreinteresting'}
        ]

    for category in categories:
        try:
            conn.execute(PostCategories.insert(), category)
        except sqlalchemy.exc.IntegrityError:
            pass

    conn.close()


def fill_db():
    # config = load_config('/etc')
    db_url = 'postgresql://wb:wb@localhost:5454/wb'
    # db_url = 'postgresql://wb:wb@postgres:5454/wb'
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
    logger.info('database tables created')


if __name__ == '__main__':
    fill_db()
