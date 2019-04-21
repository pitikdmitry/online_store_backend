import logging

from sqlalchemy import MetaData, create_engine
from database.models import PostCategories

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
logger = logging.getLogger('init_db')


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[PostCategories])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(PostCategories.insert(), [
        {'title': 'testcat'}
    ])
    conn.close()


if __name__ == '__main__':
    # db_url = DSN.format(**config['postgres'])
    db_url = 'postgresql://wb:wb@localhost:5454/wb'
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
    logger.info('database tables created')
