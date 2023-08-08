from miel.responses import HTMLResponse
from miel.applications import Application

app = Application()


@app.get("/")
async def something():
    return b"1"


@app.get("/hello")
async def something():
    return b"2"


@app.post("/hello/{my}")
async def something(my: str):
    return b"__" + bytes(my, "utf-8") + b"__"


