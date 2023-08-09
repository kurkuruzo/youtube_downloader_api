from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class YoutubeVideo(BaseModel):
    url: str
    title: Optional[str]
    thumbnail: Optional[str]
    duration: Optional[int]


class DownloadRequest(BaseModel):
    url: str
    video: Optional[YoutubeVideo] = None
    date_added: Optional[datetime] = datetime.now()
    status: str = "pending"


class TelegramDownloadRequest(DownloadRequest):
    chat_id: int
    message_id: int
