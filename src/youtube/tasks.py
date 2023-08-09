from celery import shared_task
import logging
# import pytube
from yt_dlp import YoutubeDL

from .models import YouTubeVideo

logger = logging.getLogger(__name__)

@shared_task(serializer='pickle')
def download_video(yt_video: YouTubeVideo):
    with YoutubeDL() as downloader:
        logger.info(f"Downloading video: {yt_video.name}")

        download_ret_code = downloader.download([yt_video.url])
        
    if not download_ret_code == 0:
        raise Exception("Ошибка при загрузке видео")
    logger.info(f"Video {yt_video.name} saved to {yt_video.path}")
    return {"id": yt_video.id, "path": yt_video.path}
