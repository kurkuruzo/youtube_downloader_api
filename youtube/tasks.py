from uuid import UUID
from celery import shared_task
from django.utils import timezone
import logging
import pytube
from typing import Optional

from .models import YouTubeVideo
import youtube.config as config
   
logger = logging.getLogger(__name__)   
     
@shared_task(serializer='pickle')
def download_video(yt_stream: pytube.Stream, download_path: str=config.DOWNLOAD_PATH, skip_existing=True):
    logger.info(f"Downloading video: {yt_stream.title}")
    file_path = yt_stream.download(output_path=download_path, skip_existing=skip_existing)
    logger.info(f"Video {yt_stream.title} saved to {file_path}")
    return file_path
    