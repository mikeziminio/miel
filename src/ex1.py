from miel.responses import HTMLResponse
from miel.applications import Application

app = Application()


@app.get("/")
async def something():
    return 1


@app.get("/hello")
async def something():
    return 2


@app.post("/hello/{name}")
async def something(name: str):
    return f"Hello, {name}!"


