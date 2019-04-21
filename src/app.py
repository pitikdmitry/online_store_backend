# -*- coding: utf-8 -*
""" Main application factory and setup
"""
import aiopg.sa
from aiohttp import web

from blog.category_api import get_all as get_all_categories
from blog.post_api import get_all as get_all_posts
from blog.post_api import add as add_post
from middlewares import setup_middlewares
from utils.config import load_config

from utils.const import URL_PREFIX

import aiohttp_cors


def setup_routes(app):
    app.router.add_get(
        f'{URL_PREFIX}/post/get_all',
        get_all_posts,
    )
    app.router.add_post(
        f'{URL_PREFIX}/post/add',
        add_post,
    )
    app.router.add_get(
        f'{URL_PREFIX}/category/get_all',
        get_all_categories,
    )


def setup_routes_cors(app, cors):
    category_get_all_resource = cors.add(app.router.add_resource(f'{URL_PREFIX}/category/get_all'))
    cors.add(category_get_all_resource.add_route("GET", get_all_categories))

    post_add_resource = cors.add(app.router.add_resource(f'{URL_PREFIX}/post/add'))
    cors.add(post_add_resource.add_route("POST", add_post))

    post_get_all_resource = cors.add(app.router.add_resource(f'{URL_PREFIX}/post/get_all'))
    cors.add(post_get_all_resource.add_route("GET", get_all_posts))


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

    app = web.Application(loop=loop,
                          debug=debug_mode)

    # registering middlewares
    setup_middlewares(app)

    app['config'] = config
    cors = aiohttp_cors.setup(app)
    # setup_routes(app)
    setup_routes_cors(app, cors)
    setup_database(app)

    return app
