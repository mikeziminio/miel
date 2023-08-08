from typing import Callable, Any
from http import HTTPMethod
import asyncio
import functools
from .asgi import (
    Scope,
    receive_event,
    send_event,
    HTTPRequest,
    HTTPDisconnect,
    HTTPResponseStart,
    HTTPResponseBody,
    HTTPStatus
)
from .responses import Response, HTMLResponse
from .router import Router


def is_async_callable(obj: Any) -> Any:
    while isinstance(obj, functools.partial):
        obj = obj.func

    return asyncio.iscoroutinefunction(obj) or (
        callable(obj) and asyncio.iscoroutinefunction(obj.__call__)
    )

class Application:

    router: Router

    def __init__(self):
        self.router = Router()

    async def __call__(self, _scope, receive, send):
        scope = Scope.model_validate(_scope)

        # scope.method
        # scope.path
        # scope.query_string

        event = await receive_event(receive)
        if isinstance(event, HTTPRequest):
            # response = HTMLResponse(body=b"Hello, it's response")
            # await response(scope, receive, send)
            target = self.router.get_target(scope.path)
            if not target:
                return  # TODO: Возвращать 404
            if is_async_callable(target.handler):
                response = await target.handler(**target.vars)
            else:
                response = target.handler(**target.vars)

            if isinstance(response, Response):
                await response(send)
            else:
                # TODO: поставить тут "html / json" - по умолчанию
                await HTMLResponse(body=response)(send)

        elif isinstance(event, HTTPDisconnect):
            ...

    # TODO: возможно, формировать options автоматически
    def options(self, path: str = ""):
        return self.router.func_decorator(HTTPMethod.OPTIONS, path)

    def get(self, path: str = ""):
        return self.router.func_decorator(HTTPMethod.GET, path)

    def head(self, path: str = ""):
        return self.router.func_decorator(HTTPMethod.HEAD, path)

    def post(self, path: str = ""):
        return self.router.func_decorator(HTTPMethod.POST, path)

    def put(self, path: str = ""):
        return self.router.func_decorator(HTTPMethod.PUT, path)

    def patch(self, path: str = ""):
        return self.router.func_decorator(HTTPMethod.PATCH, path)

    def delete(self, path: str = ""):
        return self.router.func_decorator(HTTPMethod.DELETE, path)

    # TODO: разобраться, нужны ли эти методы
    # CONNECT = 'CONNECT', 'Establish a connection to the server.'
    # TRACE = 'TRACE', 'Perform a message loop-back test along the path to the target.'

