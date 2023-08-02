from typing import TypedDict, Iterable, Any
from enum import StrEnum
from pydantic import BaseModel

# https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope


class ASGIType(StrEnum):
    http = "http"
    websocket = "websocket"


class ASGIVersion(TypedDict):
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


class ASGIScope(BaseModel):

    # "http" or "websocket"
    type: ASGIType

    asgi: ASGIVersion

    # For websocket: NOT "1.0", ONLY "1.1" or "2"
    http_version: HTTPVersion

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
    headers: Iterable[bytes, bytes]

    # client [host, port]
    client: Iterable[str, int]

    # server [host, port] or server [unix socket, None]
    server: Iterable[str, int | None]

    # A copy of the namespace passed into
    # the lifespan corresponding to this request. (See Lifespan Protocol).
    # Optional; if missing the server does not support this feature.
    state: dict[str, Any] | None

