from typing import Iterable, Any, Literal, Callable
from typing_extensions import TypedDict
from enum import StrEnum
from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
    ValidationError
)
from http import HTTPStatus

# https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope


class ScopeType(StrEnum):
    http = "http"
    websocket = "websocket"


class ScopeVersion(TypedDict):
    # Version of the ASGI spec
    version: str

    # Version of the ASGI HTTP spec this server understands;
    # one of "2.0", "2.1", "2.2" or "2.3".
    # Optional; if missing assume 2.0.
    spec_version: str = "2.0"


class HTTPVersion(StrEnum):
    http10 = "1.0"
    http11 = "1.1"
    http2 = "2"


class Scope(BaseModel):

    # "http" or "websocket"
    type: ScopeType

    asgi: ScopeVersion

    # For websocket: NOT "1.0", ONLY "1.1" or "2"
    http_version: HTTPVersion

    @model_validator(mode="before")
    @classmethod
    def validate_http_version(cls, data: dict) -> dict:
        if data.get("type") == "websocket":
            # согласно спецификации значение по-умолчанию для http_version
            # устанавливается только в случае type="websocket"
            if not data.get("http_version"):
                data["http_version"] = "1.1"
            else:
                # для websocket недоступно http 1.0
                if data["http_version"] not in ("1.1", "2"):
                    raise ValidationError("Для websocket недоступно HTTP 1.0")
        return data

    # The HTTP method name, uppercased
    method: str

    # URL scheme portion (LIKELY "http" / "https" / "ws" / "wss").
    # Optional (but must not be empty).
    # For "http" type: default is "http".
    # For "websocket" type: default id "ws".
    scheme: str

    # HTTP request target excluding any query string,
    # with percent-encoded sequences and UTF-8 byte sequences decoded into characters.
    path: str

    # The original HTTP path component unmodified from the bytes
    # that were received by the web server.
    # Some web server implementations may be unable to provide this.
    # Optional; if missing defaults to None.
    raw_path: str | None = None

    # URL portion after the ?.
    # Optional; if missing or None default is empty string.
    query_string: str = ""

    # The root path this application is mounted at;
    # same as SCRIPT_NAME in WSGI.
    # Optional; if missing defaults to "".
    root_path: str = ""

    # headers
    headers: tuple[tuple[bytes, bytes], ...]          # TODO: возможно, преобразовать в tuple

    # client [host, port]
    client: tuple[str, int]

    # server [host, port] or server [unix socket, None]
    server: tuple[str, int | None]

    # Websocket only
    subprotocols: tuple[str] = []

    @model_validator(mode="after")
    def validate_subprotocols(self) -> 'Scope':
        if self.type != ScopeType.websocket and self.subprotocols:
            raise ValidationError("subprotocols разрешены только для websocket")
        return self

    # A copy of the namespace passed into
    # the lifespan corresponding to this request. (See Lifespan Protocol).
    # Optional; if missing the server does not support this feature.
    state: dict[str, Any] | None


class HTTPRequest(BaseModel):
    type: Literal["http.request"]
    body: bytes = b""
    more_body: bool = False


class HTTPDisconnect(BaseModel):
    type: Literal["http.disconnect"]


class HTTPResponseStart(BaseModel):
    type: Literal["http.response.start"] = "http.response.start"
    status: HTTPStatus
    headers: list[list[bytes]]

    # Signifies if the application will send trailers.
    # If True, the server must wait until it receives
    # a "http.response.trailers" message after the Response Body event.
    # Optional; if missing defaults to False.
    trailers: bool = False


class HTTPResponseBody(BaseModel):
    type: Literal["http.response.body"] = "http.response.body"
    body: bytes = b""

    # Signifies if there is additional content to come (as part of a Response Body message).
    # Optional; if missing defaults to False
    more_body: bool = False


async def receive_event(receive: Callable) -> HTTPRequest | HTTPDisconnect:
    e = await receive()
    match e.get("type"):
        case "http.request":
            return HTTPRequest.model_validate(e)
        case "http.disconnect":
            return HTTPDisconnect.model_validate(e)
        case _:
            raise ValueError(f"Неизвестный тип сообщения {e.get('type')}")


async def send_event(send: Callable, event: HTTPResponseStart | HTTPResponseBody):
    if not isinstance(event, HTTPResponseStart | HTTPResponseBody):
        raise ValueError(f"Тип event должен соответствовать HTTPResponseStart | HTTPResponseBody")
    return await send(event.model_dump())

