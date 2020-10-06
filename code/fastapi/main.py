from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/api/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/items/{item_id}/")
def read_item(item_id: str, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/aaa/", response_class=HTMLResponse)
async def read_html():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
