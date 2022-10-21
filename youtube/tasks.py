from celery import shared_task
import json
import logging
import pytube

from .models import YouTubeVideo
import youtube.config as config
from .producer import send_download_confirmation
   
logger = logging.getLogger(__name__)   
     
@shared_task(serializer='pickle')
def download_video(yt_stream: pytube.Stream, yt_video: YouTubeVideo, chat_id: int, message_id: int, download_path: str=config.DOWNLOAD_PATH, skip_existing=True):
    logger.info(f"Downloading video: {yt_stream.title}")
    file_path = yt_stream.download(output_path=download_path, skip_existing=skip_existing)
    logger.info(f"Video {yt_stream.title} saved to {file_path}")
    logger.info(f"{chat_id=}")
    logger.info(f"{message_id=}")
    if chat_id:
        send_download_confirmation(json.dumps({'yt_video_id': str(yt_video.id), "chat_id": chat_id, "message_id": message_id}))
    return file_path
    