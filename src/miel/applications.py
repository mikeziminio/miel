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
from miel.responses import HTMLResponse
from typing import Callable
from http import HTTPMethod


class Application:

    router: dict = {}

    def __init__(self):
        ...

    async def __call__(self, _scope, receive, send):
        scope = Scope.model_validate(_scope)

        # scope.method
        # scope.path
        # scope.query_string

        event = await receive_event(receive)
        if isinstance(event, HTTPRequest):
            response = HTMLResponse(body=b"Hello, it's response")
            await response(scope, receive, send)

        elif isinstance(event, HTTPDisconnect):
            ...

    # TODO: возможно, формировать options автоматически
    def options(self, path: str = ""):
        return self.get_router_decorator(HTTPMethod.OPTIONS, path)

    def get(self, path: str = ""):
        return self.get_router_decorator(HTTPMethod.GET, path)

    def head(self, path: str = ""):
        return self.get_router_decorator(HTTPMethod.HEAD, path)

    def post(self, path: str = ""):
        return self.get_router_decorator(HTTPMethod.POST, path)

    def put(self, path: str = ""):
        return self.get_router_decorator(HTTPMethod.PUT, path)

    def patch(self, path: str = ""):
        return self.get_router_decorator(HTTPMethod.PATCH, path)

    def delete(self, path: str = ""):
        return self.get_router_decorator(HTTPMethod.DELETE, path)

    # TODO: разобраться, нужны ли эти методы
    # CONNECT = 'CONNECT', 'Establish a connection to the server.'
    # TRACE = 'TRACE', 'Perform a message loop-back test along the path to the target.'

    def get_router_decorator(self, method: HTTPMethod, path: str):
        def wrapper(func: Callable) -> Callable:
            self.router[(method, path)] = func
            return func
        return wrapper
