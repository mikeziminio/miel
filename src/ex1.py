
async def app(scope, receive, send):
    print("<scope>")
    print(scope)
    print("</scope>")
    event = await receive()
    print("<event>")
    print(event)
    print("</event>")
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ]
    })
    await send({
        "type": "http.response.body"
        "body": b"Hi there",
    })
