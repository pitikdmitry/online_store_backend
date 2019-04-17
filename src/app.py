# -*- coding: utf-8 -*
""" Main application factory and setup
"""
import aiopg.sa
import sqlalchemy as sa
from aiohttp import web

from blog.api import get_all
from utils.config import load_config

from utils.const import URL_PREFIX
from databases import Database


def setup_routes(app):
    app.router.add_get(
        f'{URL_PREFIX}/post/get_all',
        get_all,
    )


def setup_database(app):
    async def init_pg(app):
        conf = app['config']['postgres']
        engine = await aiopg.sa.create_engine(
            database=conf['database'],
            user=conf['user'],
            password=conf['password'],
            host=conf['host'],
            port=conf['port'],
        )
        app['db'] = engine

    async def close_pg(app):
        app['db'].close()
        await app['db'].wait_closed()

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)


def create_app(config_path, loop):
    """ Setups aiohttp web application instance
    """
    # Load configuration from path
    config = load_config(config_path)

    # Debug mode
    debug_mode = config.get('app', {}).get('debug', False)

    # registering middlewares
    # middlewares = [error_middleware]
    middlewares = []

    app = web.Application(loop=loop,
                          middlewares=middlewares,
                          debug=debug_mode)

    app['config'] = config
    setup_routes(app)
    setup_database(app)

    return app
