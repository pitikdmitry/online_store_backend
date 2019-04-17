# -*- coding: utf-8 -*
""" Main application factory and setup
"""
from aiohttp import web

from blog.api import get_all
from utils.config import load_config

from utils.const import URL_PREFIX


def setup_routes(app):
    app.router.add_get(
        f'{URL_PREFIX}/post/get_all',
        get_all,
    )


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

    return app
