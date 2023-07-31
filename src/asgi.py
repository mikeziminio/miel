from typing import TypedDict, Iterable
from enum import StrEnum
from pydantic import BaseModel

# https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope


class ASGIType(StrEnum):
    http = "http"
    websocket = "websocket"


class ASGIVersion(TypedDict):
    version: str                    # Version of the ASGI spec
    spec_version: str = "2.0"       # Version of the ASGI HTTP spec this server understands;
                                    # one of "2.0", "2.1", "2.2" or "2.3".
                                    # Optional; if missing assume 2.0.


class HTTPVersion(StrEnum):
    http10 = "1.0"
    http11 = "1.1"
    http2 = "2"


class ASGIScope(BaseModel):
    type: ASGIType                  # "http" или "websocket"
    asgi: ASGIVersion
    http_version: HTTPVersion       # For websocket: NOT "1.0", ONLY "1.1" or "2"
    method: str                     # The HTTP method name, uppercased

    scheme: str                     # URL scheme portion (LIKELY "http" / "https" / "ws" / "wss").
                                    # Optional (but must not be empty).
                                    # For "http" type: default is "http".
                                    # For "websocket" type: default id "ws".

    path: str                       # HTTP request target excluding any query string,
                                    # with percent-encoded sequences and UTF-8 byte sequences decoded into characters.

    raw_path: str | None = None     # The original HTTP path component unmodified from the bytes
                                    # that were received by the web server.
                                    # Some web server implementations may be unable to provide this.
                                    # Optional; if missing defaults to None.

    query_string: str = ""          # URL portion after the ?.
                                    # Optional; if missing or None default is empty string.

    root_path: str = ""             # The root path this application is mounted at;
                                    # same as SCRIPT_NAME in WSGI.
                                    # Optional; if missing defaults to "".

    headers: Iterable[bytes, bytes]     # headers

