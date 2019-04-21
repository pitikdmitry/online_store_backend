from aiohttp import web

from blog.schemas import CategoryResponseSchema
from database.category_queries import get_all as get_all_categories


async def get_all(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        raw_categories = await get_all_categories(conn)

        schema = CategoryResponseSchema(many=True, strict=True)
        categories = schema.dump(raw_categories).data

        return web.json_response(categories, content_type="application/json")
