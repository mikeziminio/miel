from typing import Callable
from starlette.responses import PlainTextResponse
from pydantic import BaseModel
from enum import StrEnum

# https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope


async def app(scope: dict, receive: Callable, send: Callable[dict]):

    print(dict(scope))
    print("\n\n")

    r = await receive()
    print(r)
    print("\n\n")

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ]
    })

    await send({
        "type": "http.response.body",
        "body": b"hello"
    })

