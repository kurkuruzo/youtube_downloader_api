from fastapi import FastAPI

from models import DownloadRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/videos/")
async def add_video_for_download(download_request: DownloadRequest):
    return {"request": download_request}
