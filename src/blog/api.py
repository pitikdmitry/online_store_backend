import ujson
from aiohttp import web


async def get_all(request: web.Request) -> web.Response:
    # request.match_info['name']

    # try:
    #     request_body = await request.json()
    # except json.decoder.JSONDecodeError as exc:
    #     raise web.HTTPBadRequest(text=str(exc))
    #
    # query_result = await process_request(
    #     app=request.app,
    #     request_body=request_body,
    #     auth_headers=request.get("user", {}).get("auth_headers", {}),
    #     auth_cookies=request.get("user", {}).get("auth_cookies", {}),
    # )

    return web.json_response("Hello world", dumps=ujson.dumps)
