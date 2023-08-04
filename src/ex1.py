from asgi import ASGIScope


async def app(_scope, receive, send):
    scope = ASGIScope.model_validate(_scope)
    print(vars(scope))
    return

    # event = await receive()
    # print("<event>")
    # print(event)
    # print("</event>")
    # await send({
    #     "type": "http.response.start",
    #     "status": 200,
    #     "headers": [
    #         [b"content-type", b"text/plain"],
    #     ]
    # })
    # await send({
    #     "type": "http.response.body"
    #     "body": b"Hi there",
    # })
