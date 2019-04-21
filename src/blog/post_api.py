# import ujson
from aiohttp import web, MultipartReader, hdrs

from database.models import PostCategories
from utils.const import ROOT_DIR


async def add(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        reader = MultipartReader.from_response(request)
        metadata = None
        filedata = None
        while True:
            part = await reader.next()
            if part is None:
                break

            print(f"part_namne: {part.name}")

            if hdrs.CONTENT_TYPE in part.headers and (part.headers[hdrs.CONTENT_TYPE] == 'image/jpeg' or \
                part.headers[hdrs.CONTENT_TYPE] == 'image/png'):
                metadata = await part.read()
                print(metadata)
                path = ROOT_DIR + '/static/' + part.name + '.jpg'
                with open(ROOT_DIR + '/static/' + part.name + '.jpg', "wb") as f:
                    f.write(metadata)
                continue
            else:
                metadata = await part.text()
                name = part.name
                print(metadata)


            print(part)
        # body = await request.read()

    return web.json_response("OK")


async def get_all(request: web.Request) -> web.Response:
    async with request.app['db'].acquire() as conn:
        result = await conn.execute(PostCategories.select())
        results = await result.fetchall()
        print(results)

    # return web.json_response(results, dumps=ujson.dumps)
