from aiohttp import web, MultipartReader, hdrs

from blog.schemas import CategoryResponseSchema
from database.models import PostCategories


async def get_all(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(PostCategories.select())
        results = await result.fetchall()

        schema = CategoryResponseSchema(many=True, strict=True)
        categories = schema.dump(results).data
        print(results)

        return web.json_response(categories, content_type="application/json")
