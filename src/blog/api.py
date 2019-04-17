import ujson
from aiohttp import web

from database.models import PostCategories


async def get_all(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(PostCategories.select())
        results = await result.fetchall()
        print(results)

    return web.json_response(results, dumps=ujson.dumps)
