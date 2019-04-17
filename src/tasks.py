import asyncio
import logging
from typing import Any

import aiohttp
import aiohttp.test_utils
import click

from app import create_app

logger = logging.getLogger(__name__)


@click.group()
@click.option(
    '--config', default='/app/etc/config/development.yml',
    help='Path to config yaml inside container')
@click.pass_context
def cli(ctx: Any, config: str) -> None:
    """ Process generic commands
    """
    ctx.obj = {}
    ctx.obj['config'] = config


@cli.command(help="Run application development server")
@click.option('--host', default='0.0.0.0', help='')
@click.option('--port', default=8080, help='')
@click.pass_context
def server(ctx: Any, host: str, port: int) -> None:
    loop = asyncio.get_event_loop()
    app = create_app(ctx.obj['config'], loop)
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s @ %(pathname)s:%(lineno)d ~ %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S",
    )
    aiohttp.web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    cli()
