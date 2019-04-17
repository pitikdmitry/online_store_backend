# async def error_middleware(app, handler):
#     """ Return middleware for profiling and error handling
#     """
#
#     async def send_profile(status_code: int, elapsed_time: int, **tags):
#         """ Send request profile to statsd
#         """
#         try:
#             await app['statsd'].timing('response_time', elapsed_time, tags=tags)
#             await app['statsd'].incr('response_code',
#                                      tags={'status_code': status_code, **tags})
#         except Exception:
#             logger.exception('Failed to send request profile to stastd.')
#
#     def form_error_response(
#             status_code: int,
#             message: str = DEFAULT_ERROR_MSG,
#             **extend_body,
#     ) -> aiohttp.web.Response:
#         """
#         Form error response from handler output
#         """
#         body = {'errors': {'message': message, **extend_body}}
#
#         return aiohttp.web.Response(
#             status=status_code,
#             body=json.dumps(body).encode('utf-8'),
#             content_type='application/json',
#         )
#
#     #
#     # Middleware
#     #
#
#     async def middleware_handler(request):
#         """ Profiling and error handling middleware. Sends profile stats to statsd,
#         caputers errors to logging and sentry, and forms correct responses if any
#         exception happend
#         """
#         # Save time when request starts
#         request_started_at = time_ms()
#
#         # Form response or error response in case of exceptions
#         try:
#             response = await handler(request)
#         except CancelledError:
#             raise
#         except Exception as exc:
#             exc_handler = get_exception_handler(exc)
#             response = form_error_response(**exc_handler(exc))
#
#             # Additional log for all 500 to Sentry and logging
#             if response.status == 500:
#                 app['sentry'].user_context({
#                     'id': request.cookies.get('ruid'),
#                     'email': request.get('user', {}).get('email'),
#                 })
#                 # Sentry will react on exception in logging and send it to server
#                 logger.exception(exc)
#
#         # Send request profile to statsd
#         await send_profile(response.status, time_ms() - request_started_at,
#                            endpoint=request.rel_url, method=request.method)
#         return response
#
#     return middleware_handler