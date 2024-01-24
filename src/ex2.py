from starlette.responses import PlainTextResponse


async def app(scope, receive, send):

    # r = PlainTextResponse(b"Hi there")
    # print(r)

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ]
    })

    await send({
        "type": "http.response.body",
        "status":
    })

