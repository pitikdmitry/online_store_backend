# middlewares.py
from aiohttp import web

import marshmallow as ma


async def handle_404(request):
    return web.json_response(request, status=404, content_type="application/json")


async def handle_validation_error(ex):
    return web.json_response(str(ex), status=400, content_type="application/json")


async def handle_internal_server_error(ex):
    return web.json_response(f'Unhandled exception: {request}', status=500, content_type="application/json")


async def handle_500(request):
    return web.json_response(f'Unhandled exception: {request}', status=500, content_type="application/json")


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):

        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override:
                return await override(request)

            return response

        except ma.ValidationError as ex:
            return await handle_validation_error(ex)

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise
        except BaseException as ex:
            return await handle_internal_server_error(ex)

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)