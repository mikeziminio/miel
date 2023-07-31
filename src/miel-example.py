from miel import App

app = App()

@app.get("/sdr")
async def some():
    return "hello"

