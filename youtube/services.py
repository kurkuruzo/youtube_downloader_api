import json
import logging
import pytube
from typing import Optional
from django.utils import timezone
from .models import YouTubeVideo
from .producer import send_download_confirmation
from .tasks import download_video

class YouTubeError(Exception):
    pass
logger = logging.getLogger(__name__)

def add_video(url: str, chat_id: int = None, message_id: int = None):
    logger.info(f"STARTING ASYNC TASK FOR VIDEO {url}")
    video_in_db = _video_in_db(url)
    logger.info(f"{video_in_db=}")
    if video_in_db:
        if chat_id:
            send_download_confirmation(json.dumps({'yt_video_id': str(video_in_db.id), "chat_id": chat_id, "message_id": message_id}))
        return (video_in_db.id, "")
    logger.info("Getting downloader")
    yt_downloader = get_downloader(url=url)
    logger.info("Got downloader")
    logger.info("Creating video object")
    yt_video = create_video_obj(url=url, downloader=yt_downloader)
    logger.info(f"Created video object {yt_video}")
    logger.info("Sending request to YouTube for stream...")
    try:
        logger.info(f"{yt_downloader.streams.all()}")
        stream = yt_downloader.streams.get_highest_resolution()
    except Exception as e:
        logger.exception(e)
        raise YouTubeError(e)
    else:
        if stream:
            logger.info(f"Received stream {stream.itag} / {stream.resolution}")
            yt_video.path = stream.default_filename
            yt_video.filesize = stream.filesize
            yt_video.save()
            download_task = download_video.delay(stream, yt_video, chat_id, message_id)
            logger.info(f"{download_task=}")
            return (yt_video.id, download_task.id)
        raise YouTubeError("Stream not found!")

def create_video_obj(url: str, downloader: pytube.YouTube) -> YouTubeVideo:
    video_obj = YouTubeVideo(name=downloader.title, description=downloader.description, url=url, length=downloader.length, date_added=timezone.now(), thumbnail=downloader.thumbnail_url)
    return video_obj
    
def _video_in_db(url: str) -> Optional[YouTubeVideo]:
    logger.info(f"Found video with url={url}, video object={YouTubeVideo.objects.filter(url=url).first()}")
    return YouTubeVideo.objects.filter(url=url).first()    
    
def get_downloader(url: str) -> pytube.YouTube:
    yt_downloader = pytube.YouTube(url, on_complete_callback=_download_completed, on_progress_callback=_download_progress)
    logger.info(yt_downloader)
    return yt_downloader

def _download_completed(stream: pytube.Stream, file_path: str) -> None:
    logger.info(f"{stream.title} download finished")
    # return file_path

def _download_progress(stream: pytube.Stream, chunk, bytes_remaining) -> None:
    logger.info(
        f"{stream.title} progress: {round((1 - (bytes_remaining / stream.filesize)) * 100, 0)}%"
    )
