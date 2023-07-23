from celery import shared_task
import json
import logging
import pytube
import yt_dlp

from .models import YouTubeVideo
from api.settings import DOWNLOAD_PATH
from .producer import send_download_confirmation

logger = logging.getLogger(__name__)   

@shared_task(serializer='pickle')
def download_video(downloader: yt_dlp.YoutubeDL, yt_video: YouTubeVideo, chat_id: int, message_id: int, download_path: str=DOWNLOAD_PATH, skip_existing=True):
    logger.info(f"Downloading video: {yt_video.name}")
    download_status = downloader.download([yt_video.url])
    if not download_status == 0:
        raise Exception("Ошибка при загрузке видео")
    logger.info(f"Video {yt_video.name} saved to {yt_video.path}")
    logger.info(f"{chat_id=}")
    logger.info(f"{message_id=}")
    if chat_id:
        send_download_confirmation(json.dumps({'yt_video_id': str(yt_video.id), "chat_id": chat_id, "message_id": message_id}))
    return yt_video.path
