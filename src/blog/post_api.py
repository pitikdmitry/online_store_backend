import copy
import logging
from datetime import datetime

from aiohttp import web, MultipartReader, hdrs

from blog.api_utils import get_file_format, get_random_filename
from blog.schemas import PostRequestSchema, PostResponseSchema, GetPostsRequestSchema
from database.category_queries import get_category_by_title
from database.post_queries import add_post, get_all_by_category_id
from database.post_queries import get_all as get_all_posts
from utils.const import ROOT_DIR

logger = logging.getLogger('post_api')


async def add(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        reader = MultipartReader.from_response(request)
        request_data = {}

        while True:
            part = await reader.next()
            if part is None:
                break

            logger.debug(f"part_name: {part.name}")

            if hdrs.CONTENT_TYPE in part.headers and part.headers[hdrs.CONTENT_TYPE].startswith('image'):
                metadata = await part.read()

                filename = get_random_filename()
                filename += get_file_format(part.headers[hdrs.CONTENT_TYPE])
                db_path = '/static/' + filename
                path = ROOT_DIR + db_path

                with open(path, "wb") as f:
                    f.write(metadata)

                request_data[part.name] = db_path
            else:
                metadata = await part.text()
                request_data[part.name] = metadata

        current_time = datetime.now().isoformat()
        request_data['created_at'] = current_time
        request_data['last_updated'] = current_time

        schema = PostRequestSchema(strict=True)
        request = schema.load(request_data).data

        category_id = await get_category_by_title(conn, request['category'])
        request['category_id'] = category_id

        await add_post(conn, request)

    return web.json_response("Ok")


async def get_all(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        schema = GetPostsRequestSchema(strict=True)
        request = schema.load(request.rel_url.query).data

        if request.get('category'):
            category_id = await get_category_by_title(conn, request['category'])
            request['category_id'] = category_id
            raw_posts = await get_all_by_category_id(conn, request)
        else:
            raw_posts = await get_all_posts(conn, request)

        schema = PostResponseSchema(many=True, strict=True)
        posts = schema.dump(raw_posts).data

    return web.json_response(posts)
