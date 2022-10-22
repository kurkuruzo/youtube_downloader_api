import json
import logging
import pytube
from typing import Optional
from django.utils import timezone
from .models import YouTubeVideo
from .tasks import download_video


class YouTubeError(Exception):
    pass


logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('django_services.log', mode='a'))

def add_video(url: str, chat_id: int = None, message_id: int = None):
    logger.info(f"STARTING ASYNC TASK FOR VIDEO {url}")
    video_in_db = _video_in_db(url)
    logger.info(f"{video_in_db=}")
    yt_downloader = get_downloader(url=url)
    if video_in_db:
        if not video_in_db.filesize_OK:
            video = video_in_db
        else:
            return (video_in_db.id, "")
    else:
        video = create_video_obj(url=url, downloader=yt_downloader)
    return _download_video(url=url, downloader=yt_downloader, video=video, chat_id=chat_id, message_id=message_id)

def _download_video(url: str, downloader: pytube.YouTube, video: YouTubeVideo, chat_id: int, message_id: int):
    try:
        stream = downloader.streams.get_highest_resolution()
    except Exception as e:
        logger.exception(e)
        raise YouTubeError(e)
    else:
        if not YouTubeVideo.objects.filter(id=str(video.id)):
            video.path = stream.default_filename
            video.filesize = stream.filesize
            video.save()
        download_task = download_video.delay(stream, video, chat_id, message_id)
        logger.info(f"{download_task=}")
        return (video.id, download_task.id)

def create_video_obj(url: str, downloader: pytube.YouTube) -> YouTubeVideo:
    video_obj = YouTubeVideo(
        name=downloader.title,
        description=downloader.description,
        url=url,
        length=downloader.length,
        date_added=timezone.now(),
        thumbnail=downloader.thumbnail_url,
    )
    logger.info(f"{video_obj.__dict__=}")
    return video_obj


def _video_in_db(url: str) -> Optional[YouTubeVideo]:
    logger.info(
        f"Found video with url={url}, video object={YouTubeVideo.objects.filter(url=url).first()}"
    )
    return YouTubeVideo.objects.filter(url=url).first()


def get_downloader(url: str) -> pytube.YouTube:
    yt_downloader = pytube.YouTube(
        url,
        on_complete_callback=_download_completed,
        on_progress_callback=_download_progress,
    )
    logger.info(yt_downloader)
    return yt_downloader


def _download_completed(stream: pytube.Stream, file_path: str) -> None:
    logger.info(f"{stream.title} download finished")
    # return file_path


def _download_progress(stream: pytube.Stream, chunk, bytes_remaining) -> None:
    logger.info(
        f"{stream.title} progress: {round((1 - (bytes_remaining / stream.filesize)) * 100, 0)}%"
    )
