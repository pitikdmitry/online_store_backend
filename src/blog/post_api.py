import logging
from datetime import datetime

from aiohttp import web, MultipartReader, hdrs

from database.category_queries import get_category_by_title
from database.models import PostCategories
from database.post_queries import add_post
from utils.const import ROOT_DIR


logger = logging.getLogger('post_api')


async def add(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        reader = MultipartReader.from_response(request)
        data = {}

        while True:
            part = await reader.next()
            if part is None:
                break

            logger.debug(f"part_name: {part.name}")

            if hdrs.CONTENT_TYPE in part.headers and (part.headers[hdrs.CONTENT_TYPE] == 'image/jpeg' or \
                part.headers[hdrs.CONTENT_TYPE] == 'image/png'):
                metadata = await part.read()
                path = ROOT_DIR + '/static/' + part.name + '.jpg'
                with open(path, "wb") as f:
                    f.write(metadata)

                data['main_img'] = path
            else:
                metadata = await part.text()

                if part.name == 'category':
                    category_id = await get_category_by_title(conn, title=metadata)
                    data['category_id'] = category_id
                    logger.info(f'category_id: {category_id}')
                else:
                    data[part.name] = metadata

        current_time = datetime.now()
        data['created_at'] = current_time
        data['last_updated'] = current_time

        await add_post(conn, data)

    return web.json_response("OK")


async def get_all(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(PostCategories.select())
        results = await result.fetchall()
        print(results)

    # return web.json_response(results, dumps=ujson.dumps)
