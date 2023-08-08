from .asgi import (
    HTTPResponseStart,
    HTTPResponseBody,
    HTTPStatus,
    send_event
)


class Response:
    content_type: str | None = None
    body: bytes | None = None
    status: HTTPStatus = HTTPStatus.OK

    def __init__(self, *,
                 media_type: str | None = None,
                 body: bytes | None = None,
                 status: HTTPStatus | None = None):
        if media_type is not None:
            self.media_type = media_type
        if body is not None:
            self.body = body
        if status is not None:
            self.status = status

    async def __call__(self, send):

        if not self.content_type:
            raise ValueError(f"content_type должен быть заполнен")
        response_start = HTTPResponseStart(
            status=self.status,
            headers=[[b"content-type", self.content_type]]
        )
        await send_event(send, response_start)
        if self.body:
            response_body = HTTPResponseBody(
                body=self.body
            )
            await send_event(send, response_body)


class HTMLResponse(Response):
    content_type = "text/html"


class PlainTextResponse(Response):
    content_type = "text/plain"


class JSONResponse(Response):
    content_type = "application/json"


class RedirectResponse(Response):
    ...
