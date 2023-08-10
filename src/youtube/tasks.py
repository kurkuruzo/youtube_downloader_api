from celery import shared_task
import logging
import os
from yt_dlp import YoutubeDL

from api.settings import DOWNLOAD_PATH
from .models import DownloadRequest

logger = logging.getLogger(__name__)

@shared_task(serializer='pickle')
def download_video(download_request: DownloadRequest):
    if not download_request.video:
        raise Exception("Не указано видео для загрузки")
    with YoutubeDL(params={"outtmpl": {"default": os.path.join(DOWNLOAD_PATH, download_request.video.path)}}) as downloader:
        logger.info(f"Downloading video: {download_request.video.name}")

        download_ret_code = downloader.download([download_request.video.url])

    if not download_ret_code == 0:
        raise Exception("Ошибка при загрузке видео")
    logger.info(f"Video {download_request.video.name} saved to {download_request.video.path}")
    download_request.status = "SUCCESS"
    download_request.save()
    return {"video_id": download_request.video.id, "path": download_request.video.path}
