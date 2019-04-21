import logging

import sqlalchemy
from sqlalchemy import MetaData, create_engine
from database.models import PostCategories, Post
from utils.config import load_config

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
logger = logging.getLogger('init_db')


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[PostCategories, Post])


def sample_data(engine):
    conn = engine.connect()

    try:
        conn.execute(PostCategories.insert(), [
            {'title': 'testcat'},
            {'title': 'interesting'}
        ])
    except sqlalchemy.exc.IntegrityError:
        pass
    finally:
        conn.close()


if __name__ == '__main__':
    # config = load_config('/etc')
    db_url = 'postgresql://wb:wb@localhost:5454/wb'
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
    logger.info('database tables created')
