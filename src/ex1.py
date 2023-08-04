from miel.responses import HTMLResponse
from miel.applications import Application

app = Application()


@app.get("/hello")
async def something():
    return 1


@app.post("/hello/my")
async def something():
    return 1

